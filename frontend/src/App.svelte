<script lang="ts">
  import { onMount } from 'svelte';
  import Navbar from './lib/components/Navbar.svelte';
  import VocabTab from './lib/tabs/VocabTab.svelte';
  import DictionaryTab from './lib/tabs/DictionaryTab.svelte';
  import GrammarTab from './lib/tabs/GrammarTab.svelte';
  import DictationTab from './lib/tabs/DictationTab.svelte';
  import ListeningTab from './lib/tabs/ListeningTab.svelte';
  import WritingTab from './lib/tabs/WritingTab.svelte';
  import ObsidianTab from './lib/tabs/ObsidianTab.svelte';
  import SettingsTab from './lib/tabs/SettingsTab.svelte';
  import { getInitialThemeState, applyThemeState, type ColorMode, type StyleMode, type ThemePalette } from './lib/utils/theme';
  import { GetWordCount } from '../wailsjs/go/main/App.js';

  let currentTab = $state('vocab');
  let dictionaryInitialWord = $state('serendipity');
  let palette = $state<ThemePalette>('default');
  let colorMode = $state<ColorMode>('dark');
  let styleMode = $state<StyleMode>('normal');
  let dictionaryWordCount = $state<number | null>(null);

  async function refreshDictionaryWordCount() {
    try {
      dictionaryWordCount = await GetWordCount();
    } catch (error) {
      console.warn('Could not load dictionary word count:', error);
    }
  }

  function handleNavigateToDictionary(word: string) {
    if (word && word.trim()) {
      dictionaryInitialWord = word.trim();
      currentTab = 'dictionary';
    }
  }

  function handleSelectPalette(newPalette: ThemePalette) {
    palette = newPalette;
    applyThemeState({ palette, colorMode, styleMode });
  }

  function handleToggleColorMode() {
    colorMode = colorMode === 'dark' ? 'light' : 'dark';
    applyThemeState({ palette, colorMode, styleMode });
  }

  function handleToggleStyleMode() {
    styleMode = styleMode === 'normal' ? 'drawing' : 'normal';
    applyThemeState({ palette, colorMode, styleMode });
  }

  onMount(() => {
    const initial = getInitialThemeState();
    palette = initial.palette;
    colorMode = initial.colorMode;
    styleMode = initial.styleMode;
    applyThemeState(initial);
    refreshDictionaryWordCount();
  });
</script>

<div class="min-h-screen flex flex-col app-container transition-colors duration-200">
  <!-- Top Navigation Bar with Theme & Style Switchers -->
  <Navbar
    bind:activeTab={currentTab}
    palette={palette}
    colorMode={colorMode}
    styleMode={styleMode}
    onSelectPalette={handleSelectPalette}
    onToggleColorMode={handleToggleColorMode}
    onToggleStyleMode={handleToggleStyleMode}
  />

  <!-- Main Content Body -->
  <main class="flex-1 w-full mx-auto p-4 sm:p-6 lg:p-8 2xl:px-12">
    {#if currentTab === 'vocab'}
      <VocabTab onNavigateToDictionary={handleNavigateToDictionary} />
    {:else if currentTab === 'dictionary'}
      <DictionaryTab
        initialWord={dictionaryInitialWord}
        wordCount={dictionaryWordCount}
        onWordStored={refreshDictionaryWordCount}
      />
    {:else if currentTab === 'grammar'}
      <GrammarTab />
    {:else if currentTab === 'dictation'}
      <DictationTab />
    {:else if currentTab === 'listening'}
      <ListeningTab />
    {:else if currentTab === 'writing'}
      <WritingTab onNavigateTab={(tab) => currentTab = tab} />
    {:else if currentTab === 'obsidian'}
      <ObsidianTab onNavigateToDictionary={handleNavigateToDictionary} />
    {:else if currentTab === 'settings'}
      <SettingsTab />
    {/if}
  </main>
</div>
