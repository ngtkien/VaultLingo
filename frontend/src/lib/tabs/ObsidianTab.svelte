<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    GetSavedObsidianVocab, 
    UpdateObsidianSrsReview, 
    DeleteWordFromObsidian, 
    OpenInObsidian, 
    GetConfig 
  } from '../../../wailsjs/go/main/App.js';
  import { playTTS } from '../utils/audio';
  import { 
    ExternalLink, 
    RefreshCw, 
    Volume2, 
    Calendar, 
    Clock, 
    Trash2, 
    ChevronDown,
    List,
    LayoutGrid,
    MoreVertical,
    ArrowUpDown
  } from 'lucide-svelte';

  let { onNavigateToDictionary } = $props<{ onNavigateToDictionary?: (word: string) => void }>();

  let items = $state<any[]>([]);
  let config = $state<any>(null);
  let loading = $state(false);
  let activeSubTab = $state<'saved' | 'due'>('saved');
  let viewMode = $state<'list' | 'grid'>('list');
  let sortOrder = $state<'newest' | 'oldest' | 'alphabetical'>('newest');
  let openDropdownWord = $state<string | null>(null);

  let filteredItems = $derived(
    items.filter(item => {
      if (activeSubTab === 'due' && !item.is_due) return false;
      return true;
    }).sort((a, b) => {
      if (sortOrder === 'alphabetical') return a.word.localeCompare(b.word);
      if (sortOrder === 'oldest') return (a.id || 0) - (b.id || 0);
      return (b.id || 0) - (a.id || 0);
    })
  );

  let dueCount = $derived(
    items.filter(item => item.is_due).length
  );

  function cleanString(text: string | undefined | null): string {
    if (!text) return '';
    return text
      .replace(/:\s*:\s*id=[^"'\s]*/gi, '')
      .replace(/id=[a-zA-Z0-9._&=-]+/gi, '')
      .replace(/\s*\b\d{3,}\b\s*$/, '')
      .trim();
  }

  async function loadObsidianData() {
    loading = true;
    try {
      config = await GetConfig();
      items = await GetSavedObsidianVocab();
      openDropdownWord = null;
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function handleDeleteWord(word: string) {
    try {
      await DeleteWordFromObsidian(word);
      await loadObsidianData();
    } catch (e) {
      console.error(e);
    }
  }

  async function handleSrsRate(item: any, rating: number) {
    try {
      await UpdateObsidianSrsReview(item.word, item.file_path, rating);
      await loadObsidianData();
    } catch (e) {
      console.error(e);
    }
  }

  async function handleOpenInObsidian(filePath: string) {
    try {
      await OpenInObsidian(filePath);
    } catch (e) {
      console.error(e);
    }
  }

  function toggleDropdown(word: string, e?: Event) {
    if (e) e.stopPropagation();
    openDropdownWord = openDropdownWord === word ? null : word;
  }

  onMount(() => {
    loadObsidianData();
    const closeDropdown = () => { openDropdownWord = null; };
    window.addEventListener('click', closeDropdown);
    return () => {
      window.removeEventListener('click', closeDropdown);
    };
  });
</script>

<div class="w-full max-w-6xl mx-auto space-y-5 pb-12">
  
  <!-- Subnav Tabs (Saved & Obsidian / Due Reviews) matching design -->
  <div class="flex items-center gap-8 border-b border-[var(--border-main)] px-1">
    <button 
      onclick={() => activeSubTab = 'saved'}
      class={`pb-3 text-sm transition-all cursor-pointer relative ${
        activeSubTab === 'saved' 
          ? 'text-[var(--accent-primary)] font-semibold' 
          : 'text-[var(--text-muted)] hover:text-[var(--text-main)] font-normal'
      }`}
    >
      <span>Saved & Obsidian</span>
      {#if activeSubTab === 'saved'}
        <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-[var(--accent-primary)] rounded-full"></div>
      {/if}
    </button>

    <button 
      onclick={() => activeSubTab = 'due'}
      class={`pb-3 text-sm transition-all cursor-pointer relative flex items-center gap-1.5 ${
        activeSubTab === 'due' 
          ? 'text-[var(--accent-primary)] font-semibold' 
          : 'text-[var(--text-muted)] hover:text-[var(--text-main)] font-normal'
      }`}
    >
      <span>Due Reviews</span>
      {#if dueCount > 0}
        <span class="text-[11px] font-mono px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-700 font-bold">
          {dueCount}
        </span>
      {/if}
      {#if activeSubTab === 'due'}
        <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-[var(--accent-primary)] rounded-full"></div>
      {/if}
    </button>
  </div>

  <!-- Top Card: Obsidian Vault Info matching design -->
  <div class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-2xl shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
    <div class="space-y-1">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[var(--accent-primary)]"></span>
        <h2 class="font-serif text-xl sm:text-2xl font-bold text-[var(--text-main)] tracking-tight">
          Obsidian Vault
        </h2>
        <span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-[#eaf2ec] text-[#386848] border border-[#c4d9cb]/50 flex items-center gap-1">
          <span>Synced Vocab</span>
          <span>🌿</span>
        </span>
      </div>
      <p class="text-xs text-[var(--text-muted)] font-mono pl-4 truncate max-w-xl">
        Path: {config?.obsidian_vault_path || '/home/kienngo/Obsidian/ZederVault'}
      </p>
    </div>

    <!-- Right Top Buttons matching design -->
    <div class="flex items-center gap-2 shrink-0">
      <button
        onclick={() => activeSubTab = 'saved'}
        class={`px-4 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
          activeSubTab === 'saved'
            ? 'btn-forest shadow-xs'
            : 'bg-[var(--bg-inner)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-main)]'
        }`}
      >
        All Saved ({items.length})
      </button>

      <button
        onclick={() => activeSubTab = 'due'}
        class={`px-4 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border ${
          activeSubTab === 'due'
            ? 'btn-forest shadow-xs border-transparent'
            : 'border-[var(--border-main)] bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
        }`}
      >
        <Clock class="w-3.5 h-3.5" />
        <span>Due Reviews ({dueCount})</span>
      </button>

      <button
        onclick={loadObsidianData}
        class="p-2 rounded-xl bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] transition cursor-pointer shadow-xs"
        title="Refresh Obsidian Vault files"
      >
        <RefreshCw class={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
      </button>
    </div>
  </div>

  <!-- Row Controls: Item count + Sort + List/Grid toggle -->
  <div class="flex items-center justify-between pt-1">
    <div class="text-xs font-semibold text-[var(--text-muted)]">
      <strong class="text-[var(--text-main)] text-sm">{filteredItems.length}</strong> items
    </div>

    <div class="flex items-center gap-2">
      <!-- Sort Dropdown -->
      <div class="relative">
        <button
          onclick={() => sortOrder = sortOrder === 'newest' ? 'alphabetical' : 'newest'}
          class="px-3 py-1.5 rounded-xl border border-[var(--border-main)] bg-[var(--bg-card)] text-xs font-medium text-[var(--text-muted)] hover:text-[var(--text-main)] flex items-center gap-1.5 transition cursor-pointer shadow-2xs"
          title="Toggle sort order"
        >
          <ArrowUpDown class="w-3.5 h-3.5" />
          <span>Sort: {sortOrder === 'newest' ? 'Newest' : 'A-Z'}</span>
          <ChevronDown class="w-3 h-3 opacity-60" />
        </button>
      </div>

      <!-- Segmented List / Grid Toggle -->
      <div class="p-1 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] flex items-center gap-0.5 shadow-2xs">
        <button
          onclick={() => viewMode = 'list'}
          class={`px-2.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer flex items-center gap-1 ${
            viewMode === 'list'
              ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold'
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
          title="List View"
        >
          <List class="w-3.5 h-3.5" />
          <span>List</span>
        </button>
        <button
          onclick={() => viewMode = 'grid'}
          class={`px-2.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer flex items-center gap-1 ${
            viewMode === 'grid'
              ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold'
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
          title="Grid View"
        >
          <LayoutGrid class="w-3.5 h-3.5" />
          <span>Grid</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Loading State -->
  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 text-[var(--text-muted)] space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-[var(--accent-primary)]" />
      <p class="text-sm font-medium font-serif">Syncing with Obsidian Vault...</p>
    </div>
  {:else if filteredItems.length === 0}
    <div class="journal-card p-12 text-center rounded-2xl border border-[var(--border-main)] bg-[var(--bg-card)] space-y-3">
      <span class="text-3xl">📚</span>
      <h3 class="font-serif text-lg font-bold text-[var(--text-main)]">No words found in this view</h3>
      <p class="text-xs text-[var(--text-muted)] max-w-md mx-auto">
        Save vocabulary words from Learn or Dictionary tabs to your Obsidian Vault to track spaced review and build your personal lexicon.
      </p>
    </div>
  {:else if viewMode === 'list'}
    <!-- List Mode matching exact design row by row -->
    <div class="space-y-3">
      {#each filteredItems as item}
        <div class="journal-card p-4 sm:p-5 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-2xl shadow-xs transition-all hover:border-[var(--border-highlight)]">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-center">
            
            <!-- Col 1: Word & Topic (lg:col-span-3) -->
            <div class="lg:col-span-3 space-y-1">
              <div class="flex items-center gap-2 flex-wrap">
                <button
                  onclick={() => onNavigateToDictionary?.(item.word)}
                  class="font-serif text-lg font-bold text-[var(--text-main)] hover:text-[var(--accent-primary)] transition text-left cursor-pointer"
                >
                  {item.word}
                </button>
                {#if item.is_due}
                  <span class="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-amber-500/15 text-amber-700 border border-amber-500/30 flex items-center gap-1">
                    <span>SRS Due Today</span>
                    <span>🔥</span>
                  </span>
                {/if}
              </div>
              <p class="text-xs text-[var(--text-muted)] truncate">
                Topic: {item.topic_title || 'Daily Life & Social'}
              </p>
            </div>

            <!-- Col 2: Definition (lg:col-span-4) -->
            <div class="lg:col-span-4 text-xs sm:text-sm text-[var(--text-main)] leading-relaxed">
              <p class="line-clamp-2">{cleanString(item.definition_en)}</p>
            </div>

            <!-- Col 3: Next Review & Interval (lg:col-span-2) -->
            <div class="lg:col-span-2 space-y-0.5 text-xs text-[var(--text-muted)]">
              <div class="flex items-center gap-1 text-[10px] uppercase font-bold tracking-wider text-[var(--text-subtle)]">
                <Calendar class="w-3 h-3" />
                <span>Next Review</span>
              </div>
              <p class="text-[var(--accent-primary)] font-medium font-mono text-xs pl-4">
                {item.next_review || '2026-09-04'}
              </p>
              <p class="text-[11px] text-[var(--text-subtle)] pl-4">
                Interval: {item.interval || 1} day(s)
              </p>
            </div>

            <!-- Col 4: Action Icons & Review Dropdown (lg:col-span-3) -->
            <div class="lg:col-span-3 flex items-center justify-end gap-1.5 relative">
              <button
                onclick={() => handleOpenInObsidian(item.file_path)}
                class="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer"
                title="Open note in Obsidian"
              >
                <ExternalLink class="w-4 h-4" />
              </button>
              <button
                onclick={() => playTTS(item.word)}
                class="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer"
                title="Pronounce"
              >
                <Volume2 class="w-4 h-4" />
              </button>
              <button
                class="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer"
                title="More Options"
              >
                <MoreVertical class="w-4 h-4" />
              </button>

              <!-- Review Now ⌵ Dropdown matching image 2 -->
              <div class="relative">
                <button
                  onclick={(e) => toggleDropdown(item.word, e)}
                  class="px-3 py-1.5 rounded-xl border border-[var(--border-main)] bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-xs font-semibold text-[var(--text-main)] flex items-center gap-1.5 transition cursor-pointer shadow-2xs"
                >
                  <span>Review Now</span>
                  <ChevronDown class="w-3.5 h-3.5 text-[var(--text-muted)]" />
                </button>

                {#if openDropdownWord === item.word}
                  <!-- svelte-ignore a11y_click_events_have_key_events -->
                  <!-- svelte-ignore a11y_no_static_element_interactions -->
                  <div
                    onclick={(e) => e.stopPropagation()}
                    class="absolute right-0 top-full mt-1 w-36 bg-[var(--bg-card)] border border-[var(--border-main)] rounded-xl shadow-lg z-30 py-1.5 text-xs font-semibold space-y-0.5"
                  >
                    <button
                      onclick={() => { handleSrsRate(item, 1); openDropdownWord = null; }}
                      class="w-full text-left px-3 py-1.5 hover:bg-red-500/10 text-red-600 transition cursor-pointer flex items-center justify-between"
                    >
                      <span>Again</span>
                      <span class="text-[11px] font-mono opacity-80">(1d)</span>
                    </button>
                    <button
                      onclick={() => { handleSrsRate(item, 2); openDropdownWord = null; }}
                      class="w-full text-left px-3 py-1.5 hover:bg-amber-500/10 text-amber-700 transition cursor-pointer flex items-center justify-between"
                    >
                      <span>Hard</span>
                      <span class="text-[11px] font-mono opacity-80">(2d)</span>
                    </button>
                    <button
                      onclick={() => { handleSrsRate(item, 3); openDropdownWord = null; }}
                      class="w-full text-left px-3 py-1.5 hover:bg-blue-500/10 text-blue-600 transition cursor-pointer flex items-center justify-between"
                    >
                      <span>Good</span>
                      <span class="text-[11px] font-mono opacity-80">(4d)</span>
                    </button>
                    <button
                      onclick={() => { handleSrsRate(item, 4); openDropdownWord = null; }}
                      class="w-full text-left px-3 py-1.5 hover:bg-emerald-500/10 text-emerald-600 transition cursor-pointer flex items-center justify-between"
                    >
                      <span>Easy</span>
                      <span class="text-[11px] font-mono opacity-80">(7d)</span>
                    </button>
                    <hr class="my-1 border-[var(--border-main)]" />
                    <button
                      onclick={() => { handleDeleteWord(item.word); openDropdownWord = null; }}
                      class="w-full text-left px-3 py-1.5 hover:bg-red-500/10 text-slate-600 hover:text-red-600 transition cursor-pointer flex items-center gap-1.5"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                      <span>Delete</span>
                    </button>
                  </div>
                {/if}
              </div>
            </div>

          </div>
        </div>
      {/each}
    </div>
  {:else}
    <!-- Grid Mode -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each filteredItems as item}
        <div class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-2xl shadow-xs flex flex-col justify-between space-y-3">
          <div class="space-y-2">
            <div class="flex items-start justify-between gap-2">
              <button
                onclick={() => onNavigateToDictionary?.(item.word)}
                class="font-serif text-xl font-bold text-[var(--text-main)] hover:text-[var(--accent-primary)] transition text-left cursor-pointer"
              >
                {item.word}
              </button>
              {#if item.is_due}
                <span class="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-amber-500/15 text-amber-700 border border-amber-500/30">
                  Due 🔥
                </span>
              {/if}
            </div>

            <p class="text-xs text-[var(--text-main)] line-clamp-3 leading-relaxed">
              {cleanString(item.definition_en)}
            </p>
          </div>

          <div class="pt-3 border-t border-[var(--border-main)] flex items-center justify-between text-xs">
            <span class="text-[var(--text-muted)] font-mono">Interval: {item.interval || 1}d</span>
            
            <div class="flex items-center gap-1">
              <button
                onclick={() => handleOpenInObsidian(item.file_path)}
                class="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] transition cursor-pointer"
                title="Open in Obsidian"
              >
                <ExternalLink class="w-3.5 h-3.5" />
              </button>
              <button
                onclick={() => playTTS(item.word)}
                class="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] transition cursor-pointer"
                title="Pronounce"
              >
                <Volume2 class="w-3.5 h-3.5" />
              </button>
              <button
                onclick={() => handleDeleteWord(item.word)}
                class="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-red-600 transition cursor-pointer"
                title="Delete"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Footer Decorative Quote matching design bottom -->
  <div class="pt-8 pb-4 text-center">
    <div class="flex items-center justify-center gap-4 text-[var(--text-subtle)]">
      <div class="h-px bg-[var(--border-main)] w-24 sm:w-48"></div>
      <span class="font-serif italic text-sm tracking-wide text-[var(--text-muted)]">
        Keep learning, keep growing.
      </span>
      <div class="h-px bg-[var(--border-main)] w-24 sm:w-48"></div>
    </div>
  </div>

</div>
