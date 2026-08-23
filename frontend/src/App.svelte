<script lang="ts">
  import Navbar from './lib/components/Navbar.svelte';
  import VocabTab from './lib/tabs/VocabTab.svelte';
  import DictationTab from './lib/tabs/DictationTab.svelte';
  import ListeningTab from './lib/tabs/ListeningTab.svelte';
  import WritingTab from './lib/tabs/WritingTab.svelte';
  import ObsidianTab from './lib/tabs/ObsidianTab.svelte';
  import SettingsTab from './lib/tabs/SettingsTab.svelte';

  let currentTab = $state('vocab');
</script>

<div class="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-blue-500 selection:text-white">
  <!-- Top Navigation Bar -->
  <Navbar bind:activeTab={currentTab} />

  <!-- Main Content Body -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
    {#if currentTab === 'vocab'}
      <VocabTab />
    {:else if currentTab === 'dictation'}
      <DictationTab />
    {:else if currentTab === 'listening'}
      <ListeningTab />
    {:else if currentTab === 'writing'}
      <WritingTab />
    {:else if currentTab === 'obsidian'}
      <ObsidianTab />
    {:else if currentTab === 'settings'}
      <SettingsTab />
    {/if}
  </main>
</div>
