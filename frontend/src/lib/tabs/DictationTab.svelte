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
    Award, 
    Filter, 
    ChevronDown, 
    Check, 
    Eye, 
    EyeOff, 
    GraduationCap,
    Sparkles
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
    { id: 'all', label: 'All Levels', icon: '🌟', desc: 'Any difficulty' },
    { id: 'A2', label: 'A2 Basic', icon: '🌱', desc: 'Everyday English' },
    { id: 'B1', label: 'B1 Intermediate', icon: '🌿', desc: 'Workplace & Context' },
    { id: 'B2', label: 'B2 Advanced', icon: '🚀', desc: 'Academic & Tech' }
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
      const sentence = await GetDictationSentenceFiltered(category, level, seenIds);
      dictation = sentence;
      if (sentence?.id && !seenIds.includes(sentence.id)) {
        seenIds = [...seenIds, sentence.id];
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
      seenIds = [];
    }
    isCategoryDropdownOpen = false;
    topicSearch = '';
    loadSentence(cat, selectedLevel);
  }

  function handleSelectLevel(lvl: string) {
    if (selectedLevel !== lvl) {
      selectedLevel = lvl;
      seenIds = [];
    }
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
    return { id: selectedLevel, label: selectedLevel, icon: '🎯', desc: selectedLevel };
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
}} />

