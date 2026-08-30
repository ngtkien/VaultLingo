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
    Compass
  } from 'lucide-svelte';
  import { lookupSmartDictionary, type SmartWordResult } from '../utils/smartDictionary';
  import { SaveWordToObsidian, DeleteWordFromObsidian, GetSavedObsidianVocab } from '../../../wailsjs/go/main/App.js';
  import { playTTS, playAudioUrl } from '../utils/audio';

  let searchQuery = $state('');
  let loading = $state(false);
  let errorMsg = $state('');
  let currentResult = $state<SmartWordResult | null>(null);
  let isSavedInVault = $state(false);
  let savingVault = $state(false);

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

  async function handleSearch(targetWord?: string) {
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

  onMount(() => {
    handleSearch('serendipity');
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
          Search any English word • Structured VaultLingo schema • One-click sync to Obsidian
        </p>
      </div>

      <div class="flex items-center gap-2">
        <span class="px-3 py-1 text-xs font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30 rounded-xl">
          ⚡ AI Lexicon Ready
        </span>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="mt-5 flex flex-col sm:flex-row items-stretch gap-3">
      <div class="relative flex-1">
        <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <Search class="w-5 h-5" />
        </div>
        <input
          type="text"
          bind:value={searchQuery}
          onkeydown={handleKeydown}
          placeholder="Type any English word (e.g., ubiquitous, resilience, serendipity...)"
          class="w-full pl-11 pr-4 py-3 bg-slate-950/80 border border-slate-700 focus:border-amber-400 text-slate-100 placeholder-slate-500 rounded-xl text-base outline-none transition theme-input shadow-inner"
        />
      </div>

      <button
        onclick={() => handleSearch()}
        disabled={loading || !searchQuery.trim()}
        class="px-6 py-3 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-bold text-sm sm:text-base rounded-xl shadow-lg shadow-amber-500/20 flex items-center justify-center gap-2 cursor-pointer transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
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
          Generating definitions, bilingual translation, CEFR level, examples, and synonyms.
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

  <!-- Word Result Card -->
  {#if currentResult && !loading}
    <div class="bg-slate-900/85 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl backdrop-blur-md theme-card">
      <!-- Main Word Header & Badges -->
      <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 border-b border-slate-800 pb-6">
        <div class="space-y-2">
          <div class="flex flex-wrap items-center gap-3">
            <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-100">
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

            <!-- Source Origin Badge -->
            <span class="px-2.5 py-0.5 text-[11px] font-mono rounded-md bg-slate-800 text-slate-400 border border-slate-700">
              {#if currentResult.source === 'vault'}
                📁 Saved in Vault
              {:else if currentResult.source === 'app_vocab'}
                📚 App Lexicon
              {:else if currentResult.source === 'ai'}
                ✨ AI Formatted
              {:else if currentResult.source === 'online_dict'}
                🌐 Online Dictionary
              {:else}
                📖 Lexicon
              {/if}
            </span>
          </div>

          <!-- Phonetic -->
          {#if currentResult.word.phonetic}
            <div class="text-base text-slate-400 font-mono">
              {currentResult.word.phonetic}
            </div>
          {/if}
        </div>

        <!-- Action Buttons (Pronounce & Save to Vault) -->
        <div class="flex flex-wrap items-center gap-2">
          <!-- Audio 1.0x -->
          <button
            onclick={() => handlePlayAudio(false)}
            class="px-3 py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600 text-blue-300 hover:text-white border border-blue-500/40 transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold"
            title="Pronounce at 1.0x standard speed"
          >
            <Volume2 class="w-4 h-4" />
            <span>1.0x</span>
          </button>

          <!-- Audio 0.75x Slow -->
          <button
            onclick={() => handlePlayAudio(true)}
            class="px-2.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition cursor-pointer text-xs font-mono"
            title="Pronounce slowly (0.75x)"
          >
            0.75x 🐢
          </button>

          <!-- Save / Unsave to Obsidian Vault -->
          <button
            onclick={toggleSaveToVault}
            disabled={savingVault}
            class={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold border transition cursor-pointer flex items-center gap-2 shadow-md ${
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

      <!-- Definitions Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- English Definition Card -->
        <div class="bg-slate-950/60 border border-slate-800 rounded-xl p-4.5 space-y-2 theme-inner">
          <div class="flex items-center gap-1.5 text-xs font-bold text-blue-400">
            <BookOpen class="w-4 h-4" />
            <span>English Definition</span>
          </div>
          <p class="text-sm sm:text-base text-slate-200 leading-relaxed font-sans">
            {currentResult.word.definition_en}
          </p>
        </div>

        <!-- Vietnamese Meaning Card -->
        <div class="bg-amber-950/15 border border-amber-500/25 rounded-xl p-4.5 space-y-2 theme-inner">
          <div class="flex items-center gap-1.5 text-xs font-bold text-amber-400">
            <Sparkles class="w-4 h-4" />
            <span>Vietnamese Meaning</span>
          </div>
          <p class="text-sm sm:text-base text-amber-100 leading-relaxed font-medium">
            {currentResult.word.definition_vi || 'Vietnamese translation available in details.'}
          </p>
        </div>
      </div>

      <!-- Example Sentence Card -->
      {#if currentResult.word.example_en}
        <div class="bg-slate-950/70 border border-slate-800 rounded-xl p-5 space-y-2.5 theme-inner">
          <div class="text-xs font-bold text-purple-400 flex items-center gap-1.5">
            <span>💬</span>
            <span>Example in Context</span>
          </div>
          <blockquote class="text-sm sm:text-base text-slate-200 italic pl-3 border-l-2 border-purple-500/60">
            "{currentResult.word.example_en}"
          </blockquote>
          {#if currentResult.word.example_vi}
            <p class="text-xs sm:text-sm text-slate-400 pl-3">
              👉 {currentResult.word.example_vi}
            </p>
          {/if}
        </div>
      {/if}

      <!-- Synonyms, Antonyms & Collocations Section -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <!-- Synonyms -->
        {#if currentResult.synonyms && currentResult.synonyms.length > 0}
          <div class="bg-slate-950/50 border border-slate-800 rounded-xl p-4 space-y-2 theme-inner">
            <div class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
              <Tag class="w-3.5 h-3.5" />
              <span>Synonyms:</span>
            </div>
            <div class="flex flex-wrap gap-1.5">
              {#each currentResult.synonyms as syn}
                <button
                  onclick={() => handleSearch(syn)}
                  class="px-2 py-0.5 text-xs bg-emerald-500/10 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/25 rounded-md transition cursor-pointer active:scale-95"
                  title={`Lookup "${syn}"`}
                >
                  {syn}
                </button>
              {/each}
            </div>
          </div>
        {/if}

        <!-- Antonyms -->
        {#if currentResult.antonyms && currentResult.antonyms.length > 0}
          <div class="bg-slate-950/50 border border-slate-800 rounded-xl p-4 space-y-2 theme-inner">
            <div class="text-xs font-bold text-rose-400 flex items-center gap-1.5">
              <Tag class="w-3.5 h-3.5" />
              <span>Antonyms:</span>
            </div>
            <div class="flex flex-wrap gap-1.5">
              {#each currentResult.antonyms as ant}
                <button
                  onclick={() => handleSearch(ant)}
                  class="px-2 py-0.5 text-xs bg-rose-500/10 hover:bg-rose-500/25 text-rose-300 border border-rose-500/25 rounded-md transition cursor-pointer active:scale-95"
                  title={`Lookup "${ant}"`}
                >
                  {ant}
                </button>
              {/each}
            </div>
          </div>
        {/if}
      </div>

      <!-- Collocations & Nuance / Usage Tips -->
      {#if currentResult.collocations && currentResult.collocations.length > 0 || currentResult.nuance_tips}
        <div class="bg-indigo-950/15 border border-indigo-500/25 rounded-xl p-4.5 space-y-2.5 theme-inner">
          <div class="text-xs font-bold text-indigo-300 flex items-center gap-1.5">
            <Lightbulb class="w-4 h-4 text-amber-400" />
            <span>Collocations & Usage Tips</span>
          </div>

          {#if currentResult.collocations && currentResult.collocations.length > 0}
            <div class="flex flex-wrap gap-2 text-xs font-mono text-indigo-200">
              {#each currentResult.collocations as col}
                <span class="px-2.5 py-1 rounded-md bg-indigo-500/15 border border-indigo-500/30">
                  ⚡ {col}
                </span>
              {/each}
            </div>
          {/if}

          {#if currentResult.nuance_tips}
            <p class="text-xs sm:text-sm text-slate-300 mt-1">
              💡 {currentResult.nuance_tips}
            </p>
          {/if}
        </div>
      {/if}

      <!-- External Dictionary Quick Links -->
      <div class="pt-2 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
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
