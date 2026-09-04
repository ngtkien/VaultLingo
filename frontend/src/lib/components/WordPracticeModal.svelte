<script lang="ts">
  import {
    X,
    Zap,
    Volume2,
    Check,
    CheckCircle2,
    XCircle,
    RotateCcw,
    Bookmark,
    ArrowRight,
    HelpCircle
  } from "lucide-svelte";
  import { playTTS } from "../utils/audio";
  import { SaveWordToObsidian } from "../../../wailsjs/go/main/App.js";

  let {
    word,
    isOpen = false,
    onClose,
    onWordSaved
  } = $props<{
    word: any;
    isOpen: boolean;
    onClose: () => void;
    onWordSaved?: (w: any) => void;
  }>();

  // Distractor definitions pool for Question 1
  const DEFINITION_DISTRACTORS = [
    "To make something greater in amount, degree, or intensity through deliberate cultivation.",
    "A state of perplexity or deep uncertainty when facing conflicting alternatives.",
    "The capacity to persist through adversity and regain original form or balance.",
    "Existing or occurring at the exact same time as another event or phenomenon.",
    "To officially cancel or repeal a law, regulation, or formal agreement.",
    "Showing deep, perceptive insight into complex problems or human motives.",
    "A gradual accumulation or gathering of materials or information over time.",
    "Relating to practical rather than theoretical considerations or applications.",
    "To clarify or elucidate a previously obscure or misunderstood concept.",
    "Characterized by rapid, unpredictable fluctuations in mood or circumstances.",
    "To foster, encourage, and stimulate the healthy growth of an initiative.",
    "A fundamental standard, criterion, or touchstone by which things are evaluated."
  ];

  let currentStep = $state(0); // 0 to 4 (5 drills), 5 = completed
  let score = $state(0);
  let answeredSteps = $state<Record<number, boolean>>({});
  let isCorrectMap = $state<Record<number, boolean>>({});
  let isSavedToVault = $state(false);

  // Drill 1: Meaning Recall state
  let d1Options = $state<string[]>([]);
  let d1Selected = $state<string | null>(null);

  // Drill 2: Contextual Cloze state
  let d2Sentence = $state<{ before: string; blank: string; after: string; full: string }>({ before: "", blank: "", after: "", full: "" });
  let d2Input = $state("");
  let d2Submitted = $state(false);
  let d2ShowHint = $state(false);

  // Drill 3: Part of Speech state
  let d3Options = $state<{ label: string; desc: string; pos: string }[]>([]);
  let d3Selected = $state<string | null>(null);

  // Drill 4: Listening & Spelling state
  let d4Input = $state("");
  let d4Submitted = $state(false);

  // Drill 5: Sentence Scramble state
  let d5Tokens = $state<{ id: number; text: string; used: boolean }[]>([]);
  let d5SelectedTokens = $state<{ id: number; text: string }[]>([]);
  let d5Submitted = $state(false);
  let d5TargetSentence = $state("");

  // Setup drill data whenever word changes or modal opens
  $effect(() => {
    if (isOpen && word) {
      initDrill();
    }
  });

  function cleanString(text: string | undefined | null): string {
    if (!text) return "";
    return text
      .replace(/:\s*:\s*id=[^"\s]*/gi, "")
      .replace(/id=[a-zA-Z0-9._&=-]+/gi, "")
      .replace(/\s*\b\d{3,}\b\s*$/, "")
      .trim();
  }

  function getCleanTargetSentence(rawExample: string | undefined): string {
    if (!rawExample) return `The concept of ${word.word} is widely recognized in academic literature.`;
    const cleaned = cleanString(rawExample);
    const parts = cleaned.split(/\s*[/|]\s*/).map(s => s.trim()).filter(Boolean);
    const main = parts[0] || cleaned;
    const match = main.match(/[^.!?]+[.!?]/);
    return match ? match[0].trim() : main.trim();
  }

  function initDrill() {
    currentStep = 0;
    score = 0;
    answeredSteps = {};
    isCorrectMap = {};
    isSavedToVault = false;

    // Drill 1: Meaning Recall setup
    const correctDef = cleanString(word.definition_en) || cleanString(word.definition_vi) || "The specific quality or action denoted by this term.";
    const shuffledDistractors = DEFINITION_DISTRACTORS
      .filter(d => d.toLowerCase() !== correctDef.toLowerCase())
      .sort(() => Math.random() - 0.5)
      .slice(0, 3);
    d1Options = [correctDef, ...shuffledDistractors].sort(() => Math.random() - 0.5);
    d1Selected = null;

    // Drill 2: Cloze setup
    const targetWord = (word.word || "").trim();
    const sentence = getCleanTargetSentence(word.example_en);
    const regex = new RegExp(`\\b(${targetWord}[a-z]*)\\b`, "i");
    const match = sentence.match(regex);

    if (match && match.index !== undefined) {
      d2Sentence = {
        before: sentence.slice(0, match.index),
        blank: match[1],
        after: sentence.slice(match.index + match[1].length),
        full: sentence
      };
    } else {
      d2Sentence = {
        before: "Understanding the practical significance of ",
        blank: targetWord,
        after: " requires comprehensive analysis.",
        full: `Understanding the practical significance of ${targetWord} requires comprehensive analysis.`
      };
    }
    d2Input = "";
    d2Submitted = false;
    d2ShowHint = false;

    // Drill 3: Part of Speech setup
    const rawPos = (word.pos || "noun").toLowerCase();
    const normalizedPos = rawPos.includes("adj") ? "adjective" : rawPos.includes("verb") ? "verb" : rawPos.includes("adv") ? "adverb" : "noun";
    d3Options = [
      { label: "Noun", desc: "Names a person, place, entity, or abstract concept", pos: "noun" },
      { label: "Verb", desc: "Denotes an action, occurrence, or state of being", pos: "verb" },
      { label: "Adjective", desc: "Modifies, qualifies, or characterizes a noun", pos: "adjective" },
      { label: "Adverb", desc: "Modifies verbs, adjectives, or clauses specifying manner", pos: "adverb" }
    ];
    d3Selected = null;

    // Drill 4: Audio Listening setup
    d4Input = "";
    d4Submitted = false;

    // Drill 5: Sentence Scramble setup
    const targetSent = getCleanTargetSentence(word.example_en);
    d5TargetSentence = targetSent;
    const rawTokens = targetSent.replace(/([.?!,])/g, " $1 ").trim().split(/\s+/);
    d5Tokens = rawTokens
      .map((tok, idx) => ({ id: idx, text: tok, used: false, sortKey: Math.random() }))
      .sort((a, b) => a.sortKey - b.sortKey)
      .map(t => ({ id: t.id, text: t.text, used: false }));
    d5SelectedTokens = [];
    d5Submitted = false;
  }

  // Action handlers
  function handleSelectD1(option: string) {
    if (answeredSteps[0]) return;
    d1Selected = option;
    answeredSteps[0] = true;

    const correctDef = cleanString(word.definition_en) || cleanString(word.definition_vi);
    const isCorrect = option === correctDef || option.toLowerCase() === correctDef.toLowerCase();
    isCorrectMap[0] = isCorrect;
    if (isCorrect) score++;
  }

  function handleCheckD2() {
    if (answeredSteps[1] || !d2Input.trim()) return;
    d2Submitted = true;
    answeredSteps[1] = true;

    const userVal = d2Input.trim().toLowerCase();
    const targetVal = d2Sentence.blank.trim().toLowerCase();
    const baseVal = (word.word || "").trim().toLowerCase();
    const isCorrect = userVal === targetVal || userVal === baseVal;
    isCorrectMap[1] = isCorrect;
    if (isCorrect) score++;
  }

  function handleSelectD3(pos: string) {
    if (answeredSteps[2]) return;
    d3Selected = pos;
    answeredSteps[2] = true;

    const rawPos = (word.pos || "noun").toLowerCase();
    const correctPos = rawPos.includes("adj") ? "adjective" : rawPos.includes("verb") ? "verb" : rawPos.includes("adv") ? "adverb" : "noun";
    const isCorrect = pos === correctPos;
    isCorrectMap[2] = isCorrect;
    if (isCorrect) score++;
  }

  function handleCheckD4() {
    if (answeredSteps[3] || !d4Input.trim()) return;
    d4Submitted = true;
    answeredSteps[3] = true;

    const userVal = d4Input.trim().toLowerCase();
    const targetVal = (word.word || "").trim().toLowerCase();
    const isCorrect = userVal === targetVal;
    isCorrectMap[3] = isCorrect;
    if (isCorrect) score++;
  }

  function handleSelectD5Token(token: { id: number; text: string; used: boolean }) {
    if (d5Submitted || token.used) return;
    token.used = true;
    d5SelectedTokens = [...d5SelectedTokens, { id: token.id, text: token.text }];
  }

  function handleDeselectD5Token(item: { id: number; text: string }) {
    if (d5Submitted) return;
    const origin = d5Tokens.find(t => t.id === item.id);
    if (origin) origin.used = false;
    d5SelectedTokens = d5SelectedTokens.filter(t => t !== item);
  }

  function handleResetD5() {
    if (d5Submitted) return;
    d5Tokens.forEach(t => (t.used = false));
    d5SelectedTokens = [];
  }

  function handleCheckD5() {
    if (answeredSteps[4] || d5SelectedTokens.length === 0) return;
    d5Submitted = true;
    answeredSteps[4] = true;

    const assembled = d5SelectedTokens
      .map(t => t.text)
      .join(" ")
      .replace(/\s+([.,?!])/g, "$1")
      .trim()
      .toLowerCase();

    const target = d5TargetSentence.trim().toLowerCase();
    const isCorrect = assembled === target;
    isCorrectMap[4] = isCorrect;
    if (isCorrect) score++;
  }

  function nextStep() {
    if (currentStep < 4) {
      currentStep++;
      if (currentStep === 3) {
        playTTS(word.word, 1.0);
      }
    } else {
      currentStep = 5;
    }
  }

  async function handleSaveToVault() {
    try {
      await SaveWordToObsidian(word);
      isSavedToVault = true;
      if (onWordSaved) onWordSaved(word);
    } catch (err) {
      console.error("Failed to save word to Obsidian:", err);
    }
  }
</script>

{#if isOpen && word}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    onclick={onClose}
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 animate-in fade-in duration-200"
  >
    <div
      onclick={(e) => e.stopPropagation()}
      class="journal-card w-full max-w-2xl bg-[var(--bg-card)] border border-[var(--border-main)] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh] animate-in zoom-in-95 duration-200"
    >
      <!-- Modal Header -->
      <div class="px-5 py-4 border-b border-[var(--border-main)] flex items-center justify-between bg-[var(--bg-inner)]">
        <div class="flex items-center gap-2.5">
          <span class="p-1.5 rounded-lg bg-[var(--accent-primary-light)] text-[var(--accent-primary)] shadow-2xs">
            <Zap class="w-4 h-4 fill-[var(--accent-primary)]/20" />
          </span>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-serif font-bold text-base text-[var(--text-main)]">
                {word.word}
              </span>
              {#if word.phonetic}
                <span class="text-xs font-mono text-[var(--accent-primary)]">
                  [{word.phonetic}]
                </span>
              {/if}
              <span class="px-1.5 py-0.2 rounded text-[10px] uppercase font-mono bg-[var(--bg-card)] text-[var(--text-subtle)] border border-[var(--border-main)] font-semibold">
                {word.pos || "word"}
              </span>
            </div>
            <p class="text-[11px] text-[var(--text-muted)] font-sans">
              Word Workout • 5-Step Active Recall
            </p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <!-- Step Indicator Pills -->
          <div class="hidden sm:flex items-center gap-1.5">
            {#each [0, 1, 2, 3, 4] as stepIdx}
              <div
                class={`w-5 h-1.5 rounded-full transition-all duration-300 ${
                  currentStep === 5
                    ? "bg-emerald-500"
                    : currentStep === stepIdx
                    ? "bg-[var(--accent-primary)] w-7"
                    : answeredSteps[stepIdx]
                    ? isCorrectMap[stepIdx]
                      ? "bg-emerald-500/80"
                      : "bg-red-400"
                    : "bg-[var(--border-main)]"
                }`}
              ></div>
            {/each}
          </div>

          <button
            type="button"
            onclick={onClose}
            class="p-1.5 rounded-lg hover:bg-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)] transition cursor-pointer"
            title="Close drill"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Modal Body (Dynamic Drills) -->
      <div class="p-5 sm:p-6 overflow-y-auto space-y-5 flex-1 select-text">
        <!-- DRILL 1: Meaning Recall -->
        {#if currentStep === 0}
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--accent-primary)]">
                Drill 1 / 5 • Meaning Recall
              </span>
              <span class="text-xs text-[var(--text-subtle)] font-mono">Multiple Choice</span>
            </div>

            <h3 class="font-serif text-lg font-bold text-[var(--text-main)] leading-snug">
              Which definition best expresses the meaning of <span class="text-[var(--accent-primary)] underline underline-offset-4 decoration-1">{word.word}</span>?
            </h3>

            <div class="space-y-2.5 pt-1">
              {#each d1Options as opt, idx}
                <button
                  type="button"
                  onclick={() => handleSelectD1(opt)}
                  disabled={answeredSteps[0]}
                  class={`w-full p-3.5 rounded-xl border text-left text-xs font-sans transition cursor-pointer flex items-start gap-3 ${
                    answeredSteps[0]
                      ? opt === (cleanString(word.definition_en) || cleanString(word.definition_vi))
                        ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-800 dark:text-emerald-300 font-semibold"
                        : d1Selected === opt
                        ? "bg-red-500/10 border-red-500/40 text-red-700 dark:text-red-400"
                        : "bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] opacity-60"
                      : "bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] hover:border-[var(--accent-primary-border)] border-[var(--border-main)] text-[var(--text-main)]"
                  }`}
                >
                  <span class="w-5 h-5 rounded-full border border-[var(--border-main)] flex items-center justify-center font-mono text-[11px] shrink-0 font-bold">
                    {String.fromCharCode(65 + idx)}
                  </span>
                  <span class="leading-relaxed flex-1">{opt}</span>
                </button>
              {/each}
            </div>

            <!-- Feedback & Explanation -->
            {#if answeredSteps[0]}
              <div class={`p-3.5 rounded-xl border text-xs space-y-1 ${
                isCorrectMap[0]
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-800 dark:text-emerald-300"
                  : "bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400"
              }`}>
                <div class="font-bold flex items-center gap-1.5">
                  {#if isCorrectMap[0]}
                    <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                    <span>Precisely correct!</span>
                  {:else}
                    <XCircle class="w-4 h-4 text-red-600" />
                    <span>Not quite. Check the primary definition:</span>
                  {/if}
                </div>
                {#if word.definition_vi}
                  <p class="text-[11px] opacity-90 italic pt-0.5">
                    Nghĩa tiếng Việt: {word.definition_vi}
                  </p>
                {/if}
              </div>
            {/if}
          </div>

        <!-- DRILL 2: Contextual Cloze -->
        {:else if currentStep === 1}
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--accent-primary)]">
                Drill 2 / 5 • Contextual Cloze
              </span>
              <span class="text-xs text-[var(--text-subtle)] font-mono">Fill in the blank</span>
            </div>

            <h3 class="font-serif text-lg font-bold text-[var(--text-main)] leading-snug">
              Complete the sentence with the target word:
            </h3>

            <!-- Sentence Card -->
            <div class="p-4.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] font-serif text-sm text-[var(--text-main)] leading-relaxed">
              <span>{d2Sentence.before}</span>
              <span class="inline-block px-3 py-0.5 mx-1 font-mono font-bold text-xs rounded border border-dashed border-[var(--accent-primary)] bg-[var(--bg-card)] text-[var(--accent-primary)]">
                {#if answeredSteps[1]}
                  {d2Sentence.blank}
                {:else if d2ShowHint}
                  {d2Sentence.blank[0]} _ _ _ _ ({d2Sentence.blank.length} letters)
                {:else}
                  [ ________ ]
                {/if}
              </span>
              <span>{d2Sentence.after}</span>
            </div>

            <!-- Input area -->
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <input
                  type="text"
                  bind:value={d2Input}
                  disabled={answeredSteps[1]}
                  onkeydown={(e) => e.key === "Enter" && handleCheckD2()}
                  placeholder="Type the missing word here..."
                  class="flex-1 journal-input px-3.5 py-2.5 rounded-xl border border-[var(--border-main)] bg-[var(--bg-inner)] text-xs text-[var(--text-main)] font-mono focus:border-[var(--accent-primary)] focus:outline-none"
                />
                <button
                  type="button"
                  onclick={handleCheckD2}
                  disabled={answeredSteps[1] || !d2Input.trim()}
                  class="btn-forest px-4 py-2.5 rounded-xl text-xs font-semibold cursor-pointer disabled:opacity-50"
                >
                  Verify
                </button>
              </div>

              <!-- Hint button -->
              {#if !answeredSteps[1]}
                <div class="flex justify-end">
                  <button
                    type="button"
                    onclick={() => d2ShowHint = !d2ShowHint}
                    class="text-[11px] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center gap-1"
                  >
                    <HelpCircle class="w-3.5 h-3.5" />
                    <span>{d2ShowHint ? "Hide hint" : "Show letter hint"}</span>
                  </button>
                </div>
              {/if}
            </div>

            <!-- Feedback -->
            {#if answeredSteps[1]}
              <div class={`p-3.5 rounded-xl border text-xs space-y-1 ${
                isCorrectMap[1]
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-800 dark:text-emerald-300"
                  : "bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400"
              }`}>
                <div class="font-bold flex items-center gap-1.5">
                  {#if isCorrectMap[1]}
                    <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                    <span>Spot on! Target word inserted accurately.</span>
                  {:else}
                    <XCircle class="w-4 h-4 text-red-600" />
                    <span>The expected answer was: <strong class="font-mono">{d2Sentence.blank}</strong></span>
                  {/if}
                </div>
              </div>
            {/if}
          </div>

        <!-- DRILL 3: Part of Speech -->
        {:else if currentStep === 2}
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--accent-primary)]">
                Drill 3 / 5 • Grammatical Function
              </span>
              <span class="text-xs text-[var(--text-subtle)] font-mono">Part of Speech</span>
            </div>

            <h3 class="font-serif text-lg font-bold text-[var(--text-main)] leading-snug">
              What primary part of speech is <span class="text-[var(--accent-primary)] underline underline-offset-4 decoration-1">{word.word}</span>?
            </h3>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
              {#each d3Options as opt}
                <button
                  type="button"
                  onclick={() => handleSelectD3(opt.pos)}
                  disabled={answeredSteps[2]}
                  class={`p-3.5 rounded-xl border text-left text-xs transition cursor-pointer flex flex-col justify-between space-y-1 ${
                    answeredSteps[2]
                      ? opt.pos === (word.pos || "noun").toLowerCase() || ((word.pos || "").toLowerCase().includes(opt.pos))
                        ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-800 dark:text-emerald-300 font-semibold"
                        : d3Selected === opt.pos
                        ? "bg-red-500/10 border-red-500/40 text-red-700 dark:text-red-400"
                        : "bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] opacity-60"
                      : "bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] hover:border-[var(--accent-primary-border)] border-[var(--border-main)] text-[var(--text-main)]"
                  }`}
                >
                  <div class="font-mono font-bold text-xs uppercase tracking-wider text-[var(--accent-primary)]">
                    {opt.label}
                  </div>
                  <p class="text-[11px] text-[var(--text-muted)] leading-relaxed font-sans">
                    {opt.desc}
                  </p>
                </button>
              {/each}
            </div>

            <!-- Feedback -->
            {#if answeredSteps[2]}
              <div class={`p-3.5 rounded-xl border text-xs space-y-1 ${
                isCorrectMap[2]
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-800 dark:text-emerald-300"
                  : "bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400"
              }`}>
                <div class="font-bold flex items-center gap-1.5">
                  {#if isCorrectMap[2]}
                    <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                    <span>Correct! Categorized as <strong class="uppercase font-mono">{word.pos || "Noun"}</strong>.</span>
                  {:else}
                    <XCircle class="w-4 h-4 text-red-600" />
                    <span>Actually, this word is used as a <strong class="uppercase font-mono">{word.pos || "Noun"}</strong>.</span>
                  {/if}
                </div>
              </div>
            {/if}
          </div>

        <!-- DRILL 4: Audio Listening & Spelling -->
        {:else if currentStep === 3}
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--accent-primary)]">
                Drill 4 / 5 • Audio & Orthography
              </span>
              <span class="text-xs text-[var(--text-subtle)] font-mono">Listening Recall</span>
            </div>

            <h3 class="font-serif text-lg font-bold text-[var(--text-main)] leading-snug">
              Listen to the pronunciation and spell the word accurately:
            </h3>

            <div class="p-5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-col sm:flex-row items-center justify-between gap-3">
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  onclick={() => playTTS(word.word, 1.0)}
                  class="btn-forest px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-sm cursor-pointer"
                >
                  <Volume2 class="w-4 h-4" />
                  <span>Listen (1.0x)</span>
                </button>
                <button
                  type="button"
                  onclick={() => playTTS(word.word, 0.75)}
                  class="px-3 py-2 rounded-xl border border-[var(--border-main)] hover:bg-[var(--accent-primary-light)] text-xs font-mono text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer"
                >
                  Slow 0.75x
                </button>
              </div>

              {#if word.phonetic}
                <span class="font-mono text-xs text-[var(--accent-primary)] font-bold">
                  [{word.phonetic}]
                </span>
              {/if}
            </div>

            <div class="flex items-center gap-2">
              <input
                type="text"
                bind:value={d4Input}
                disabled={answeredSteps[3]}
                onkeydown={(e) => e.key === "Enter" && handleCheckD4()}
                placeholder="Type the word you heard..."
                class="flex-1 journal-input px-3.5 py-2.5 rounded-xl border border-[var(--border-main)] bg-[var(--bg-inner)] text-xs text-[var(--text-main)] font-mono focus:border-[var(--accent-primary)] focus:outline-none"
              />
              <button
                type="button"
                onclick={handleCheckD4}
                disabled={answeredSteps[3] || !d4Input.trim()}
                class="btn-forest px-4 py-2.5 rounded-xl text-xs font-semibold cursor-pointer disabled:opacity-50"
              >
                Submit
              </button>
            </div>

            {#if answeredSteps[3]}
              <div class={`p-3.5 rounded-xl border text-xs space-y-1 ${
                isCorrectMap[3]
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-800 dark:text-emerald-300"
                  : "bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400"
              }`}>
                <div class="font-bold flex items-center gap-1.5">
                  {#if isCorrectMap[3]}
                    <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                    <span>Flawless spelling!</span>
                  {:else}
                    <XCircle class="w-4 h-4 text-red-600" />
                    <span>Spelling target was: <strong class="font-mono">{word.word}</strong></span>
                  {/if}
                </div>
              </div>
            {/if}
          </div>

        <!-- DRILL 5: Sentence Scramble -->
        {:else if currentStep === 4}
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--accent-primary)]">
                Drill 5 / 5 • Sentence Construction
              </span>
              <span class="text-xs text-[var(--text-subtle)] font-mono">Word Scramble</span>
            </div>

            <h3 class="font-serif text-lg font-bold text-[var(--text-main)] leading-snug">
              Reconstruct the authentic sentence by tapping the tokens in order:
            </h3>

            <div class="p-4 min-h-[70px] rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-wrap items-center gap-1.5">
              {#if d5SelectedTokens.length === 0}
                <span class="text-xs font-serif italic text-[var(--text-muted)] opacity-60">
                  Tap word chips below to assemble the sentence...
                </span>
              {:else}
                {#each d5SelectedTokens as item}
                  <button
                    type="button"
                    onclick={() => handleDeselectD5Token(item)}
                    disabled={answeredSteps[4]}
                    class="px-2.5 py-1 rounded-lg bg-[var(--bg-card)] border border-[var(--border-main)] hover:border-red-400 text-xs font-sans text-[var(--text-main)] transition cursor-pointer shadow-2xs"
                  >
                    {item.text}
                  </button>
                {/each}
              {/if}
            </div>

            <div class="flex flex-wrap items-center gap-2 p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
              {#each d5Tokens as tok}
                <button
                  type="button"
                  onclick={() => handleSelectD5Token(tok)}
                  disabled={tok.used || answeredSteps[4]}
                  class={`px-3 py-1.5 rounded-lg text-xs font-sans transition cursor-pointer ${
                    tok.used
                      ? "opacity-25 bg-[var(--bg-card)] border border-transparent cursor-not-allowed"
                      : "bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] text-[var(--text-main)] shadow-2xs"
                  }`}
                >
                  {tok.text}
                </button>
              {/each}
            </div>

            <div class="flex items-center justify-between pt-1">
              <button
                type="button"
                onclick={handleResetD5}
                disabled={answeredSteps[4] || d5SelectedTokens.length === 0}
                class="text-xs text-[var(--text-muted)] hover:text-[var(--text-main)] transition cursor-pointer flex items-center gap-1 disabled:opacity-40"
              >
                <RotateCcw class="w-3.5 h-3.5" />
                <span>Reset tokens</span>
              </button>

              <button
                type="button"
                onclick={handleCheckD5}
                disabled={answeredSteps[4] || d5SelectedTokens.length === 0}
                class="btn-forest px-4 py-2 rounded-xl text-xs font-semibold cursor-pointer disabled:opacity-50"
              >
                Check Sentence
              </button>
            </div>

            {#if answeredSteps[4]}
              <div class={`p-3.5 rounded-xl border text-xs space-y-1 ${
                isCorrectMap[4]
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-800 dark:text-emerald-300"
                  : "bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400"
              }`}>
                <div class="font-bold flex items-center gap-1.5">
                  {#if isCorrectMap[4]}
                    <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                    <span>Sentence accurately constructed!</span>
                  {:else}
                    <XCircle class="w-4 h-4 text-red-600" />
                    <span>Full target sentence:</span>
                  {/if}
                </div>
                <p class="font-serif italic text-xs pt-1 border-t border-[var(--border-main)]">
                  “{d5TargetSentence}”
                </p>
              </div>
            {/if}
          </div>

        <!-- COMPLETED SCREEN -->
        {:else if currentStep === 5}
          <div class="text-center py-6 space-y-6">
            <div class="w-16 h-16 mx-auto rounded-2xl bg-[var(--accent-primary-light)] text-[var(--accent-primary)] flex items-center justify-center shadow-sm">
              <Zap class="w-8 h-8 fill-[var(--accent-primary)]/20" />
            </div>

            <div class="space-y-1">
              <span class="journal-badge text-xs font-mono uppercase font-bold text-[var(--accent-primary)]">
                Mastery Workout Complete
              </span>
              <h2 class="font-serif text-2xl font-bold text-[var(--text-main)]">
                Score: {score} / 5
              </h2>
              <p class="text-xs text-[var(--text-muted)] font-serif italic">
                {#if score === 5}
                  Exceptional active recall! You have firmly consolidated this word into memory.
                {:else if score >= 3}
                  Solid progress! A few minor nuances to sharpen in future reviews.
                {:else}
                  Good initial drill! Consider adding to Obsidian for spaced repetition.
                {/if}
              </p>
            </div>

            <!-- Word summary recap -->
            <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] text-left space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-baseline gap-2">
                  <span class="font-serif font-bold text-base text-[var(--text-main)]">{word.word}</span>
                  {#if word.phonetic}
                    <span class="text-xs font-mono text-[var(--accent-primary)]">[{word.phonetic}]</span>
                  {/if}
                  <span class="text-[10px] uppercase font-mono px-1.5 py-0.2 rounded bg-[var(--bg-card)] text-[var(--text-subtle)] border border-[var(--border-main)]">
                    {word.pos || "word"}
                  </span>
                </div>
                <button
                  type="button"
                  onclick={() => playTTS(word.word, 1.0)}
                  class="p-1 rounded hover:bg-[var(--accent-primary-light)] text-[var(--accent-primary)] transition cursor-pointer"
                  title="Listen"
                >
                  <Volume2 class="w-4 h-4" />
                </button>
              </div>

              {#if word.definition_en}
                <p class="text-xs text-[var(--text-main)] font-sans">
                  {word.definition_en}
                </p>
              {/if}
              {#if word.definition_vi}
                <p class="text-xs text-[var(--text-muted)] font-serif italic">
                  {word.definition_vi}
                </p>
              {/if}
            </div>

            <!-- Bottom Actions -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
              <button
                type="button"
                onclick={handleSaveToVault}
                disabled={isSavedToVault}
                class={`w-full sm:w-auto px-4 py-2.5 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition cursor-pointer ${
                  isSavedToVault
                    ? "bg-emerald-500/15 border-emerald-400/50 text-emerald-700 dark:text-emerald-300"
                    : "bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] border-[var(--border-main)] text-[var(--text-main)] hover:text-[var(--accent-primary)]"
                }`}
              >
                {#if isSavedToVault}
                  <CheckCircle2 class="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                  <span>Saved in Obsidian</span>
                {:else}
                  <Bookmark class="w-4 h-4" />
                  <span>Save to Obsidian Vault</span>
                {/if}
              </button>

              <button
                type="button"
                onclick={initDrill}
                class="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-[var(--border-main)] hover:bg-[var(--accent-primary-light)] text-xs font-semibold text-[var(--text-main)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center justify-center gap-2"
              >
                <RotateCcw class="w-4 h-4" />
                <span>Repeat Drill</span>
              </button>

              <button
                type="button"
                onclick={onClose}
                class="w-full sm:w-auto btn-forest px-5 py-2.5 rounded-xl text-xs font-semibold transition cursor-pointer shadow-sm"
              >
                Done
              </button>
            </div>
          </div>
        {/if}
      </div>

      <!-- Modal Footer with Step Advance -->
      {#if currentStep < 5}
        <div class="px-5 py-3.5 border-t border-[var(--border-main)] bg-[var(--bg-inner)] flex items-center justify-between">
          <span class="text-xs font-mono text-[var(--text-muted)]">
            Score: <strong class="text-[var(--text-main)]">{score}</strong> / 5
          </span>

          <button
            type="button"
            onclick={nextStep}
            disabled={!answeredSteps[currentStep]}
            class="btn-forest px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition shadow-sm cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <span>{currentStep === 4 ? "View Results" : "Next Drill"}</span>
            <ArrowRight class="w-3.5 h-3.5" />
          </button>
        </div>
      {/if}
    </div>
  </div>
{/if}
