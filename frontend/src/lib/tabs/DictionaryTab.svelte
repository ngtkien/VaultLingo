<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    Search, 
    Volume2, 
    Bookmark, 
    Check, 
    Sparkles, 
    ExternalLink, 
    FolderSync, 
    Trash2, 
    RefreshCw, 
    BookOpen, 
    Lightbulb, 
    Tag, 
    Layers, 
    ArrowRight,
    Compass,
    History,
    Network,
    Quote,
    BrainCircuit,
    Terminal,
    ChevronDown,
    ChevronUp
  } from 'lucide-svelte';
  import { lookupSmartDictionary, type SmartWordResult } from '../utils/smartDictionary';
  import { SaveWordToObsidian, DeleteWordFromObsidian, GetSavedObsidianVocab, SearchWordsInDB } from '../../../wailsjs/go/main/App.js';
  import { backend } from '../../../wailsjs/go/models';
  import { playTTS, playAudioUrl } from '../utils/audio';

  let { initialWord = 'serendipity' } = $props<{ initialWord?: string }>();

  let searchQuery = $state('');
  let loading = $state(false);
  let errorMsg = $state('');
  let currentResult = $state<SmartWordResult | null>(null);
  let isSavedInVault = $state(false);
  let savingVault = $state(false);
  let showDebugLogs = $state(false);

  // Live SQLite Autocomplete Suggestions
  let suggestions = $state<backend.Word[]>([]);
  let showSuggestions = $state(false);
  let searchTimer: any = null;

  function handleInputChange(e: Event) {
    const val = (e.target as HTMLInputElement).value;
    searchQuery = val;
    clearTimeout(searchTimer);

    if (!val || val.trim().length < 2) {
      suggestions = [];
      showSuggestions = false;
      return;
    }

    searchTimer = setTimeout(async () => {
      try {
        const matches = await SearchWordsInDB(val.trim(), 8);
        suggestions = matches || [];
        showSuggestions = suggestions.length > 0;
      } catch (err) {
        suggestions = [];
      }
    }, 150);
  }

  const POPULAR_WORDS = [
    { word: 'resilience', tag: 'C1 • Grit' },
    { word: 'serendipity', tag: 'C2 • Luck' },
    { word: 'ephemeral', tag: 'C2 • Time' },
    { word: 'ubiquitous', tag: 'C1 • Tech' },
    { word: 'eloquent', tag: 'B2 • Speech' },
    { word: 'pragmatic', tag: 'C1 • Mindset' },
    { word: 'procrastinate', tag: 'B2 • Habit' }
  ];

  async function checkSavedStatus(wordName: string) {
    try {
      const savedItems = await GetSavedObsidianVocab();
      if (savedItems && savedItems.length > 0) {
        const found = savedItems.some(
          (item) => item.word.toLowerCase() === wordName.toLowerCase()
        );
        isSavedInVault = found;
        return;
      }
    } catch (e) {
      console.warn('Could not verify vault status:', e);
    }
    isSavedInVault = false;
  }

  export async function handleSearch(targetWord?: string) {
    const term = (targetWord || searchQuery).trim();
    if (!term) return;

    searchQuery = term;
    loading = true;
    errorMsg = '';

    try {
      const result = await lookupSmartDictionary(term);
      currentResult = result;
      await checkSavedStatus(result.word.word);
    } catch (err: any) {
      console.error('Dictionary search error:', err);
      errorMsg = err?.message || 'Word not found or error looking up word.';
      currentResult = null;
    } finally {
      loading = false;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }

  async function handleDeepEnrich() {
    if (!currentResult?.word?.word) return;
    const term = currentResult.word.word;
    loading = true;
    errorMsg = '';
    try {
      const result = await lookupSmartDictionary(term, true);
      currentResult = result;
      await checkSavedStatus(result.word.word);
    } catch (err: any) {
      console.error('Deep enrich error:', err);
      errorMsg = 'Could not enrich with AI: ' + (err?.message || 'AI timeout');
    } finally {
      loading = false;
    }
  }

  async function toggleSaveToVault() {
    if (!currentResult?.word) return;
    savingVault = true;

    try {
      if (isSavedInVault) {
        await DeleteWordFromObsidian(currentResult.word.word);
        isSavedInVault = false;
      } else {
        const res = await SaveWordToObsidian(currentResult.word);
        if (res.success) {
          isSavedInVault = true;
        } else {
          errorMsg = res.error || 'Failed to save to Obsidian Vault';
        }
      }
    } catch (err: any) {
      console.error('Vault toggle error:', err);
      errorMsg = err?.message || 'Error saving to Obsidian';
    } finally {
      savingVault = false;
    }
  }

  function handlePlayAudio(slow = false) {
    if (!currentResult?.word) return;

    if (currentResult.audioUrl && !slow) {
      playAudioUrl(currentResult.audioUrl, 1.0, currentResult.word.word);
    } else {
      playTTS(currentResult.word.word, slow ? 0.75 : 1.0, currentResult.word.word);
    }
  }

  let lastLoadedInitialWord = $state('');

  // React to initialWord changes ONLY when initialWord prop changes from outside
  $effect(() => {
    const target = initialWord?.trim() || '';
    if (target && target !== lastLoadedInitialWord) {
      lastLoadedInitialWord = target;
      searchQuery = target;
      handleSearch(target);
    }
  });
</script>

<div class="space-y-6 pb-12">
  <!-- Dictionary Search Header -->
  <div class="relative bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-md theme-card">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="text-2xl">📖</span>
          <h2 class="text-2xl sm:text-3xl font-bold tracking-tight bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">
            Smart Dictionary & Lexicon Search
          </h2>
        </div>
        <p class="text-xs sm:text-sm text-slate-400 theme-text-muted mt-1">
          Search any English word • In-depth linguistic insights • One-click sync to Obsidian
        </p>
      </div>

      <div class="flex items-center gap-2">
        <span class="px-3 py-1 text-xs font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30 rounded-xl">
          ⚡ Comprehensive Lexicon
        </span>
      </div>
    </div>

    <!-- Search Bar with Live SQLite Search Engine Suggestions -->
    <div class="mt-5 flex flex-col sm:flex-row items-stretch gap-3 relative">
      <div class="relative flex-1">
        <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <Search class="w-5 h-5" />
        </div>
        <input
          type="text"
          value={searchQuery}
          oninput={handleInputChange}
          onkeydown={handleKeydown}
          onfocus={() => { if (suggestions.length > 0) showSuggestions = true; }}
          placeholder="Type any English word (e.g., architecture, environment, serendipity...)"
          class="w-full pl-11 pr-4 py-3 bg-slate-950/80 border border-slate-700 focus:border-amber-400 text-slate-100 placeholder-slate-500 rounded-xl text-base outline-none transition theme-input shadow-inner"
        />

        <!-- Live SQLite Search Autocomplete Dropdown Overlay -->
        {#if showSuggestions && suggestions.length > 0}
          <div class="absolute left-0 right-0 top-full mt-2 bg-slate-900/95 border border-slate-700/90 rounded-xl shadow-2xl backdrop-blur-xl z-50 overflow-hidden divide-y divide-slate-800">
            <div class="px-3.5 py-1.5 bg-slate-950/70 text-[11px] font-mono text-slate-400 flex items-center justify-between">
              <span>⚡ SQLite Instant Matches ({suggestions.length})</span>
              <span class="text-amber-400">0ms</span>
            </div>
            <div class="max-h-60 overflow-y-auto">
              {#each suggestions as item}
                <button
                  type="button"
                  onclick={() => {
                    showSuggestions = false;
                    handleSearch(item.word);
                  }}
                  class="w-full px-4 py-2.5 hover:bg-slate-800/90 text-left transition flex items-center justify-between group cursor-pointer"
                >
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-slate-200 group-hover:text-amber-300 transition text-sm">
                      {item.word}
                    </span>
                    {#if item.pos}
                      <span class="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 group-hover:bg-slate-700">
                        {item.pos}
                      </span>
                    {/if}
                    {#if item.definition_vi}
                      <span class="text-xs text-slate-400 truncate max-w-[200px] sm:max-w-xs">
                        - {item.definition_vi}
                      </span>
                    {/if}
                  </div>
                  <div class="flex items-center gap-1.5 shrink-0">
                    {#if item.level}
                      <span class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                        {item.level}
                      </span>
                    {/if}
                    <ArrowRight class="w-3.5 h-3.5 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-0.5 transition" />
                  </div>
                </button>
              {/each}
            </div>
          </div>
        {/if}
      </div>

      <button
        onclick={() => {
          showSuggestions = false;
          handleSearch();
        }}
        disabled={loading || !searchQuery.trim()}
        class="px-6 py-3 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-bold text-sm sm:text-base rounded-xl shadow-lg shadow-amber-500/20 flex items-center justify-center gap-2 cursor-pointer transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
      >
        {#if loading}
          <RefreshCw class="w-4 h-4 animate-spin" />
          <span>Searching...</span>
        {:else}
          <Search class="w-4 h-4" />
          <span>Search</span>
        {/if}
      </button>
    </div>

    <!-- Suggested Words Chips -->
    <div class="mt-4 flex flex-wrap items-center gap-2">
      <span class="text-xs text-slate-400 theme-text-muted flex items-center gap-1 mr-1">
        <Compass class="w-3.5 h-3.5 text-amber-400" />
        Suggested Words:
      </span>
      {#each POPULAR_WORDS as item}
        <button
          onclick={() => handleSearch(item.word)}
          class="px-2.5 py-1 text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-amber-300 border border-slate-700 rounded-lg transition cursor-pointer flex items-center gap-1.5 active:scale-95"
        >
          <span>{item.word}</span>
          <span class="text-[10px] text-slate-400 font-mono">({item.tag})</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Loading State -->
  {#if loading}
    <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center space-y-3 theme-card">
      <div class="inline-flex p-3 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 animate-pulse">
        <Sparkles class="w-6 h-6 animate-spin" />
      </div>
      <div>
        <h3 class="text-lg font-bold text-slate-200">Analyzing & Formatting Word...</h3>
        <p class="text-xs text-slate-400 mt-1">
          Generating definitions, bilingual translation, CEFR level, examples, word family, and synonyms.
        </p>
      </div>
    </div>
  {/if}

  <!-- Error Message -->
  {#if errorMsg && !loading}
    <div class="bg-red-950/40 border border-red-500/40 rounded-2xl p-5 text-red-300 flex items-start gap-3">
      <div class="text-xl">⚠️</div>
      <div>
        <h4 class="font-bold text-sm text-red-200">Word not found or error occurred</h4>
        <p class="text-xs text-red-300/90 mt-0.5">{errorMsg}</p>
      </div>
    </div>
  {/if}

  <!-- Word Result Card: Comprehensive 6-Block Content Layout -->
  {#if currentResult && !loading}
    <div class="bg-slate-900/85 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl backdrop-blur-md theme-card">
      
      <!-- ========================================================================= -->
      <!-- BLOCK 1: Main Word Identity, Badges, Audio & Obsidian Action -->
      <!-- ========================================================================= -->
      <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 border-b border-slate-800 pb-6">
        <div class="space-y-2">
          <div class="flex flex-wrap items-center gap-3">
            <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-slate-100">
              {currentResult.word.word}
            </h1>

            <!-- Part of Speech Badge -->
            {#if currentResult.word.pos}
              <span class="px-2.5 py-0.5 text-xs font-semibold rounded-lg bg-blue-500/15 text-blue-400 border border-blue-500/30">
                {currentResult.word.pos}
              </span>
            {/if}

            <!-- CEFR Level Badge -->
            {#if currentResult.word.level}
              <span class="px-2.5 py-0.5 text-xs font-bold font-mono rounded-lg bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                {currentResult.word.level}
              </span>
            {/if}

            <!-- Source Origin Badge with Clear Visual Indicator -->
            {#if currentResult.source === 'app_vocab'}
              <span class="px-2.5 py-0.5 text-xs font-semibold rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5" title="Loaded directly from native SQLite database file (vocab.db)">
                <span>🗄️</span>
                <span>SQLite DB (0ms)</span>
              </span>
            {:else if currentResult.source === 'online_dict'}
              <span class="px-2.5 py-0.5 text-xs font-semibold rounded-lg bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 flex items-center gap-1.5" title="Loaded from Free Dictionary Online API (~150ms) and saved to SQLite">
                <span>🌐</span>
                <span>Online API ➔ SQLite</span>
              </span>
            {:else if currentResult.source === 'ai'}
              <span class="px-2.5 py-0.5 text-xs font-semibold rounded-lg bg-purple-500/15 text-purple-300 border border-purple-500/30 flex items-center gap-1.5" title="Generated by AI & Saved into SQLite DB">
                <span>✨</span>
                <span>AI Formatted ➔ SQLite</span>
              </span>
            {:else}
              <span class="px-2.5 py-0.5 text-xs font-semibold rounded-lg bg-amber-500/15 text-amber-300 border border-amber-500/30 flex items-center gap-1.5" title="Loaded from Lexicon">
                <span>📖</span>
                <span>Lexicon</span>
              </span>
            {/if}

            <!-- Execution Time Badge -->
            {#if currentResult.executionTimeMs !== undefined}
              <span class="px-2.5 py-0.5 text-xs font-mono font-bold rounded-lg bg-slate-800 text-amber-300 border border-slate-700 flex items-center gap-1">
                <span>⚡</span>
                <span>{currentResult.executionTimeMs}ms</span>
              </span>
            {/if}
          </div>

          <!-- Phonetic -->
          {#if currentResult.word.phonetic}
            <div class="text-base sm:text-lg text-slate-400 font-mono">
              {currentResult.word.phonetic}
            </div>
          {/if}
        </div>

        <!-- Action Buttons (Pronounce, AI Enrich & Save to Vault) -->
        <div class="flex flex-wrap items-center gap-2">
          <!-- AI Deep Enrich Button (Available if not already AI generated) -->
          {#if currentResult.source !== 'ai'}
            <button
              onclick={handleDeepEnrich}
              class="px-3 py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/40 transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold active:scale-95 shadow-sm"
              title="Request AI to analyze deeper: IELTS nuance, etymology, mnemonic hook, and Vietnamese contextual translation"
            >
              <Sparkles class="w-3.5 h-3.5 text-purple-400" />
              <span>AI Deep Enrich ✨</span>
            </button>
          {/if}

          <!-- Audio 1.0x -->
          <button
            onclick={() => handlePlayAudio(false)}
            class="px-3.5 py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600 text-blue-300 hover:text-white border border-blue-500/40 transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold active:scale-95"
            title="Pronounce at 1.0x standard speed"
          >
            <Volume2 class="w-4 h-4" />
            <span>1.0x</span>
          </button>

          <!-- Audio 0.75x Slow -->
          <button
            onclick={() => handlePlayAudio(true)}
            class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition cursor-pointer text-xs font-mono active:scale-95"
            title="Pronounce slowly (0.75x)"
          >
            0.75x 🐢
          </button>

          <!-- Save / Unsave to Obsidian Vault -->
          <button
            onclick={toggleSaveToVault}
            disabled={savingVault}
            class={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold border transition cursor-pointer flex items-center gap-2 shadow-md active:scale-95 ${
              isSavedInVault
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 shadow-emerald-500/10'
                : 'bg-purple-600/30 hover:bg-purple-600 text-purple-200 hover:text-white border-purple-500/40'
            }`}
            title={isSavedInVault ? 'Saved in Obsidian (Click to unsave)' : 'Save to Obsidian Vault'}
          >
            {#if isSavedInVault}
              <Check class="w-4 h-4 text-emerald-400" />
              <span>Saved in Vault</span>
            {:else}
              <Bookmark class="w-4 h-4" />
              <span>Save to Obsidian</span>
            {/if}
          </button>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- BLOCK 2: Definitions Grid (English & Vietnamese) -->
      <!-- ========================================================================= -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- English Definition Card -->
        <div class="bg-slate-950/60 border border-slate-800 rounded-xl p-5 space-y-2 theme-inner">
          <div class="flex items-center gap-1.5 text-xs font-bold text-blue-400 uppercase tracking-wider">
            <BookOpen class="w-4 h-4" />
            <span>English Definition</span>
          </div>
          <p class="text-sm sm:text-base text-slate-200 leading-relaxed font-sans">
            {currentResult.word.definition_en}
          </p>
        </div>

        <!-- Vietnamese Meaning Card -->
        <div class="bg-amber-950/15 border border-amber-500/25 rounded-xl p-5 space-y-2 theme-inner">
          <div class="flex items-center gap-1.5 text-xs font-bold text-amber-400 uppercase tracking-wider">
            <Sparkles class="w-4 h-4" />
            <span>Vietnamese Meaning</span>
          </div>
          <p class="text-sm sm:text-base text-amber-100 leading-relaxed font-medium">
            {currentResult.word.definition_vi || 'Vietnamese translation available in details.'}
          </p>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- BLOCK 3: Word Family & Etymology (Linguistic Root & Derivations) -->
      <!-- ========================================================================= -->
      {#if (currentResult.word_family && currentResult.word_family.length > 0) || currentResult.etymology}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Word Family -->
          {#if currentResult.word_family && currentResult.word_family.length > 0}
            <div class="bg-slate-950/50 border border-slate-800 rounded-xl p-4.5 space-y-2.5 theme-inner">
              <div class="flex items-center gap-1.5 text-xs font-bold text-cyan-400">
                <Network class="w-4 h-4" />
                <span>Word Family / Related Forms</span>
              </div>
              <div class="flex flex-wrap gap-2">
                {#each currentResult.word_family as member}
                  <button
                    onclick={() => handleSearch(member.word)}
                    class="px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-mono transition cursor-pointer flex items-center gap-1.5 active:scale-95"
                    title={`Lookup "${member.word}"`}
                  >
                    <span class="text-[10px] text-cyan-400/70 uppercase">({member.pos}):</span>
                    <span class="font-bold">{member.word}</span>
                  </button>
                {/each}
              </div>
            </div>
          {/if}

          <!-- Etymology / Linguistic Root -->
          {#if currentResult.etymology}
            <div class="bg-slate-950/50 border border-slate-800 rounded-xl p-4.5 space-y-2 theme-inner">
              <div class="flex items-center gap-1.5 text-xs font-bold text-purple-400">
                <History class="w-4 h-4" />
                <span>Etymology & Root Origin</span>
              </div>
              <p class="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans">
                {currentResult.etymology}
              </p>
            </div>
          {/if}
        </div>
      {/if}

      <!-- ========================================================================= -->
      <!-- BLOCK 4: Contextual Bilingual Examples (Multiple Sentences) -->
      <!-- ========================================================================= -->
      <div class="bg-slate-950/70 border border-slate-800 rounded-xl p-5 space-y-3.5 theme-inner">
        <div class="text-xs font-bold text-purple-400 flex items-center gap-1.5 uppercase tracking-wider">
          <Quote class="w-4 h-4" />
          <span>Real-World Contextual Examples</span>
        </div>

        <div class="space-y-3">
          {#if currentResult.examples && currentResult.examples.length > 0}
            {#each currentResult.examples as ex, i}
              <div class="pl-3.5 border-l-2 border-purple-500/60 space-y-1">
                <p class="text-sm sm:text-base text-slate-200 italic font-sans">
                  "{ex.en}"
                </p>
                {#if ex.vi}
                  <p class="text-xs sm:text-sm text-slate-400">
                    👉 {ex.vi}
                  </p>
                {/if}
              </div>
            {/each}
          {:else if currentResult.word.example_en}
            <div class="pl-3.5 border-l-2 border-purple-500/60 space-y-1">
              <p class="text-sm sm:text-base text-slate-200 italic font-sans">
                "{currentResult.word.example_en}"
              </p>
              {#if currentResult.word.example_vi}
                <p class="text-xs sm:text-sm text-slate-400">
                  👉 {currentResult.word.example_vi}
                </p>
              {/if}
            </div>
          {/if}
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- BLOCK 5: Synonyms, Antonyms & High-Yield Collocations -->
      <!-- ========================================================================= -->
      {#if (currentResult.synonyms && currentResult.synonyms.length > 0) || (currentResult.antonyms && currentResult.antonyms.length > 0)}
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Synonyms (Clickable Tags) -->
          {#if currentResult.synonyms && currentResult.synonyms.length > 0}
            <div class="bg-slate-950/50 border border-slate-800 rounded-xl p-4.5 space-y-2.5 theme-inner">
              <div class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                <Tag class="w-3.5 h-3.5" />
                <span>Synonyms (Click to explore):</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                {#each currentResult.synonyms as syn}
                  <button
                    onclick={() => handleSearch(syn)}
                    class="px-2.5 py-1 text-xs bg-emerald-500/10 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/25 rounded-md transition cursor-pointer active:scale-95"
                    title={`Lookup "${syn}"`}
                  >
                    {syn}
                  </button>
                {/each}
              </div>
            </div>
          {/if}

          <!-- Antonyms (Clickable Tags) -->
          {#if currentResult.antonyms && currentResult.antonyms.length > 0}
            <div class="bg-slate-950/50 border border-slate-800 rounded-xl p-4.5 space-y-2.5 theme-inner">
              <div class="text-xs font-bold text-rose-400 flex items-center gap-1.5">
                <Tag class="w-3.5 h-3.5" />
                <span>Antonyms (Click to explore):</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                {#each currentResult.antonyms as ant}
                  <button
                    onclick={() => handleSearch(ant)}
                    class="px-2.5 py-1 text-xs bg-rose-500/10 hover:bg-rose-500/25 text-rose-300 border border-rose-500/25 rounded-md transition cursor-pointer active:scale-95"
                    title={`Lookup "${ant}"`}
                  >
                    {ant}
                  </button>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      {/if}

      <!-- High-Yield Collocations -->
      {#if currentResult.collocations && currentResult.collocations.length > 0}
        <div class="bg-indigo-950/15 border border-indigo-500/25 rounded-xl p-4.5 space-y-2.5 theme-inner">
          <div class="text-xs font-bold text-indigo-300 flex items-center gap-1.5">
            <Lightbulb class="w-4 h-4 text-amber-400" />
            <span>High-Yield Collocations</span>
          </div>
          <div class="flex flex-wrap gap-2 text-xs font-mono text-indigo-200">
            {#each currentResult.collocations as col}
              <span class="px-2.5 py-1 rounded-lg bg-indigo-500/15 border border-indigo-500/30">
                ⚡ {col}
              </span>
            {/each}
          </div>
        </div>
      {/if}

      <!-- ========================================================================= -->
      <!-- BLOCK 6: Memory Hook, IELTS Nuance & Multi-Dictionary Links -->
      <!-- ========================================================================= -->
      {#if currentResult.mnemonic_hook || currentResult.nuance_tips}
        <div class="bg-amber-950/10 border border-amber-500/20 rounded-xl p-4.5 space-y-2.5 theme-inner">
          <div class="text-xs font-bold text-amber-300 flex items-center gap-1.5">
            <BrainCircuit class="w-4 h-4 text-amber-400" />
            <span>Memory Hook & IELTS / Communication Nuance</span>
          </div>

          {#if currentResult.mnemonic_hook}
            <div class="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs sm:text-sm text-amber-200 flex items-start gap-2">
              <span class="text-base">🧠</span>
              <div>
                <strong class="text-amber-300 block mb-0.5">Memory Hook:</strong>
                {currentResult.mnemonic_hook}
              </div>
            </div>
          {/if}

          {#if currentResult.nuance_tips}
            <p class="text-xs sm:text-sm text-slate-300 mt-1 pl-2 border-l-2 border-amber-400/50">
              💡 {currentResult.nuance_tips}
            </p>
          {/if}
        </div>
      {/if}

      <!-- ========================================================================= -->
      <!-- BLOCK 7: Real-time Debug Logs & SQLite Execution Trace Drawer -->
      <!-- ========================================================================= -->
      {#if currentResult.debugLogs && currentResult.debugLogs.length > 0}
        <div class="rounded-xl bg-slate-950/80 border border-slate-800/80 overflow-hidden font-mono text-xs shadow-inner">
          <button
            onclick={() => showDebugLogs = !showDebugLogs}
            class="w-full px-4 py-2.5 bg-slate-900/90 hover:bg-slate-800/90 border-b border-slate-800 transition flex items-center justify-between cursor-pointer text-slate-300 text-left"
          >
            <div class="flex items-center gap-2">
              <Terminal class="w-4 h-4 text-cyan-400" />
              <span class="font-bold text-cyan-300">Execution Pipeline & SQLite Trace</span>
              <span class="px-2 py-0.5 rounded-md bg-cyan-500/20 text-cyan-300 text-[10px] font-bold">
                {currentResult.debugLogs.length} events • {currentResult.executionTimeMs || 0}ms
              </span>
            </div>
            <div class="flex items-center gap-1 text-slate-400 text-[11px]">
              <span>{showDebugLogs ? 'Hide Logs' : 'Show Logs'}</span>
              {#if showDebugLogs}
                <ChevronUp class="w-3.5 h-3.5" />
              {:else}
                <ChevronDown class="w-3.5 h-3.5" />
              {/if}
            </div>
          </button>

          {#if showDebugLogs}
            <div class="p-3.5 space-y-1.5 bg-black/40 text-slate-300 text-[11px] leading-relaxed max-h-48 overflow-y-auto">
              {#each currentResult.debugLogs as logLine}
                <div class="flex items-start gap-2">
                  <span class="text-cyan-500 font-bold select-none">&gt;</span>
                  <span class={`font-mono ${logLine.includes('HIT') || logLine.includes('Successfully') ? 'text-emerald-300 font-semibold' : logLine.includes('MISS') || logLine.includes('error') ? 'text-amber-300' : 'text-slate-300'}`}>
                    {logLine}
                  </span>
                </div>
              {/each}
              <div class="pt-2 border-t border-slate-800/60 text-[10px] text-slate-500 flex items-center justify-between">
                <span>📁 SQLite Database: ~/.local/share/VaultLingo/vocab.db</span>
                <span class="text-emerald-400">● Native Backend Connected</span>
              </div>
            </div>
          {/if}
        </div>
      {/if}

      <!-- External Dictionary Quick Links -->
      <div class="pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
        <span class="text-slate-400 theme-text-muted flex items-center gap-1">
          <ExternalLink class="w-3.5 h-3.5 text-amber-400" />
          Open in External Dictionaries:
        </span>
        <div class="flex flex-wrap items-center gap-2">
          <a
            href={currentResult.word.dict_link || `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(currentResult.word.word)}`}
            target="_blank"
            rel="noopener noreferrer"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-blue-400 border border-slate-700 transition flex items-center gap-1 font-mono text-[11px]"
          >
            <span>Cambridge</span>
            <ExternalLink class="w-3 h-3" />
          </a>
          <a
            href={`https://www.oxfordlearnersdictionaries.com/definition/english/${encodeURIComponent(currentResult.word.word)}`}
            target="_blank"
            rel="noopener noreferrer"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-slate-700 transition flex items-center gap-1 font-mono text-[11px]"
          >
            <span>Oxford</span>
            <ExternalLink class="w-3 h-3" />
          </a>
          <a
            href={`https://www.ldoceonline.com/dictionary/${encodeURIComponent(currentResult.word.word)}`}
            target="_blank"
            rel="noopener noreferrer"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-purple-400 border border-slate-700 transition flex items-center gap-1 font-mono text-[11px]"
          >
            <span>Longman</span>
            <ExternalLink class="w-3 h-3" />
          </a>
          <a
            href={`https://www.merriam-webster.com/dictionary/${encodeURIComponent(currentResult.word.word)}`}
            target="_blank"
            rel="noopener noreferrer"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-400 border border-slate-700 transition flex items-center gap-1 font-mono text-[11px]"
          >
            <span>Merriam-Webster</span>
            <ExternalLink class="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  {/if}
</div>
