<script lang="ts">
  import { onMount } from 'svelte';
  import Navbar from './lib/components/Navbar.svelte';
  import TodayTab from './lib/tabs/TodayTab.svelte';
  import PracticeHubTab from './lib/tabs/PracticeHubTab.svelte';
  import VocabTab from './lib/tabs/VocabTab.svelte';
  import DictionaryTab from './lib/tabs/DictionaryTab.svelte';
  import GrammarTab from './lib/tabs/GrammarTab.svelte';
  import DictationTab from './lib/tabs/DictationTab.svelte';
  import ListeningTab from './lib/tabs/ListeningTab.svelte';
  import WritingTab from './lib/tabs/WritingTab.svelte';
  import ObsidianTab from './lib/tabs/ObsidianTab.svelte';
  import SettingsTab from './lib/tabs/SettingsTab.svelte';
  import { GetWordCount, GetDailyVocab, GetDailyIdiom } from '../wailsjs/go/main/App.js';
  import { getInitialThemeState, applyThemeState, type ColorMode, type ThemePalette } from './lib/utils/theme';

  type Area = 'today' | 'dictionary' | 'learn' | 'practice' | 'library' | 'settings';

  const defaults: Record<Area, string> = {
    today: 'today',
    dictionary: 'dictionary',
    learn: 'vocab',
    practice: 'hub',
    library: 'obsidian',
    settings: 'settings'
  };

  const subnav: Partial<Record<Area, { id: string; label: string }[]>> = {
    practice: [
      { id: 'hub', label: 'Overview' },
      { id: 'dictation', label: 'Dictation' },
      { id: 'listening', label: 'Listening' },
      { id: 'grammar', label: 'Grammar' },
      { id: 'writing', label: 'Writing Lab' }
    ],
    library: [
      { id: 'obsidian', label: 'Saved & Obsidian' }
    ]
  };

  let activeArea = $state<Area>('today');
  let currentView = $state('today');
  let dictionaryInitialWord = $state('resilience');
  let palette = $state<ThemePalette>('editorial');
  let colorMode = $state<ColorMode>('light');
  let dictionaryWordCount = $state<number | null>(null);
  let dueCount = $state(18);
  let idiom = $state<any>(null);

  async function refreshDictionaryWordCount() {
    try {
      dictionaryWordCount = await GetWordCount();
    } catch (e) {
      console.warn(e);
    }
  }

  function selectArea(area: string) {
    activeArea = area as Area;
    currentView = defaults[activeArea];
  }

  function selectView(view: string) {
    currentView = view;
  }

  function navigateTo(area: string, view?: string) {
    activeArea = area as Area;
    currentView = view || defaults[activeArea];
  }

  function openDictionary(word: string) {
    dictionaryInitialWord = word;
    activeArea = 'dictionary';
    currentView = 'dictionary';
  }

  function toggleMode() {
    colorMode = colorMode === 'dark' ? 'light' : 'dark';
    applyThemeState({ palette, colorMode });
  }

  onMount(async () => {
    const initial = getInitialThemeState();
    palette = initial.palette;
    colorMode = initial.colorMode;
    applyThemeState(initial);
    refreshDictionaryWordCount();

    try {
      const [due, dailyIdiom] = await Promise.all([
        GetDailyVocab('due_srs', 10),
        GetDailyIdiom()
      ]);
      if (due && due.length > 0) {
        dueCount = due.length;
      }
      idiom = dailyIdiom;
    } catch (e) {
      console.warn(e);
    }
  });
</script>

<div class="min-h-screen flex flex-col app-container transition-colors duration-200">
  <Navbar 
    {activeArea} 
    {colorMode} 
    dayStreak={7}
    onSelectArea={selectArea} 
    onToggleColorMode={toggleMode}
    onOpenSearch={() => openDictionary('resilience')}
  />

  {#if subnav[activeArea]}
    <div class="border-b border-[var(--border-main)] bg-[var(--bg-inner)]/50 backdrop-blur-sm">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex gap-1.5 overflow-x-auto py-1.5">
        {#each subnav[activeArea] || [] as item}
          {@const isSelected = currentView === item.id}
          <button 
            onclick={() => selectView(item.id)} 
            class={`px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-all cursor-pointer ${
              isSelected 
                ? 'bg-[var(--accent-primary)] text-white shadow-sm font-semibold' 
                : 'text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)]'
            }`}
          >
            {item.label}
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <main class="flex-1 w-full p-4 sm:p-6 lg:p-8">
    {#if currentView === 'today'}
      <TodayTab 
        {dueCount} 
        {idiom} 
        onNavigate={navigateTo} 
        onOpenWord={openDictionary} 
      />
    {:else if currentView === 'hub'}
      <PracticeHubTab 
        onSelectPracticeTab={(tabId) => selectView(tabId)} 
      />
    {:else if currentView === 'vocab'}
      <VocabTab onNavigateToDictionary={openDictionary} />
    {:else if currentView === 'dictionary'}
      <DictionaryTab 
        initialWord={dictionaryInitialWord} 
        wordCount={dictionaryWordCount} 
        onWordStored={refreshDictionaryWordCount} 
      />
    {:else if currentView === 'dictation'}
      <DictationTab />
    {:else if currentView === 'listening'}
      <ListeningTab />
    {:else if currentView === 'grammar'}
      <GrammarTab />
    {:else if currentView === 'writing'}
      <WritingTab onNavigateTab={(tab) => navigateTo(tab)} />
    {:else if currentView === 'obsidian'}
      <ObsidianTab onNavigateToDictionary={openDictionary} />
    {:else if currentView === 'settings'}
      <SettingsTab />
    {/if}
  </main>
</div>
