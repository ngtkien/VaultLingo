<script lang="ts">
  import { onMount } from 'svelte';
  import { GetSavedObsidianVocab, UpdateObsidianSrsReview, DeleteWordFromObsidian, OpenInObsidian, GetConfig } from '../../../wailsjs/go/main/App.js';
  import { playTTS } from '../utils/audio';
  import { FolderSync, ExternalLink, RefreshCw, Volume2, Calendar, Clock, Layers, Trash2, BookA } from 'lucide-svelte';

  let { onNavigateToDictionary } = $props<{ onNavigateToDictionary?: (word: string) => void }>();

  let items = $state<any[]>([]);
  let config = $state<any>(null);
  let loading = $state(false);
  let filterMode = $state<'all' | 'due'>('all');
  let selectedTopic = $state('all');

  let filteredItems = $derived(
    items.filter(item => {
      if (filterMode === 'due' && !item.is_due) return false;
      if (selectedTopic !== 'all' && item.topic_key !== selectedTopic) return false;
      return true;
    })
  );

  let dueCount = $derived(
    items.filter(item => item.is_due).length
  );

  async function loadObsidianData() {
    loading = true;
    try {
      config = await GetConfig();
      items = await GetSavedObsidianVocab();
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

  onMount(() => {
    loadObsidianData();
  });
</script>

<div class="space-y-6">
  <!-- Top Stats & Vault Header -->
  <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center gap-3">
      <div class="p-3 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
        <FolderSync class="w-6 h-6" />
      </div>
      <div>
        <h3 class="text-lg font-bold text-slate-100">Obsidian Vault Synced Vocab</h3>
        <p class="text-xs text-slate-400 font-mono">
          Path: {config?.obsidian_vault_path || '~/Obsidian/ZederVault'}
        </p>
      </div>
    </div>

    <!-- Filters & Actions -->
    <div class="flex items-center gap-2">
      <!-- Filter Due vs All -->
      <div class="bg-slate-800 p-1 rounded-xl flex items-center gap-1 border border-slate-700">
        <button
          onclick={() => filterMode = 'all'}
          class={`px-3 py-1 text-xs font-semibold rounded-lg transition cursor-pointer ${
            filterMode === 'all' ? 'bg-purple-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          All Saved ({items.length})
        </button>
        <button
          onclick={() => filterMode = 'due'}
          class={`px-3 py-1 text-xs font-semibold rounded-lg transition cursor-pointer flex items-center gap-1 ${
            filterMode === 'due' ? 'bg-purple-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Clock class="w-3 h-3" />
          Due Reviews ({dueCount})
        </button>
      </div>

      <button
        onclick={loadObsidianData}
        class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer border border-slate-700"
        title="Rescan Obsidian Vault"
      >
        <RefreshCw class={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
      </button>
    </div>
  </div>

  <!-- Items List -->
  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-purple-500" />
      <p class="text-sm font-medium">Scanning Obsidian Vault Markdown files...</p>
    </div>
  {:else if filteredItems.length === 0}
    <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center space-y-3">
      <p class="text-base font-semibold text-slate-300">No saved vocabulary found in this view!</p>
      <p class="text-xs text-slate-500">
        Go to the <strong>Vocabulary</strong> tab and click <em>"Save to Obsidian"</em> to bookmark words directly into your Vault.
      </p>
    </div>
  {:else}
    <div class="grid gap-4">
      {#each filteredItems as item}
        <div class="bg-slate-900/70 border border-slate-800 hover:border-purple-500/40 rounded-2xl p-5 backdrop-blur-md transition space-y-3">
          <div class="flex items-start justify-between gap-4">
            <div>
              <div class="flex items-center gap-2">
                <button
                  onclick={() => onNavigateToDictionary?.(item.word)}
                  class="text-xl font-bold text-slate-100 hover:text-cyan-400 text-left transition cursor-pointer flex items-center gap-1.5 group/title"
                  title="Click to view in Smart Dictionary"
                >
                  <span>{item.word}</span>
                  <BookA class="w-3.5 h-3.5 opacity-0 group-hover/title:opacity-100 text-cyan-400 transition" />
                </button>
                {#if item.is_due}
                  <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 animate-pulse">
                    SRS Due Today 🔥
                  </span>
                {/if}
              </div>
              <div class="text-xs text-slate-500 mt-0.5">
                Topic: {item.topic_title || item.topic_key}
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2">
              <button
                onclick={() => onNavigateToDictionary?.(item.word)}
                class="p-2 rounded-xl bg-slate-800 hover:bg-cyan-600 text-slate-300 hover:text-white transition cursor-pointer"
                title="Look up in Smart Dictionary"
              >
                <BookA class="w-4 h-4" />
              </button>
              <button
                onclick={() => playTTS(item.word)}
                class="p-2 rounded-xl bg-slate-800 hover:bg-purple-600 text-slate-300 hover:text-white transition cursor-pointer"
                title="Pronounce"
              >
                <Volume2 class="w-4 h-4" />
              </button>
              <button
                onclick={() => handleOpenInObsidian(item.file_path)}
                class="px-3 py-1.5 rounded-xl bg-purple-600/20 hover:bg-purple-600 text-purple-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border border-purple-500/30"
                title="Open Markdown file in Obsidian"
              >
                <span>Open in Obsidian</span>
                <ExternalLink class="w-3.5 h-3.5" />
              </button>
              <button
                onclick={() => handleDeleteWord(item.word)}
                class="p-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 border border-red-500/30 transition cursor-pointer"
                title="Delete from Obsidian Vault"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>

          {#if item.definition}
            <p class="text-sm text-slate-300 bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              {item.definition}
            </p>
          {/if}

          <!-- SRS Review Controls -->
          <div class="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs">
            <div class="text-slate-400 flex items-center gap-3">
              <span class="flex items-center gap-1">
                <Calendar class="w-3 h-3 text-slate-500" />
                Next Review: {item.next_review || 'Not set'}
              </span>
              <span>Interval: {item.interval || 1} day(s)</span>
            </div>

            <!-- Rating buttons -->
            <div class="flex items-center gap-1.5">
              <button
                onclick={() => handleSrsRate(item, 1)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 transition cursor-pointer"
              >
                Again (1d)
              </button>
              <button
                onclick={() => handleSrsRate(item, 2)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 border border-amber-500/20 transition cursor-pointer"
              >
                Hard (2d)
              </button>
              <button
                onclick={() => handleSrsRate(item, 3)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20 transition cursor-pointer"
              >
                Good (4d)
              </button>
              <button
                onclick={() => handleSrsRate(item, 4)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/20 transition cursor-pointer"
              >
                Easy (7d)
              </button>
              <button
                onclick={() => handleDeleteWord(item.word)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 transition cursor-pointer flex items-center gap-1"
                title="Delete from Vault"
              >
                <Trash2 class="w-3 h-3" />
                <span>Delete</span>
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
