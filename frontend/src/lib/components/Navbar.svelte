<script lang="ts">
  import { BookOpen, Headphones, MessageSquare, PenTool, FolderSync, Settings, Sun, Moon } from 'lucide-svelte';
  import pegasusLogo from '../../assets/images/pegasus-logo.png';
  import type { Theme } from '../utils/theme';

  let { 
    activeTab = $bindable('vocab'),
    theme = 'dark',
    onToggleTheme
  } = $props<{ 
    activeTab: string;
    theme: Theme;
    onToggleTheme?: () => void;
  }>();

  const tabs = [
    { id: 'vocab', label: 'Vocabulary', icon: BookOpen },
    { id: 'dictation', label: 'Dictation', icon: Headphones },
    { id: 'listening', label: '75 Topics', icon: MessageSquare },
    { id: 'writing', label: 'AI Writing', icon: PenTool },
    { id: 'obsidian', label: 'Obsidian Vault', icon: FolderSync },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];
</script>

<header class={`border-b backdrop-blur-2xl sticky top-0 z-50 select-none shadow-xl transition-colors duration-200 ${
  theme === 'dark'
    ? 'bg-slate-950/85 border-slate-800/80 text-slate-100'
    : 'bg-white/90 border-slate-200 text-slate-900'
}`}>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
    <!-- Brand Logo with Cute Anime Pegasus -->
    <div class="flex items-center gap-3">
      <div class="relative group">
        <div class="absolute -inset-1 rounded-2xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 opacity-60 blur-sm group-hover:opacity-100 transition duration-300"></div>
        <img
          src={pegasusLogo}
          alt="VaultLingo Pegasus"
          class="relative w-10 h-10 rounded-xl object-cover ring-1 ring-cyan-400/40 shadow-lg shadow-cyan-500/20"
        />
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-lg font-black tracking-tight bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
            VaultLingo
          </h1>
          <span class="px-1.5 py-0.2 rounded-full text-[9px] font-bold font-mono bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-400 border border-cyan-500/30">
            v0.0.1
          </span>
        </div>
        <p class={`text-[10px] font-medium ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>
          Daily AI English & Obsidian Vault Sync
        </p>
      </div>
    </div>

    <!-- Right Controls: Navigation Tabs & Day/Night Toggle -->
    <div class="flex items-center gap-2">
      <!-- Navigation Tabs -->
      <nav class={`flex items-center gap-1 p-1 rounded-xl border transition-colors ${
        theme === 'dark'
          ? 'bg-slate-900/90 border-slate-800/80'
          : 'bg-slate-100 border-slate-200'
      }`}>
        {#each tabs as t}
          {@const Icon = t.icon}
          <button
            onclick={() => activeTab = t.id}
            class={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-2 cursor-pointer ${
              activeTab === t.id
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-md shadow-cyan-500/30 ring-1 ring-cyan-400/50'
                : theme === 'dark'
                ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/70'
            }`}
          >
            <Icon class="w-3.5 h-3.5" />
            <span>{t.label}</span>
          </button>
        {/each}
      </nav>

      <!-- Day / Night Theme Toggle Button -->
      <button
        onclick={onToggleTheme}
        class={`p-2 rounded-xl border transition-all shadow-md cursor-pointer flex items-center justify-center active:scale-95 ${
          theme === 'dark'
            ? 'bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-amber-300 border-slate-800/80'
            : 'bg-slate-100 hover:bg-slate-200 text-slate-700 hover:text-indigo-600 border-slate-200'
        }`}
        title={theme === 'dark' ? 'Switch to Light Mode (Day ☀️)' : 'Switch to Dark Mode (Night 🌙)'}
      >
        {#if theme === 'dark'}
          <Sun class="w-4 h-4 text-amber-400 animate-spin-slow" />
        {:else}
          <Moon class="w-4 h-4 text-indigo-600 animate-pulse" />
        {/if}
      </button>
    </div>
  </div>
</header>
