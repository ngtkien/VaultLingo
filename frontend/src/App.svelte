<script lang="ts">
  import { onMount } from 'svelte';
  import Navbar from './lib/components/Navbar.svelte';
  import VocabTab from './lib/tabs/VocabTab.svelte';
  import DictationTab from './lib/tabs/DictationTab.svelte';
  import ListeningTab from './lib/tabs/ListeningTab.svelte';
  import WritingTab from './lib/tabs/WritingTab.svelte';
  import ObsidianTab from './lib/tabs/ObsidianTab.svelte';
  import SettingsTab from './lib/tabs/SettingsTab.svelte';
  import { getInitialTheme, applyTheme, type Theme } from './lib/utils/theme';

  let currentTab = $state('vocab');
  let currentTheme = $state<Theme>('dark');

  function handleThemeToggle() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme);
  }

  onMount(() => {
    currentTheme = getInitialTheme();
    applyTheme(currentTheme);
  });
</script>

<div class={`min-h-screen flex flex-col transition-colors duration-200 ${currentTheme === 'dark' ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'}`}>
  <!-- Top Navigation Bar with Theme Switcher -->
  <Navbar
    bind:activeTab={currentTab}
    theme={currentTheme}
    onToggleTheme={handleThemeToggle}
  />

  <!-- Main Content Body -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
    {#if currentTab === 'vocab'}
      <VocabTab />
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