<div class="w-full max-w-5xl mx-auto space-y-6 pb-12">
  <!-- Header Title -->
  <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-0.5 rounded text-[10px]">
          Audio Training
        </span>
      </div>
      <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)] mt-1">
        Dictation Practice
      </h1>
      <p class="text-sm font-serif italic text-[var(--text-muted)] mt-1">
        Train your ear and refine your spelling with real-world audio dictation.
      </p>
    </div>

    <button
      onclick={() => loadSentence(selectedCategory, selectedLevel)}
      class="p-2.5 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold border border-[var(--border-main)] self-start sm:self-auto"
      title="Load next sentence"
    >
      <RefreshCw class="w-3.5 h-3.5" />
      <span>Next Sentence</span>
    </button>
  </div>

  <!-- Filters: CEFR Level & Topic Domain (matches 5.png) -->
  <section class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-4">
    <!-- CEFR Levels -->
    <div class="space-y-2">
      <div class="flex items-center justify-between text-xs font-semibold text-[var(--text-muted)]">
        <div class="flex items-center gap-1.5">
          <GraduationCap class="w-4 h-4 text-[var(--accent-primary)]" />
          <span>Difficulty Level (CEFR):</span>
        </div>
        <span class="font-mono">Current: <strong class="text-[var(--accent-primary)]">{activeLevelInfo().label}</strong></span>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {#each CEFR_LEVEL_GROUPS as lvl}
          {@const isSelected = selectedLevel === lvl.id}
          <button
            onclick={() => handleSelectLevel(lvl.id)}
            class={`p-3 rounded-xl border text-left transition cursor-pointer flex items-center gap-2.5 ${
              isSelected
                ? 'bg-[var(--accent-primary)] text-white border-[var(--accent-primary)] font-bold shadow-sm'
                : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)] hover:border-[var(--accent-primary)]'
            }`}
          >
            <span class="text-base">{lvl.icon}</span>
            <div class="min-w-0 flex-1">
              <div class="text-xs font-bold truncate">{lvl.label}</div>
              <div class={`text-[10px] truncate ${isSelected ? 'text-white/80' : 'text-[var(--text-subtle)]'}`}>
                {lvl.desc}
              </div>
            </div>
          </button>
        {/each}
      </div>
    </div>

    <div class="h-px bg-[var(--border-main)]"></div>

    <!-- Topic Domain Selector -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <Filter class="w-4 h-4 text-[var(--accent-primary)]" />
        <div>
          <span class="text-xs font-semibold text-[var(--text-main)] block">Topic Domain:</span>
          <span class="text-[11px] text-[var(--text-muted)]">Select vocabulary context</span>
        </div>
      </div>

      <!-- Dropdown -->
      <div class="relative category-dropdown-container">
        <button
          onclick={() => isCategoryDropdownOpen = !isCategoryDropdownOpen}
          class="w-full sm:w-64 px-3.5 py-2 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] hover:border-[var(--accent-primary)] text-[var(--text-main)] text-xs font-semibold flex items-center justify-between transition cursor-pointer"
        >
          <div class="flex items-center gap-2 truncate">
            <span>{activeCategoryInfo().category_icon}</span>
            <span class="truncate">{activeCategoryInfo().category}</span>
          </div>
          <ChevronDown class={`w-3.5 h-3.5 text-[var(--text-muted)] transition-transform ${isCategoryDropdownOpen ? 'rotate-180' : ''}`} />
        </button>

        {#if isCategoryDropdownOpen}
          <div class="absolute right-0 top-full mt-2 w-80 max-h-72 overflow-y-auto bg-[var(--bg-card)] border border-[var(--border-main)] rounded-2xl shadow-xl z-50 p-2 space-y-1">
            <div class="px-1 pb-1">
              <input
                type="text"
                bind:value={topicSearch}
                placeholder="Search topics..."
                class="w-full px-3 py-1.5 rounded-lg bg-[var(--bg-inner)] border border-[var(--border-main)] text-[var(--text-main)] text-xs outline-none focus:border-[var(--accent-primary)]"
              />
            </div>

            {#if !topicSearch.trim()}
              <button
                onclick={() => handleSelectCategory('all')}
                class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between cursor-pointer ${
                  selectedCategory === 'all'
                    ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold'
                    : 'hover:bg-[var(--bg-inner)] text-[var(--text-main)]'
                }`}
              >
                <div class="flex items-center gap-2">
                  <span>🌟</span>
                  <span>All Topics</span>
                </div>
                {#if selectedCategory === 'all'}
                  <Check class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                {/if}
              </button>
              <div class="h-px bg-[var(--border-main)] my-1"></div>
            {/if}

            {#each filteredCategories() as cat}
              <button
                onclick={() => handleSelectCategory(cat.category)}
                class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between cursor-pointer ${
                  selectedCategory === cat.category
                    ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold'
                    : 'hover:bg-[var(--bg-inner)] text-[var(--text-main)]'
                }`}
              >
                <div class="flex items-center gap-2 truncate">
                  <span>{cat.category_icon}</span>
                  <span class="truncate">{cat.category}</span>
                </div>
                <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-[var(--bg-inner)] text-[var(--text-subtle)] font-mono">
                  {cat.count}
                </span>
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  </section>

  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 text-[var(--text-muted)] space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-[var(--accent-primary)]" />
      <p class="text-sm font-medium font-serif italic">Selecting audio sentence...</p>
    </div>
  {:else if dictation}
    <!-- Main Dictation Practice Card -->
    <article class="journal-card p-6 sm:p-8 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-2xl">{dictation.category_icon || '🎧'}</span>
          <div>
            <h2 class="text-lg font-bold font-serif text-[var(--text-main)]">{dictation.category}</h2>
            <div class="flex items-center gap-2 mt-0.5">
              <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-[var(--accent-primary-light)] text-[var(--accent-primary)] border border-[var(--accent-primary-border)]">
                {dictation.level}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Audio Control Center -->
      <div class="p-6 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-col items-center justify-center space-y-3">
        <div class="flex items-center gap-3">
          <button
            onclick={() => playAudio(false)}
            class="px-6 py-3 rounded-xl btn-forest font-bold text-sm flex items-center gap-2 shadow-sm cursor-pointer"
          >
            <Volume2 class={`w-5 h-5 ${isAudioPlaying ? 'animate-bounce' : ''}`} />
            <span>Play Audio (1.0x)</span>
          </button>

          <button
            onclick={() => playAudio(true)}
            class="px-4 py-3 rounded-xl bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] hover:text-[var(--accent-primary)] font-semibold text-sm transition cursor-pointer border border-[var(--border-main)]"
          >
            Slow (0.75x)
          </button>
        </div>

        <p class="text-xs text-[var(--text-muted)] font-serif italic">
          Listen carefully to the audio and transcribe what you hear below.
        </p>
      </div>

      <!-- User Input Box -->
      <div class="space-y-3">
        <textarea
          bind:value={userInput}
          onkeydown={(e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey || !e.shiftKey)) {
              e.preventDefault();
              handleCheck();
            }
          }}
          placeholder="Type the exact sentence you hear..."
          rows="3"
          class="w-full bg-[var(--bg-inner)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-2xl p-4 text-base text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none transition resize-none font-sans"
        ></textarea>

        <div class="flex items-center justify-between">
          <button
            onclick={() => showHint = !showHint}
            class="text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--accent-primary)] flex items-center gap-1.5 transition cursor-pointer"
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
            class="px-6 py-2.5 rounded-xl btn-forest disabled:opacity-50 font-bold text-sm transition shadow-sm cursor-pointer"
          >
            Check Dictation (Enter)
          </button>
        </div>

        {#if showHint && dictation.hint}
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] text-xs text-[var(--accent-primary)]">
            <strong>Hint:</strong> {dictation.hint}
          </div>
        {/if}
      </div>

      <!-- Diff & Accuracy Breakdown -->
      {#if checked && diffResult}
        <div class="p-5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Award class={`w-5 h-5 ${diffResult.passed ? 'text-emerald-600' : 'text-amber-600'}`} />
              <div>
                <span class="text-sm font-semibold text-[var(--text-main)]">Accuracy: </span>
                <span class={`text-lg font-bold font-mono ${diffResult.passed ? 'text-emerald-600' : 'text-amber-600'}`}>
                  {diffResult.accuracy}%
                </span>
              </div>
            </div>

            <span class={`px-3 py-1 rounded-full text-xs font-bold ${
              diffResult.passed
                ? 'bg-emerald-500/15 text-emerald-700 border border-emerald-400/30'
                : 'bg-amber-500/15 text-amber-700 border border-amber-400/30'
            }`}>
              {diffResult.passed ? '🎉 Passed' : '⚡ Keep Practicing'}
            </span>
          </div>

          <!-- Token-by-Token Diff -->
          <div class="p-4 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] space-y-2">
            <span class="journal-badge text-[var(--text-subtle)]">Word-by-word Diff Comparison:</span>
            <div class="flex flex-wrap gap-1.5 text-sm font-mono pt-1">
              {#each diffResult.tokens as tok}
                {#if tok.type === 'correct'}
                  <span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-700 border border-emerald-400/30 font-semibold">
                    {tok.word}
                  </span>
                {:else if tok.type === 'wrong'}
                  <span class="px-2 py-0.5 rounded bg-red-500/15 text-red-700 line-through border border-red-400/30" title="Incorrect">
                    {tok.word}
                  </span>
                {:else if tok.type === 'missing'}
                  <span class="px-2 py-0.5 rounded bg-amber-500/15 text-amber-700 underline border border-amber-400/30" title="Missing word">
                    [{tok.match}]
                  </span>
                {/if}
              {/each}
            </div>
          </div>

          <!-- Original Correct Sentence & Translation -->
          <div class="p-4 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] space-y-1 text-sm">
            <div class="text-[var(--text-main)] font-serif italic text-base">
              “{dictation.sentence}”
            </div>
            {#if dictation.sentence_vi}
              <div class="text-xs text-[var(--text-muted)] pt-1 border-t border-[var(--border-main)]">
                👉 {dictation.sentence_vi}
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </article>
  {/if}
</div>
