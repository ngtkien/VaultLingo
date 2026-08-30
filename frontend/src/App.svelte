<script lang="ts">
  import { onMount } from 'svelte';
  import Navbar from './lib/components/Navbar.svelte';
  import VocabTab from './lib/tabs/VocabTab.svelte';
  import DictionaryTab from './lib/tabs/DictionaryTab.svelte';
  import DictationTab from './lib/tabs/DictationTab.svelte';
  import ListeningTab from './lib/tabs/ListeningTab.svelte';
  import WritingTab from './lib/tabs/WritingTab.svelte';
  import ObsidianTab from './lib/tabs/ObsidianTab.svelte';
  import SettingsTab from './lib/tabs/SettingsTab.svelte';
  import { getInitialThemeState, applyThemeState, type ColorMode, type StyleMode, type ThemePalette } from './lib/utils/theme';

  let currentTab = $state('vocab');
  let palette = $state<ThemePalette>('default');
  let colorMode = $state<ColorMode>('dark');
  let styleMode = $state<StyleMode>('normal');

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
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
    {#if currentTab === 'vocab'}
      <VocabTab />
    {:else if currentTab === 'dictionary'}
      <DictionaryTab />
    {:else if currentTab === 'dictation'}
      <DictationTab />
    {:else if currentTab === 'listening'}
      <ListeningTab />
    {:else if currentTab === 'writing'}
      <WritingTab onNavigateTab={(tab) => currentTab = tab} />
    {:else if currentTab === 'obsidian'}
      <ObsidianTab />
    {:else if currentTab === 'settings'}
      <SettingsTab />
    {/if}
  </main>
</div>
