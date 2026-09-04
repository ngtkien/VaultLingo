<script lang="ts">
  import { onMount } from "svelte";
  import {
    Search,
    Volume2,
    Bookmark,
    Check,
    Sparkles,
    ExternalLink,
    Trash2,
    RefreshCw,
    BookOpen,
    Lightbulb,
    Tag,
    ArrowRight,
    Compass,
    History,
    Network,
    Quote,
    BrainCircuit,
    Terminal,
    ChevronDown,
    ChevronUp,
    X
  } from "lucide-svelte";
  import {
    lookupSmartDictionary,
    parseExamplePairs,
    type SmartWordResult,
  } from "../utils/smartDictionary";
  import {
    SaveWordToObsidian,
    DeleteWordFromObsidian,
    GetSavedObsidianVocab,
    SearchWordsInDB,
  } from "../../../wailsjs/go/main/App.js";
  import { backend } from "../../../wailsjs/go/models";
  import { BrowserOpenURL } from "../../../wailsjs/runtime/runtime";
  import { playTTS, playAudioUrl } from "../utils/audio";
  import ParagraphTranslator from "../components/ParagraphTranslator.svelte";

  let {
    initialWord = "resilience",
    wordCount = null,
    onWordStored,
  } = $props<{
    initialWord?: string;
    wordCount?: number | null;
    onWordStored?: () => void;
  }>();

  let searchTerm = $state(initialWord || "resilience");
  let currentResult = $state<SmartWordResult | null>(null);
  let isSaved = $state(false);
  let loading = $state(false);
  let logs = $state<string[]>([]);
  let showLogs = $state(false);
  let recentSearches = $state<string[]>([]);
  let autoSuggestions = $state<backend.Word[]>([]);
  let isSearchingSuggest = $state(false);
  let showSuggestions = $state(false);
  let isEnriching = $state(false);
  let activeInsightTab = $state<"nuance" | "memory">("nuance");
  let activeDictionaryMode = $state<"lookup" | "translator">("lookup");

  function openDictionaryLink() {
    const term = currentResult?.word?.word || searchTerm || "";
    const url =
      currentResult?.word?.dict_link ||
      `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(term)}`;
    try {
      BrowserOpenURL(url);
    } catch {
      window.open(url, "_blank");
    }
  }

  async function handleDeepEnrich() {
    if (!currentResult?.word?.word) return;
    const term = currentResult.word.word;
    isEnriching = true;
    showLogs = true;
    try {
      const result = await lookupSmartDictionary(
        term,
        (msg) => {
          logs = [...logs, msg];
        },
        true
      );
      if (result) {
        currentResult = result;
        await checkSavedStatus(result.word.word);
        if (onWordStored) onWordStored();
      }
    } catch (err: any) {
      logs = [...logs, `❌ AI Enrichment failed: ${err?.message || err}`];
    } finally {
      isEnriching = false;
    }
  }

  async function checkSavedStatus(word: string) {
    try {
      const items = await GetSavedObsidianVocab();
      isSaved = items.some(
        (item: any) => item.word.toLowerCase() === word.toLowerCase()
      );
    } catch {
      isSaved = false;
    }
  }

  async function handleSearch(termToSearch?: string) {
    const term = (termToSearch || searchTerm).trim();
    if (!term) return;

    searchTerm = term;
    showSuggestions = false;
    loading = true;
    logs = [];

    if (!recentSearches.includes(term)) {
      recentSearches = [term, ...recentSearches.slice(0, 7)];
      try {
        localStorage.setItem(
          "vaultlingo_recent_searches",
          JSON.stringify(recentSearches)
        );
      } catch {}
    }

    try {
      const result = await lookupSmartDictionary(term, (msg) => {
        logs = [...logs, msg];
      });

      if (result) {
        currentResult = result;
        await checkSavedStatus(result.word.word);
        if (result.source === "ai" && onWordStored) {
          onWordStored();
        }
        if (!result.nuance_tips && result.mnemonic_hook) {
          activeInsightTab = "memory";
        } else {
          activeInsightTab = "nuance";
        }
      }
    } catch (err) {
      logs = [...logs, `❌ Lookup exception: ${err}`];
    } finally {
      loading = false;
    }
  }

  async function handleInput(e: Event) {
    const val = (e.target as HTMLInputElement).value.trim();
    searchTerm = val;
    if (val.length < 2) {
      autoSuggestions = [];
      showSuggestions = false;
      return;
    }

    isSearchingSuggest = true;
    try {
      const hits = await SearchWordsInDB(val, 6);
      autoSuggestions = hits || [];
      showSuggestions = autoSuggestions.length > 0;
    } catch {
      autoSuggestions = [];
    } finally {
      isSearchingSuggest = false;
    }
  }

  async function handleSaveWord() {
    if (!currentResult) return;
    try {
      if (isSaved) {
        await DeleteWordFromObsidian(currentResult.word.word);
        isSaved = false;
      } else {
        const res = await SaveWordToObsidian(currentResult.word);
        if (res.success) {
          isSaved = true;
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  function handlePronounce(slow = false) {
    if (!currentResult) return;
    if (currentResult.audioUrl && !slow) {
      playAudioUrl(currentResult.audioUrl);
    } else {
      playTTS(currentResult.word.word, slow ? 0.75 : 1.0);
    }
  }

  onMount(() => {
    try {
      const stored = localStorage.getItem("vaultlingo_recent_searches");
      if (stored) recentSearches = JSON.parse(stored);
    } catch {}

    if (initialWord) {
      handleSearch(initialWord);
    }
  });
</script>

<div class="w-full max-w-5xl mx-auto space-y-6 pb-12">
  <!-- Mode Switcher: Dictionary Lookup vs AI Paragraph Translator -->
  <div class="flex items-center gap-2 border-b border-[var(--border-main)] pb-3">
    <button
      type="button"
      onclick={() => (activeDictionaryMode = "lookup")}
      class={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition cursor-pointer ${
        activeDictionaryMode === "lookup"
          ? "btn-forest shadow-sm"
          : "bg-[var(--bg-inner)] hover:bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-main)]"
      }`}
    >
      <BookOpen class="w-4 h-4" />
      <span>Dictionary Lookup</span>
    </button>

    <button
      type="button"
      onclick={() => (activeDictionaryMode = "translator")}
      class={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition cursor-pointer ${
        activeDictionaryMode === "translator"
          ? "btn-forest shadow-sm"
          : "bg-[var(--bg-inner)] hover:bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-main)]"
      }`}
    >
      <Sparkles class="w-4 h-4" />
      <span>AI Paragraph Translator</span>
      <span class="px-1.5 py-0.5 rounded-full text-[9px] uppercase font-mono bg-amber-500/20 text-amber-700 dark:text-amber-300 font-bold">New</span>
    </button>
  </div>

  {#if activeDictionaryMode === "translator"}
    <ParagraphTranslator />
  {:else}
  <!-- Search Hero (matches 2.png) -->
  <div class="space-y-4">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-0.5 rounded text-[10px]">
            Lexicon Engine
          </span>
          {#if wordCount}
            <span class="text-xs text-[var(--text-muted)] font-mono">
              • {wordCount.toLocaleString()} words indexed
            </span>
          {/if}
        </div>
        <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)] mt-1">
          Smart Dictionary
        </h1>
        <p class="text-sm font-serif italic text-[var(--text-muted)] mt-1">
          Oxford 6-Block Lexical Architecture with high-speed SQLite lookup and AI synthesis.
        </p>
      </div>

      <!-- Quick SQLite status badge -->
      <div class="px-3 py-1 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] text-xs text-[var(--text-muted)] font-mono flex items-center gap-1.5 self-start sm:self-auto">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span>Local SQLite Ready</span>
      </div>
    </div>

    <!-- Search Input & Suggestions Popup -->
    <div class="relative">
      <div class="relative flex items-center">
        <Search class="w-5 h-5 text-[var(--text-muted)] absolute left-4 pointer-events-none" />
        <input
          type="text"
          bind:value={searchTerm}
          oninput={handleInput}
          onkeydown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Search any English word, collocation, or idiom..."
          class="w-full bg-[var(--bg-card)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-2xl pl-12 pr-28 py-3.5 text-base text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none shadow-sm transition"
        />

        <div class="absolute right-2 flex items-center gap-1.5">
          {#if searchTerm}
            <button
              onclick={() => { searchTerm = ''; autoSuggestions = []; showSuggestions = false; }}
              class="p-1.5 text-[var(--text-muted)] hover:text-[var(--text-main)] transition cursor-pointer"
            >
              <X class="w-4 h-4" />
            </button>
          {/if}

          <button
            onclick={() => handleSearch()}
            disabled={loading}
            class="px-4 py-2 rounded-xl btn-forest text-xs font-semibold flex items-center gap-1.5 transition shadow-sm cursor-pointer disabled:opacity-50"
          >
            {#if loading}
              <RefreshCw class="w-3.5 h-3.5 animate-spin" />
              <span>Looking up...</span>
            {:else}
              <Sparkles class="w-3.5 h-3.5" />
              <span>Explore</span>
            {/if}
          </button>
        </div>
      </div>

      <!-- Auto Suggestions Dropdown -->
      {#if showSuggestions && autoSuggestions.length > 0}
        <div class="absolute left-0 right-0 top-full mt-2 bg-[var(--bg-card)] border border-[var(--border-main)] rounded-2xl shadow-xl z-50 overflow-hidden divide-y divide-[var(--border-main)]">
          {#each autoSuggestions as item}
            <button
              onclick={() => handleSearch(item.word)}
              class="w-full px-4 py-2.5 text-left hover:bg-[var(--accent-primary-light)] transition flex items-center justify-between group cursor-pointer"
            >
              <div class="flex items-center gap-2">
                <span class="font-serif font-bold text-sm text-[var(--text-main)] group-hover:text-[var(--accent-primary)]">
                  {item.word}
                </span>
                <span class="text-xs text-[var(--text-muted)] font-mono">[{item.phonetic}]</span>
                <span class="text-[10px] px-1.5 py-0.5 rounded bg-[var(--bg-inner)] text-[var(--text-subtle)] font-medium">
                  {item.pos}
                </span>
              </div>
              <span class="text-xs text-[var(--text-muted)] truncate max-w-xs font-serif italic">
                {item.definition_vi || item.definition_en}
              </span>
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <!-- Recent Searches Pill Chips -->
    {#if recentSearches.length > 0}
      <div class="flex items-center gap-2 overflow-x-auto pb-1 text-xs text-[var(--text-muted)] no-scrollbar">
        <span class="shrink-0 flex items-center gap-1 font-mono text-[11px]">
          <History class="w-3.5 h-3.5" /> Recent:
        </span>
        {#each recentSearches as word}
          <button
            onclick={() => handleSearch(word)}
            class="px-2.5 py-1 rounded-lg bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] transition cursor-pointer shrink-0 font-medium"
          >
            {word}
          </button>
        {/each}
      </div>
    {/if}
  </div>

  <!-- Word Result Card (matches 2.png) -->
  {#if currentResult}
    <article class="journal-card p-6 sm:p-8 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-6">
      <!-- Word Header: Title, Phonetic, POS, Audio, Actions -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-[var(--border-main)]">
        <div>
          <div class="flex items-baseline gap-3 flex-wrap">
            <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)]">
              {currentResult.word.word}
            </h1>
            <span class="text-sm font-mono text-[var(--text-muted)]">
              [{currentResult.word.phonetic || "/.../"}]
            </span>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[var(--accent-primary-light)] text-[var(--accent-primary)] border border-[var(--accent-primary-border)]">
              {currentResult.word.pos || "noun"}
            </span>

            <!-- Source Badge -->
            <span class="px-2 py-0.5 rounded text-[10px] font-mono uppercase font-bold tracking-wider bg-[var(--bg-inner)] text-[var(--text-subtle)] border border-[var(--border-main)]">
              {currentResult.source === 'lexicon' ? 'SQLite Fast Cache' : currentResult.source.toUpperCase()}
            </span>
          </div>

          {#if currentResult.word.topic_title}
            <div class="text-xs text-[var(--text-subtle)] mt-1 font-medium">
              Topic: {currentResult.word.topic_title}
            </div>
          {/if}
        </div>

        <!-- Action Toolbar: Cohesive Editorial Journal Controls -->
        <div class="flex items-center gap-2 shrink-0 flex-wrap">
          <!-- Audio Speed Segmented Group -->
          <div class="inline-flex items-center rounded-xl border border-[var(--border-main)] bg-[var(--bg-inner)] overflow-hidden divide-x divide-[var(--border-main)] shadow-sm">
            <button
              onclick={() => handlePronounce(false)}
              class="px-2.5 py-1.5 flex items-center gap-1.5 text-xs text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] hover:text-[var(--accent-primary)] transition cursor-pointer"
              title="Pronounce at standard speed (1.0x)"
            >
              <Volume2 class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              <span class="font-mono font-medium">1.0x</span>
            </button>
            <button
              onclick={() => handlePronounce(true)}
              class="px-2 py-1.5 text-xs font-mono text-[var(--text-muted)] hover:bg-[var(--accent-primary-light)] hover:text-[var(--accent-primary)] transition cursor-pointer"
              title="Pronounce slowly (0.75x)"
            >
              0.75x
            </button>
          </div>

          <!-- AI Enrich Button (Editorial Forest/Sage Theme) -->
          <button
            onclick={handleDeepEnrich}
            disabled={isEnriching || loading}
            class="px-3 py-1.5 rounded-xl border border-[var(--border-main)] hover:border-[var(--accent-primary-border)] bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center gap-1.5 text-xs font-medium shadow-sm active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Deep AI analysis: 6-block breakdown, collocations, nuances, roots & examples"
          >
            {#if isEnriching}
              <RefreshCw class="w-3.5 h-3.5 animate-spin text-[var(--accent-primary)]" />
              <span>Enriching...</span>
            {:else}
              <Sparkles class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              <span>{currentResult.source === "ai" ? "AI Re-enrich" : "AI Enrich"}</span>
            {/if}
          </button>

          <!-- External Cambridge Dictionary Link -->
          <button
            type="button"
            onclick={openDictionaryLink}
            class="px-2.5 py-1.5 rounded-xl border border-[var(--border-main)] hover:border-[var(--border-highlight)] bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center gap-1.5 text-xs font-medium shadow-sm active:scale-95"
            title="Open Cambridge Dictionary in system browser"
          >
            <ExternalLink class="w-3.5 h-3.5" />
            <span class="hidden sm:inline">Cambridge</span>
          </button>

          <!-- Save to Obsidian Button -->
          <button
            onclick={handleSaveWord}
            class={`px-3.5 py-1.5 rounded-xl transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold border shadow-sm ${
              isSaved
                ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-400/40"
                : "btn-forest"
            }`}
          >
            {#if isSaved}
              <Check class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span>Saved in Vault</span>
            {:else}
              <Bookmark class="w-3.5 h-3.5" />
              <span>Save to Obsidian</span>
            {/if}
          </button>
        </div>
      </div>

      <!-- 2-Column Definition Grid: English & Vietnamese (matches 2.png) -->
      <div class="grid md:grid-cols-2 gap-4">
        <!-- English Definition -->
        <div class="p-4.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[var(--accent-primary)]"></span>
            <span class="journal-badge text-[var(--text-subtle)] font-bold">English Definition</span>
          </div>
          <p class="text-sm font-medium text-[var(--text-main)] leading-relaxed">
            {currentResult.word.definition_en}
          </p>
        </div>

        <!-- Vietnamese Definition -->
        <div class="p-4.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span class="journal-badge text-[var(--text-subtle)] font-bold">Vietnamese Translation</span>
          </div>
          <p class="text-sm font-serif italic text-[var(--text-main)] leading-relaxed">
            {currentResult.word.definition_vi || "No Vietnamese definition available."}
          </p>
        </div>
      </div>

      <!-- Word Family & Roots (matches 2.png) -->
      {#if currentResult.word_family && currentResult.word_family.length > 0}
        <div class="p-4.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2.5">
          <div class="text-xs font-bold text-[var(--text-subtle)] flex items-center gap-1.5 uppercase tracking-wider">
            <Network class="w-4 h-4 text-[var(--accent-primary)]" />
            <span>Word Family & Morphological Derivatives</span>
          </div>
          <div class="flex flex-wrap gap-2">
            {#each currentResult.word_family as wf}
              <div class="px-3 py-1.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-main)] flex items-center gap-2 text-xs">
                <span class="px-1.5 py-0.5 rounded text-[10px] uppercase font-mono bg-[var(--bg-inner)] text-[var(--text-subtle)]">
                  {wf.pos}
                </span>
                <button
                  onclick={() => handleSearch(wf.word)}
                  class="font-serif font-bold text-[var(--text-main)] hover:text-[var(--accent-primary)] transition cursor-pointer"
                >
                  {wf.word}
                </button>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- Etymology & Origins -->
      {#if currentResult.etymology}
        <div class="p-4.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
          <div class="text-xs font-bold text-[var(--text-subtle)] flex items-center gap-1.5 uppercase tracking-wider">
            <Compass class="w-4 h-4 text-[var(--accent-primary)]" />
            <span>Etymology & Historical Roots</span>
          </div>
          <p class="text-xs text-[var(--text-muted)] font-serif italic leading-relaxed">
            {currentResult.etymology}
          </p>
        </div>
      {/if}

      <!-- Real-World Contextual Examples (Split & formatted like image 3) -->
      <div class="p-4.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-3">
        <div class="text-xs font-bold text-[var(--text-subtle)] flex items-center gap-1.5 uppercase tracking-wider">
          <Quote class="w-4 h-4 text-[var(--accent-primary)]" />
          <span>Real-World Contextual Examples</span>
        </div>

        <div class="space-y-2.5">
          {#if currentResult.examples && currentResult.examples.length > 0}
            {#each currentResult.examples as ex}
              <div class="pl-3.5 border-l-2 border-[var(--accent-primary)] space-y-0.5">
                <p class="text-sm text-[var(--text-main)] font-serif italic leading-relaxed">
                  “{ex.en}”
                </p>
                {#if ex.vi}
                  <p class="text-xs text-[var(--text-muted)]">
                    👉 {ex.vi}
                  </p>
                {/if}
              </div>
            {/each}
          {:else if currentResult.word.example_en}
            {@const fallbackExamples = parseExamplePairs(currentResult.word.example_en, currentResult.word.example_vi)}
            {#each fallbackExamples as ex}
              <div class="pl-3.5 border-l-2 border-[var(--accent-primary)] space-y-0.5">
                <p class="text-sm text-[var(--text-main)] font-serif italic leading-relaxed">
                  “{ex.en}”
                </p>
                {#if ex.vi}
                  <p class="text-xs text-[var(--text-muted)]">
                    👉 {ex.vi}
                  </p>
                {/if}
              </div>
            {/each}
          {/if}
        </div>
      </div>

      <!-- Synonyms, Antonyms & High-Yield Collocations -->
      {#if (currentResult.synonyms && currentResult.synonyms.length > 0) || (currentResult.antonyms && currentResult.antonyms.length > 0) || (currentResult.collocations && currentResult.collocations.length > 0)}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Synonyms -->
          {#if currentResult.synonyms && currentResult.synonyms.length > 0}
            <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
              <span class="journal-badge text-[var(--text-subtle)]">Synonyms (Click to explore)</span>
              <div class="flex flex-wrap gap-1.5">
                {#each currentResult.synonyms as syn}
                  <button
                    onclick={() => handleSearch(syn)}
                    class="px-2 py-0.5 text-xs bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] border border-[var(--border-main)] rounded-md transition cursor-pointer"
                  >
                    {syn}
                  </button>
                {/each}
              </div>
            </div>
          {/if}

          <!-- Antonyms -->
          {#if currentResult.antonyms && currentResult.antonyms.length > 0}
            <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
              <span class="journal-badge text-[var(--text-subtle)]">Antonyms</span>
              <div class="flex flex-wrap gap-1.5">
                {#each currentResult.antonyms as ant}
                  <button
                    onclick={() => handleSearch(ant)}
                    class="px-2 py-0.5 text-xs bg-[var(--bg-card)] hover:bg-red-500/10 text-[var(--text-muted)] hover:text-red-700 border border-[var(--border-main)] rounded-md transition cursor-pointer"
                  >
                    {ant}
                  </button>
                {/each}
              </div>
            </div>
          {/if}

          <!-- Collocations -->
          {#if currentResult.collocations && currentResult.collocations.length > 0}
            <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
              <span class="journal-badge text-[var(--text-subtle)]">High-Yield Collocations</span>
              <div class="flex flex-wrap gap-1.5">
                {#each currentResult.collocations as col}
                  <span class="px-2 py-0.5 text-xs bg-[var(--bg-card)] text-[var(--text-main)] border border-[var(--border-main)] rounded-md font-medium">
                    {col}
                  </span>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      {/if}

      <!-- Linguistic Insights: Usage Nuances & Memory Hook (2 Separate Tabs) -->
      {#if currentResult.nuance_tips || currentResult.mnemonic_hook}
        <div class="rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] p-4 space-y-3">
          <!-- Tab Header -->
          <div class="flex items-center justify-between border-b border-[var(--border-main)] pb-2.5">
            <div class="flex items-center gap-1.5">
              <!-- Tab 1: Usage & Nuance -->
              <button
                type="button"
                onclick={() => (activeInsightTab = "nuance")}
                class={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer ${
                  activeInsightTab === "nuance"
                    ? "bg-amber-500/15 text-amber-800 dark:text-amber-300 border border-amber-500/30 shadow-2xs font-bold"
                    : "text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card)]"
                }`}
              >
                <Lightbulb class="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                <span>Usage & IELTS Nuance</span>
                {#if currentResult.nuance_tips}
                  <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                {/if}
              </button>

              <!-- Tab 2: Memory Hook -->
              <button
                type="button"
                onclick={() => (activeInsightTab = "memory")}
                class={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer ${
                  activeInsightTab === "memory"
                    ? "bg-amber-500/15 text-amber-800 dark:text-amber-300 border border-amber-500/30 shadow-2xs font-bold"
                    : "text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card)]"
                }`}
              >
                <BrainCircuit class="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                <span>Memory Hook (Mnemonic)</span>
                {#if currentResult.mnemonic_hook}
                  <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                {/if}
              </button>
            </div>

            <span class="text-[10px] uppercase font-mono tracking-wider text-[var(--text-subtle)] font-bold hidden sm:inline">
              Linguistic Insights
            </span>
          </div>

          <!-- Tab Content Body -->
          <div class="pt-1">
            {#if activeInsightTab === "nuance"}
              {#if currentResult.nuance_tips}
                <div class="text-xs text-[var(--text-main)] leading-relaxed font-sans flex items-start gap-2.5">
                  <span class="p-1 rounded-md bg-amber-500/10 text-amber-600 dark:text-amber-400 shrink-0">
                    <Lightbulb class="w-3.5 h-3.5" />
                  </span>
                  <p class="leading-relaxed flex-1">{currentResult.nuance_tips}</p>
                </div>
              {:else}
                <p class="text-xs text-[var(--text-muted)] italic">
                  No specific usage nuance recorded for this word yet. Click "AI Enrich" to synthesize IELTS tips.
                </p>
              {/if}
            {:else if activeInsightTab === "memory"}
              {#if currentResult.mnemonic_hook}
                <div class="text-xs text-[var(--text-main)] leading-relaxed font-sans flex items-start gap-2.5">
                  <span class="p-1 rounded-md bg-amber-500/10 text-amber-600 dark:text-amber-400 shrink-0">
                    <BrainCircuit class="w-3.5 h-3.5" />
                  </span>
                  <p class="leading-relaxed flex-1 font-medium text-[var(--text-main)]">{currentResult.mnemonic_hook}</p>
                </div>
              {:else}
                <p class="text-xs text-[var(--text-muted)] italic">
                  No memory hook recorded yet. Click "AI Enrich" to generate a vivid mnemonic association.
                </p>
              {/if}
            {/if}
          </div>
        </div>
      {/if}

      <!-- SQLite & AI Execution Pipeline Log (Expandable) -->
      <div class="pt-4 border-t border-[var(--border-main)]">
        <button
          onclick={() => showLogs = !showLogs}
          class="text-xs text-[var(--text-muted)] hover:text-[var(--text-main)] flex items-center gap-1.5 font-mono cursor-pointer"
        >
          <Terminal class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
          <span>Execution Pipeline Trace ({currentResult.executionTimeMs || 4}ms)</span>
          {#if showLogs}
            <ChevronUp class="w-3.5 h-3.5" />
          {:else}
            <ChevronDown class="w-3.5 h-3.5" />
          {/if}
        </button>

        {#if showLogs && currentResult.debugLogs && currentResult.debugLogs.length > 0}
          <div class="mt-3 p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] font-mono text-[11px] text-[var(--text-muted)] space-y-1 overflow-x-auto">
            {#each currentResult.debugLogs as logLine}
              <div class="leading-relaxed">{logLine}</div>
            {/each}
          </div>
        {/if}
      </div>
    </article>
  {/if}
  {/if}
</div>
