<script lang="ts">
  import { BookOpen, Headphones, MessageSquare, PenTool, FolderSync, Settings } from 'lucide-svelte';

  let { activeTab = $bindable('vocab') } = $props<{ activeTab: string }>();

  const tabs = [
    { id: 'vocab', label: 'Vocabulary', icon: BookOpen },
    { id: 'dictation', label: 'Dictation', icon: Headphones },
    { id: 'listening', label: '75 Topics', icon: MessageSquare },
    { id: 'writing', label: 'AI Writing', icon: PenTool },
    { id: 'obsidian', label: 'Obsidian Vault', icon: FolderSync },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];
</script>

<header class="bg-slate-950/80 border-b border-slate-800/80 backdrop-blur-xl sticky top-0 z-50 select-none">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
    <!-- Brand Logo with Pegasus (Thiên Mã) -->
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-violet-600 via-indigo-500 to-blue-500 flex items-center justify-center text-xl shadow-lg shadow-indigo-500/25 ring-1 ring-indigo-400/30">
        🦄
      </div>
      <div>
        <div class="flex items-center gap-1.5">
          <h1 class="text-lg font-black tracking-tight bg-gradient-to-r from-violet-400 via-indigo-300 to-blue-400 bg-clip-text text-transparent">
            VaultLingo
          </h1>
          <span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">v1.0</span>
        </div>
        <p class="text-[10px] text-slate-400 font-medium">Daily AI English & Obsidian Vault Sync</p>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <nav class="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800/80">
      {#each tabs as t}
        {@const Icon = t.icon}
        <button
          onclick={() => activeTab = t.id}
          class={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-2 cursor-pointer ${
            activeTab === t.id
              ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-md shadow-indigo-500/30 ring-1 ring-indigo-400/50'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Icon class="w-3.5 h-3.5" />
          <span>{t.label}</span>
        </button>
      {/each}
    </nav>
  </div>
</header>
