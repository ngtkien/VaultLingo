<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    GetDictationSentenceFiltered, 
    CheckDictation, 
    GetDictationCategories, 
    GetDictationLevels 
  } from '../../../wailsjs/go/main/App.js';
  import { playTTS, stopAudio } from '../utils/audio';
  import { 
    Volume2, 
    RefreshCw, 
    CheckCircle2, 
    XCircle, 
    Eye, 
    EyeOff, 
    Sparkles, 
    Award, 
    Filter, 
    ChevronDown, 
    Check, 
    Layers,
    FolderKanban,
    GraduationCap
  } from 'lucide-svelte';

  interface CategoryInfo {
    category: string;
    category_icon: string;
    count: number;
  }

  interface LevelInfo {
    level: string;
    level_color: string;
    count: number;
  }

  const CEFR_LEVEL_GROUPS = [
    { id: 'all', label: 'All Levels', icon: '🌟', desc: 'Any difficulty', color: 'from-blue-500/20 to-indigo-500/20 text-blue-300 border-blue-500/30' },
    { id: 'A2', label: 'A2 Basic', icon: '🌱', desc: 'Everyday Daily English', color: 'from-emerald-500/20 to-teal-500/20 text-emerald-300 border-emerald-500/30' },
    { id: 'B1', label: 'B1 Intermediate', icon: '🌿', desc: 'Workplace & Conversations', color: 'from-cyan-500/20 to-blue-500/20 text-cyan-300 border-cyan-500/30' },
    { id: 'B2', label: 'B2 Advanced', icon: '🚀', desc: 'IELTS, Tech & Academic', color: 'from-purple-500/20 to-amber-500/20 text-purple-300 border-purple-500/30' }
  ];

  let categories = $state<CategoryInfo[]>([]);
  let levels = $state<LevelInfo[]>([]);
  let selectedCategory = $state<string>('all');
  let selectedLevel = $state<string>('all');
  let dictation = $state<any>(null);
  let userInput = $state('');
  let checked = $state(false);
  let diffResult = $state<any>(null);
  let showHint = $state(false);
  let loading = $state(false);
  let isAudioPlaying = $state(false);
  let isCategoryDropdownOpen = $state(false);
  let isLevelDropdownOpen = $state(false);
  let seenIds = $state<number[]>([]);
  let topicSearch = $state('');

  async function loadMetadata() {
    try {
      const [cats, lvls] = await Promise.all([
        GetDictationCategories(),
        GetDictationLevels()
      ]);
      if (cats && cats.length > 0) categories = cats;
      if (lvls && lvls.length > 0) levels = lvls;
    } catch (e) {
      console.error('Failed to load dictation metadata:', e);
    }
  }

  async function loadSentence(category = selectedCategory, level = selectedLevel) {
    loading = true;
    try {
      // Exclude recently seen IDs in this category & level to prevent repeating
      const sentence = await GetDictationSentenceFiltered(category, level, seenIds);
      dictation = sentence;
      if (sentence?.id) {
        if (!seenIds.includes(sentence.id)) {
          seenIds = [...seenIds, sentence.id];
        }
      }
      userInput = '';
      checked = false;
      diffResult = null;
      showHint = false;
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  function handleSelectCategory(cat: string) {
    if (selectedCategory !== cat) {
      selectedCategory = cat;
      seenIds = []; // reset seen queue when switching topic
    }
    isCategoryDropdownOpen = false;
    topicSearch = '';
    loadSentence(cat, selectedLevel);
  }

  function handleSelectLevel(lvl: string) {
    if (selectedLevel !== lvl) {
      selectedLevel = lvl;
      seenIds = []; // reset seen queue when switching level
    }
    isLevelDropdownOpen = false;
    loadSentence(selectedCategory, lvl);
  }

  function playAudio(slow = false) {
    if (!dictation?.sentence) return;
    isAudioPlaying = true;
    playTTS(dictation.sentence, slow ? 0.75 : 1.0, 'dictation').then(() => {
      isAudioPlaying = false;
    });
  }

  async function handleCheck() {
    if (!dictation?.sentence || !userInput.trim()) return;
    try {
      diffResult = await CheckDictation(dictation.sentence, userInput);
      checked = true;
    } catch (e) {
      console.error(e);
    }
  }

  // Active metadata derivations
  let activeCategoryInfo = $derived(() => {
    if (selectedCategory === 'all') {
      return { category: 'All Topics', category_icon: '🌟', count: categories.reduce((acc, c) => acc + c.count, 0) };
    }
    const found = categories.find(c => c.category === selectedCategory);
    return found || { category: selectedCategory, category_icon: '🎧', count: 0 };
  });

  let activeLevelInfo = $derived(() => {
    const found = CEFR_LEVEL_GROUPS.find(l => l.id === selectedLevel);
    if (found) return found;
    return { id: selectedLevel, label: selectedLevel, icon: '🎯', desc: selectedLevel, color: 'text-slate-300' };
  });

  let filteredCategories = $derived(() => {
    if (!topicSearch.trim()) return categories;
    const query = topicSearch.toLowerCase().trim();
    return categories.filter(c => c.category.toLowerCase().includes(query));
  });

  onMount(async () => {
    await loadMetadata();
    loadSentence('all', 'all');
  });
</script>

<svelte:window onclick={(e) => {
  const target = e.target as HTMLElement;
  if (!target.closest('.category-dropdown-container')) {
    isCategoryDropdownOpen = false;
  }
  if (!target.closest('.level-dropdown-container')) {
    isLevelDropdownOpen = false;
  }
}} />

<div class="max-w-3xl mx-auto space-y-6">
  <!-- Top Practice Filters Bar -->
  <div class="relative z-30 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-lg backdrop-blur-md space-y-4">
    <!-- Level Selector Bar -->
    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-xs font-bold text-slate-300">
          <GraduationCap class="w-4 h-4 text-emerald-400" />
          <span>Difficulty Level (CEFR):</span>
        </div>
        <span class="text-[11px] text-slate-400 font-mono">
          Current: <strong class="text-emerald-400">{activeLevelInfo().label}</strong>
        </span>
      </div>

      <!-- CEFR Level Pills Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {#each CEFR_LEVEL_GROUPS as lvl}
          <button
            onclick={() => handleSelectLevel(lvl.id)}
            class={`p-2.5 rounded-xl border text-left transition cursor-pointer flex items-center gap-2.5 ${
              selectedLevel === lvl.id
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 border-emerald-400 text-white font-bold shadow-md shadow-emerald-500/25 ring-1 ring-emerald-400/50'
                : 'bg-slate-950/70 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
            }`}
          >
            <span class="text-lg shrink-0">{lvl.icon}</span>
            <div class="min-w-0 flex-1">
              <div class="text-xs font-bold truncate leading-tight">{lvl.label}</div>
              <div class={`text-[10px] truncate opacity-75 ${selectedLevel === lvl.id ? 'text-white' : 'text-slate-500'}`}>
                {lvl.desc}
              </div>
            </div>
          </button>
        {/each}
      </div>
    </div>

    <!-- Divider -->
    <div class="h-px bg-slate-800/80"></div>

    <!-- Practice Topic Bar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
          <Filter class="w-3.5 h-3.5" />
        </div>
        <div>
          <span class="text-xs font-bold text-slate-300 block">Topic Domain:</span>
          <span class="text-[11px] text-slate-400">Filter by conversational context</span>
        </div>
      </div>

      <!-- Dropdown Selector -->
      <div class="relative category-dropdown-container">
        <button
          onclick={() => isCategoryDropdownOpen = !isCategoryDropdownOpen}
          class="w-full sm:w-64 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700/80 hover:border-slate-600 text-slate-200 text-xs font-semibold flex items-center justify-between transition cursor-pointer shadow-inner"
        >
          <div class="flex items-center gap-2 truncate">
            <span>{activeCategoryInfo().category_icon}</span>
            <span class="truncate">{activeCategoryInfo().category}</span>
          </div>
          <ChevronDown class={`w-3.5 h-3.5 text-slate-400 transition-transform duration-200 ${isCategoryDropdownOpen ? 'rotate-180' : ''}`} />
        </button>

        {#if isCategoryDropdownOpen}
          <div class="absolute right-0 top-full mt-2 w-80 max-h-80 overflow-y-auto bg-slate-950 border border-slate-700 rounded-2xl shadow-2xl shadow-black/90 z-50 p-2 backdrop-blur-xl space-y-1 ring-1 ring-slate-700/50">
            <!-- Search input inside dropdown -->
            <div class="px-1 pb-1">
              <input
                type="text"
                bind:value={topicSearch}
                placeholder="Search topics (e.g. IELTS, Tech, Food)..."
                class="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-slate-200 placeholder-slate-500 text-xs outline-none focus:border-blue-500 transition"
              />
            </div>

            <!-- All Topics Option -->
            {#if !topicSearch.trim()}
              <button
                onclick={() => handleSelectCategory('all')}
                class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between transition cursor-pointer ${
                  selectedCategory === 'all' 
                    ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30' 
                    : 'hover:bg-slate-900 text-slate-300'
                }`}
              >
                <div class="flex items-center gap-2.5">
                  <span class="text-base">🌟</span>
                  <span class="font-bold">All Topics</span>
                </div>
                {#if selectedCategory === 'all'}
                  <Check class="w-3.5 h-3.5 text-blue-400" />
                {/if}
              </button>

              <div class="h-px bg-slate-800 my-1"></div>
            {/if}

            <!-- Dynamic Categories List -->
            {#each filteredCategories() as cat}
              <button
                onclick={() => handleSelectCategory(cat.category)}
                class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between transition cursor-pointer ${
                  selectedCategory === cat.category 
                    ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30 font-semibold' 
                    : 'hover:bg-slate-900 text-slate-300'
                }`}
              >
                <div class="flex items-center gap-2.5 truncate">
                  <span class="text-base">{cat.category_icon}</span>
                  <span class="truncate">{cat.category}</span>
                </div>
                <div class="flex items-center gap-1.5">
                  <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                    {cat.count}
                  </span>
                  {#if selectedCategory === cat.category}
                    <Check class="w-3.5 h-3.5 text-blue-400" />
                  {/if}
                </div>
              </button>
            {/each}

            {#if filteredCategories().length === 0}
              <div class="py-3 text-center text-xs text-slate-500">
                No matching topic found.
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </div>
  </div>

  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-emerald-500" />
      <p class="text-sm font-medium">Loading {activeLevelInfo().label} dictation sentence...</p>
    </div>
  {:else if dictation}
    <!-- Dictation Main Practice Card -->
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-xl space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-2xl">{dictation.category_icon || '🎧'}</span>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-lg font-bold text-slate-100">{dictation.category}</h3>
            </div>
            <div class="flex items-center gap-2 mt-0.5">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                {dictation.level}
              </span>
              {#if selectedLevel !== 'all'}
                <span class="text-[11px] text-slate-400 font-mono">
                  (Filtered by {selectedLevel})
                </span>
              {/if}
            </div>
          </div>
        </div>

        <button
          onclick={() => loadSentence(selectedCategory, selectedLevel)}
          class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold shadow-sm active:scale-95"
          title="Load next sentence with current filters"
        >
          <RefreshCw class="w-3.5 h-3.5" />
          <span>Next Sentence</span>
        </button>
      </div>

      <!-- Audio Control Center -->
      <div class="bg-slate-950/60 p-6 rounded-2xl border border-slate-800/80 flex flex-col items-center justify-center space-y-4">
        <div class="flex items-center gap-4">
          <button
            onclick={() => playAudio(false)}
            class="px-6 py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm flex items-center gap-2 shadow-lg shadow-emerald-500/30 active:scale-95 transition cursor-pointer"
          >
            <Volume2 class={`w-5 h-5 ${isAudioPlaying ? 'animate-bounce' : ''}`} />
            <span>Play Audio (1.0x)</span>
          </button>

          <button
            onclick={() => playAudio(true)}
            class="px-4 py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-sm transition cursor-pointer border border-slate-700 active:scale-95"
          >
            Slow (0.75x)
          </button>
        </div>

        <p class="text-xs text-slate-400">
          Listen carefully to the neural pronunciation and transcribe what you hear below 👇
        </p>
      </div>

      <!-- Dictation Input Box -->
      <div class="space-y-3">
        <div class="relative">
          <textarea
            bind:value={userInput}
            onkeydown={(e) => {
              if (e.key === 'Enter' && (e.ctrlKey || e.metaKey || !e.shiftKey)) {
                e.preventDefault();
                handleCheck();
              }
            }}
            placeholder="Type the sentence you hear..."
            rows="3"
            class="w-full bg-slate-950 border border-slate-700/80 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 rounded-2xl p-4 text-base text-slate-100 placeholder-slate-500 outline-none transition resize-none leading-relaxed font-sans"
          ></textarea>
        </div>

        <div class="flex items-center justify-between">
          <button
            onclick={() => showHint = !showHint}
            class="text-xs font-semibold text-slate-400 hover:text-slate-200 flex items-center gap-1.5 transition cursor-pointer"
          >
            {#if showHint}
              <EyeOff class="w-3.5 h-3.5" />
              <span>Hide Hint</span>
            {:else}
              <Eye class="w-3.5 h-3.5" />
              <span>Show Keyword Hint</span>
            {/if}
          </button>

          <button
            onclick={handleCheck}
            disabled={!userInput.trim()}
            class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:opacity-50 text-white font-bold text-sm transition shadow-lg shadow-emerald-500/25 active:scale-95 cursor-pointer"
          >
            Check Dictation (Enter)
          </button>
        </div>

        <!-- Hint Box -->
        {#if showHint && dictation.hint}
          <div class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
            <strong>Hint:</strong> {dictation.hint}
          </div>
        {/if}
      </div>

      <!-- Diff & Accuracy Result Breakdown -->
      {#if checked && diffResult}
        <div class="bg-slate-950/80 rounded-2xl p-5 border border-slate-800 space-y-4 animate-fade-in">
          <!-- Accuracy Score Header -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Award class={`w-6 h-6 ${diffResult.passed ? 'text-emerald-400' : 'text-amber-400'}`} />
              <div>
                <span class="text-sm font-bold text-slate-200">Accuracy Score: </span>
                <span class={`text-xl font-extrabold ${diffResult.passed ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {diffResult.accuracy}%
                </span>
              </div>
            </div>

            <span class={`px-3 py-1 rounded-full text-xs font-bold ${
              diffResult.passed ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
            }`}>
              {diffResult.passed ? '🎉 Passed' : '⚡ Keep Practicing'}
            </span>
          </div>

          <!-- Token-by-Token Visual Diff -->
          <div class="p-4 rounded-xl bg-slate-900 border border-slate-800/80 space-y-2">
            <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Word-by-word Diff Comparison:</span>
            <div class="flex flex-wrap gap-2 text-base font-mono leading-relaxed pt-1">
              {#each diffResult.tokens as tok}
                {#if tok.type === 'correct'}
                  <span class="px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                    {tok.word}
                  </span>
                {:else if tok.type === 'wrong'}
                  <span class="px-2 py-0.5 rounded-lg bg-red-500/20 text-red-300 line-through border border-red-500/40" title="Incorrect word">
                    {tok.word}
                  </span>
                {:else if tok.type === 'missing'}
                  <span class="px-2 py-0.5 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 underline" title={`Missing word: "${tok.match}"`}>
                    [{tok.match}]
                  </span>
                {/if}
              {/each}
            </div>
          </div>

          <!-- Original Correct Sentence & Translation -->
          <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800/60 space-y-1.5 text-sm">
            <div class="text-slate-300">
              <strong class="text-slate-100">Original Sentence:</strong> {dictation.sentence}
            </div>
            {#if dictation.sentence_vi}
              <div class="text-xs text-slate-400 italic">
                <strong>Translation:</strong> {dictation.sentence_vi}
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>
