<script lang="ts">
  import {
    ArrowLeftRight,
    Languages,
    Sparkles,
    Volume2,
    Copy,
    Check,
    Bookmark,
    Trash2,
    RefreshCw,
    Lightbulb,
    FileText,
    CheckCircle2,
    Plus,
    BookOpen
  } from "lucide-svelte";
  import {
    TranslateParagraph,
    SaveTranslationToObsidian,
    SaveWordToDB
  } from "../../../wailsjs/go/main/App.js";
  import { backend } from "../../../wailsjs/go/models";
  import { playTTS } from "../utils/audio";

  let sourceText = $state("");
  let sourceLang = $state<"English" | "Vietnamese">("English");
  let targetLang = $state<"English" | "Vietnamese">("Vietnamese");
  let tone = $state("Editorial & Journalistic");
  
  let isTranslating = $state(false);
  let translationResult = $state<backend.TranslationResult | null>(null);
  let errorMsg = $state("");
  let isCopied = $state(false);
  let isSavedToObsidian = $state(false);
  let savedWords = $state<Record<string, boolean>>({});

  const toneOptions = [
    { label: "Editorial & Journalistic", desc: "Sharp, journalistic publication style" },
    { label: "Natural & Conversational", desc: "Everyday authentic spoken English" },
    { label: "Academic & Formal (IELTS)", desc: "Advanced lexicon, formal syntax" },
    { label: "Literal & Faithful", desc: "Direct structural alignment" }
  ];

  const sampleSnippets = [
    {
      title: "Psychological Resilience",
      lang: "English" as const,
      target: "Vietnamese" as const,
      text: "Resilience is not merely passive endurance under adversity, but an active adaptation process that allows individuals and communities to bounce back to health and equilibrium."
    },
    {
      title: "The Power of Self-Discipline",
      lang: "Vietnamese" as const,
      target: "English" as const,
      text: "Kỷ luật bản thân không phải là sự gò bó hay trừng phạt, mà là cây cầu nối vững chắc nhất giữa ước mơ trừu tượng và thành tựu thực tế."
    },
    {
      title: "IELTS Writing Task 2 Focus",
      lang: "English" as const,
      target: "Vietnamese" as const,
      text: "While technological proliferation undoubtedly enhances workforce productivity, it concurrently precipitates socioeconomic disparities that necessitate robust policy interventions."
    }
  ];

  function swapLanguages() {
    const tempLang = sourceLang;
    sourceLang = targetLang;
    targetLang = tempLang;

    // Swap text if translation already exists
    if (translationResult?.translated_text) {
      const oldTargetText = translationResult.translated_text;
      translationResult = null;
      sourceText = oldTargetText;
    }
  }

  function applySnippet(snippet: typeof sampleSnippets[0]) {
    sourceLang = snippet.lang;
    targetLang = snippet.target;
    sourceText = snippet.text;
    translationResult = null;
    errorMsg = "";
  }

  async function handleTranslate() {
    if (!sourceText.trim()) return;

    isTranslating = true;
    errorMsg = "";
    isSavedToObsidian = false;

    try {
      const res = await TranslateParagraph(sourceText.trim(), sourceLang, targetLang, tone);
      translationResult = res;
    } catch (err: any) {
      errorMsg = err?.toString() || "AI translation encountered an issue. Please try again.";
    } finally {
      isTranslating = false;
    }
  }

  async function handleCopy() {
    if (!translationResult?.translated_text) return;
    try {
      await navigator.clipboard.writeText(translationResult.translated_text);
      isCopied = true;
      setTimeout(() => (isCopied = false), 2000);
    } catch {
      // Fallback
    }
  }

  async function handleSaveToObsidian() {
    if (!translationResult?.translated_text || !sourceText.trim()) return;

    try {
      await SaveTranslationToObsidian(
        sourceText.trim(),
        translationResult.translated_text,
        sourceLang,
        targetLang,
        tone,
        translationResult.key_vocabulary || []
      );
      isSavedToObsidian = true;
    } catch (err) {
      console.error("Failed to save translation to Obsidian:", err);
    }
  }

  function handlePlayAudio() {
    // Play English portion
    const englishText = sourceLang === "English" ? sourceText : translationResult?.translated_text;
    if (englishText) {
      playTTS(englishText.trim(), 1.0);
    }
  }

  async function handleSaveWordToVocab(vocab: backend.ExtractedVocab) {
    try {
      const wordObj: backend.Word = {
        id: 0,
        word: vocab.word,
        raw_word: vocab.word,
        pos: vocab.pos || "word",
        phonetic: vocab.phonetic || "",
        definition_en: sourceLang === "English" ? vocab.meaning : vocab.word,
        definition_vi: sourceLang === "English" ? vocab.meaning : vocab.meaning,
        example_en: sourceLang === "English" ? sourceText.slice(0, 120) + "..." : translationResult?.translated_text?.slice(0, 120) + "..." || "",
        example_vi: sourceLang === "Vietnamese" ? sourceText.slice(0, 120) + "..." : translationResult?.translated_text?.slice(0, 120) + "..." || "",
        level: "B2",
        topic: "ai_translation",
        topic_title: "AI Translation",
        topic_icon: "✍️",
        dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(vocab.word)}`
      };

      await SaveWordToDB(wordObj);
      savedWords = { ...savedWords, [vocab.word]: true };
    } catch (err) {
      console.error("Failed to save vocab into database:", err);
    }
  }
</script>

<div class="space-y-6">
  <!-- Header / Subtitle & Tone Selector -->
  <div class="journal-card p-5 space-y-4">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[var(--border-main)] pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="p-1.5 rounded-lg bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
            <Languages class="w-4 h-4" />
          </span>
          <h2 class="font-serif text-lg font-bold text-[var(--text-main)]">AI Paragraph Translator</h2>
          <span class="journal-badge text-xs font-mono">Bilingual Engine</span>
        </div>
        <p class="text-xs text-[var(--text-muted)] mt-1 font-sans">
          Deep contextual translation with grammatical breakdowns and Obsidian vocabulary extraction.
        </p>
      </div>

      <!-- Tone Style Selector -->
      <div class="flex items-center gap-2">
        <span class="text-xs font-medium text-[var(--text-subtle)] font-mono uppercase tracking-wider hidden sm:inline">Tone:</span>
        <select
          bind:value={tone}
          class="journal-input text-xs py-1.5 px-3 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-[var(--text-main)] font-medium cursor-pointer focus:border-[var(--accent-primary)] focus:outline-none"
        >
          {#each toneOptions as opt}
            <option value={opt.label}>{opt.label}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Quick Sample Snippets -->
    <div class="flex flex-wrap items-center gap-2 pt-1">
      <span class="text-[11px] font-mono text-[var(--text-subtle)] uppercase tracking-wider">Samples:</span>
      {#each sampleSnippets as snip}
        <button
          type="button"
          onclick={() => applySnippet(snip)}
          class="px-2.5 py-1 rounded-md text-xs bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] hover:text-[var(--accent-primary)] text-[var(--text-muted)] border border-[var(--border-main)] transition cursor-pointer"
        >
          {snip.title} ({snip.lang === "English" ? "EN ➔ VI" : "VI ➔ EN"})
        </button>
      {/each}
    </div>
  </div>

  <!-- Translation Workspace (2-Column Split View) -->
  <div class="grid lg:grid-cols-2 gap-4">
    <!-- Source Column -->
    <div class="journal-card p-4.5 space-y-3 flex flex-col justify-between">
      <div class="space-y-3">
        <!-- Source Header -->
        <div class="flex items-center justify-between border-b border-[var(--border-main)] pb-2.5">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[var(--accent-primary)]"></span>
            <span class="text-xs font-bold text-[var(--text-main)] uppercase tracking-wider font-mono">
              Source Text ({sourceLang})
            </span>
          </div>

          <div class="flex items-center gap-2">
            <!-- Swap Button -->
            <button
              type="button"
              onclick={swapLanguages}
              class="p-1.5 rounded-lg text-xs bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] transition cursor-pointer flex items-center justify-center active:scale-95 shadow-2xs"
              title="Swap source and target languages"
            >
              <ArrowLeftRight class="w-3.5 h-3.5" />
            </button>

            <!-- Clear Button -->
            {#if sourceText}
              <button
                type="button"
                onclick={() => { sourceText = ""; translationResult = null; errorMsg = ""; }}
                class="px-1.5 py-1 rounded-md text-xs text-[var(--text-muted)] hover:text-red-600 hover:bg-red-500/10 transition cursor-pointer"
                title="Clear text"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            {/if}
          </div>
        </div>

        <!-- Source Textarea -->
        <textarea
          bind:value={sourceText}
          rows="7"
          placeholder={sourceLang === "English" 
            ? "Enter or paste English text/paragraph here..." 
            : "Enter or paste Vietnamese text/paragraph here..."}
          class="w-full bg-transparent border-0 focus:outline-none resize-none text-sm text-[var(--text-main)] font-sans leading-relaxed placeholder:text-[var(--text-muted)] placeholder:italic"
        ></textarea>
      </div>

      <!-- Source Footer -->
      <div class="pt-3 border-t border-[var(--border-main)] flex items-center justify-between text-xs text-[var(--text-subtle)]">
        <span class="font-mono">{sourceText.length} characters</span>

        <!-- Action Button -->
        <button
          type="button"
          onclick={handleTranslate}
          disabled={isTranslating || !sourceText.trim()}
          class="btn-forest px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 shadow-sm transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {#if isTranslating}
            <RefreshCw class="w-3.5 h-3.5 animate-spin" />
            <span>Translating...</span>
          {:else}
            <Sparkles class="w-3.5 h-3.5" />
            <span>Translate Paragraph ✨</span>
          {/if}
        </button>
      </div>
    </div>

    <!-- Target / Result Column -->
    <div class="journal-card p-4.5 space-y-3 flex flex-col justify-between">
      <div class="space-y-3">
        <!-- Target Header -->
        <div class="flex items-center justify-between border-b border-[var(--border-main)] pb-2.5">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span class="text-xs font-bold text-[var(--text-main)] uppercase tracking-wider font-mono">
              Target Translation ({targetLang})
            </span>
          </div>

          <!-- Target Tools -->
          <div class="flex items-center gap-1.5">
            <!-- Audio Playback Button (for English) -->
            {#if (sourceLang === "English" && sourceText) || (targetLang === "English" && translationResult?.translated_text)}
              <button
                type="button"
                onclick={handlePlayAudio}
                class="px-2 py-1 rounded-md text-xs bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] transition cursor-pointer flex items-center gap-1"
                title="Listen to authentic English pronunciation"
              >
                <Volume2 class="w-3 h-3" />
                <span class="text-[11px] hidden sm:inline">Listen</span>
              </button>
            {/if}

            <!-- Copy Button -->
            {#if translationResult?.translated_text}
              <button
                type="button"
                onclick={handleCopy}
                class="px-2 py-1 rounded-md text-xs bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] transition cursor-pointer flex items-center gap-1"
                title="Copy translation"
              >
                {#if isCopied}
                  <Check class="w-3 h-3 text-emerald-600" />
                  <span class="text-[11px] text-emerald-600">Copied</span>
                {:else}
                  <Copy class="w-3 h-3" />
                  <span class="text-[11px]">Copy</span>
                {/if}
              </button>

              <!-- Save to Obsidian Button -->
              <button
                type="button"
                onclick={handleSaveToObsidian}
                disabled={isSavedToObsidian}
                class={`px-2 py-1 rounded-md text-xs border transition cursor-pointer flex items-center gap-1 ${
                  isSavedToObsidian
                    ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-400/40"
                    : "bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] border-[var(--border-main)]"
                }`}
                title="Save translation & vocabulary to Obsidian"
              >
                {#if isSavedToObsidian}
                  <CheckCircle2 class="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
                  <span class="text-[11px]">Saved to Vault</span>
                {:else}
                  <Bookmark class="w-3 h-3" />
                  <span class="text-[11px]">Save to Vault</span>
                {/if}
              </button>
            {/if}
          </div>
        </div>

        <!-- Target Text Body -->
        {#if isTranslating}
          <div class="py-10 flex flex-col items-center justify-center space-y-3 text-[var(--text-muted)]">
            <RefreshCw class="w-6 h-6 animate-spin text-[var(--accent-primary)]" />
            <p class="text-xs font-serif italic">AI is analyzing linguistic context and composing translation...</p>
          </div>
        {:else if errorMsg}
          <div class="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-xs text-red-600 dark:text-red-400">
            {errorMsg}
          </div>
        {:else if translationResult?.translated_text}
          <div class="text-sm font-medium text-[var(--text-main)] leading-relaxed font-sans min-h-[140px] whitespace-pre-line select-text">
            {translationResult.translated_text}
          </div>
        {:else}
          <div class="py-12 flex flex-col items-center justify-center space-y-2 text-[var(--text-muted)] opacity-60">
            <FileText class="w-8 h-8 stroke-[1.25]" />
            <p class="text-xs font-serif italic">Translation output and linguistic analysis will appear here.</p>
          </div>
        {/if}
      </div>

      <!-- Target Footer -->
      <div class="pt-3 border-t border-[var(--border-main)] flex items-center justify-between text-xs text-[var(--text-subtle)]">
        <span class="font-mono">
          {translationResult?.translated_text ? `${translationResult.translated_text.length} characters` : "Ready"}
        </span>
        <span class="font-mono text-[11px] italic text-[var(--text-muted)]">{tone}</span>
      </div>
    </div>
  </div>

  <!-- Linguistic Insights: Extracted Vocab & Grammar Nuances (Shows after translation) -->
  {#if translationResult && ((translationResult.key_vocabulary && translationResult.key_vocabulary.length > 0) || (translationResult.nuance_notes && translationResult.nuance_notes.length > 0))}
    <div class="journal-card p-5 space-y-4">
      <div class="flex items-center justify-between border-b border-[var(--border-main)] pb-3">
        <div class="flex items-center gap-2">
          <span class="p-1 rounded-md bg-amber-500/10 text-amber-600 dark:text-amber-400">
            <Lightbulb class="w-4 h-4" />
          </span>
          <h3 class="font-serif text-sm font-bold text-[var(--text-main)]">Linguistic Breakdown & Extracted Lexicon</h3>
        </div>
        <span class="text-[10px] font-mono uppercase text-[var(--text-subtle)] tracking-wider">Deep Analysis</span>
      </div>

      <!-- Key Vocabulary Grid -->
      {#if translationResult.key_vocabulary && translationResult.key_vocabulary.length > 0}
        <div class="space-y-2">
          <div class="flex items-center gap-1.5 text-xs font-bold text-[var(--text-subtle)] uppercase tracking-wider font-mono">
            <BookOpen class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
            <span>Key Extracted Lexicon & Collocations:</span>
          </div>

          <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-2.5 pt-1">
            {#each translationResult.key_vocabulary as vocab}
              <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-col justify-between space-y-2 hover:border-[var(--accent-primary-border)] transition">
                <div>
                  <div class="flex items-center justify-between gap-1.5">
                    <span class="font-serif font-bold text-sm text-[var(--text-main)]">{vocab.word}</span>
                    {#if vocab.pos}
                      <span class="px-1.5 py-0.5 rounded text-[10px] uppercase font-mono bg-[var(--bg-card)] text-[var(--text-subtle)]">
                        {vocab.pos}
                      </span>
                    {/if}
                  </div>
                  {#if vocab.phonetic}
                    <div class="text-[11px] font-mono text-[var(--accent-primary)]">{vocab.phonetic}</div>
                  {/if}
                  <p class="text-xs text-[var(--text-muted)] mt-1 line-clamp-2">{vocab.meaning}</p>
                </div>

                <div class="pt-1.5 border-t border-[var(--border-main)] flex items-center justify-end">
                  <button
                    type="button"
                    onclick={() => handleSaveWordToVocab(vocab)}
                    disabled={savedWords[vocab.word]}
                    class={`px-2 py-0.5 rounded-md text-[11px] font-medium transition cursor-pointer flex items-center gap-1 ${
                      savedWords[vocab.word]
                        ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300"
                        : "hover:bg-[var(--accent-primary-light)] text-[var(--accent-primary)] hover:underline"
                    }`}
                  >
                    {#if savedWords[vocab.word]}
                      <Check class="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
                      <span>Saved</span>
                    {:else}
                      <Plus class="w-3 h-3" />
                      <span>Save Word</span>
                    {/if}
                  </button>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- Nuance & Grammar Notes -->
      {#if translationResult.nuance_notes && translationResult.nuance_notes.length > 0}
        <div class="space-y-2 pt-2 border-t border-[var(--border-main)]">
          <div class="text-xs font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
            <Lightbulb class="w-3.5 h-3.5" />
            <span>Grammar Notes & Semantic Nuances:</span>
          </div>
          <ul class="space-y-1.5 text-xs text-[var(--text-main)] font-sans leading-relaxed list-disc list-inside">
            {#each translationResult.nuance_notes as note}
              <li class="pl-1">{note}</li>
            {/each}
          </ul>
        </div>
      {/if}
    </div>
  {/if}
</div>
