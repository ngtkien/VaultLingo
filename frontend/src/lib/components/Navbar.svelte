<script lang="ts">
  import { CalendarDays, BookOpen, BookA, Headphones, LibraryBig, Settings, Moon, Sun } from 'lucide-svelte';
  import pegasusLogo from '../../assets/images/pegasus-logo.png';
  import type { ColorMode } from '../utils/theme';
  let { activeArea, colorMode, onSelectArea, onToggleColorMode } = $props<{ activeArea: string; colorMode: ColorMode; onSelectArea: (area: string) => void; onToggleColorMode: () => void; }>();
  const areas = [{ id: 'today', label: 'Today', icon: CalendarDays }, { id: 'dictionary', label: 'Dictionary', icon: BookA }, { id: 'learn', label: 'Learn', icon: BookOpen }, { id: 'practice', label: 'Practice', icon: Headphones }, { id: 'library', label: 'Library', icon: LibraryBig }];
</script>
<header class="theme-header sticky top-0 z-50 border-b">
  <div class="w-full h-16 px-4 sm:px-6 lg:px-8 flex items-center gap-4">
    <button onclick={() => onSelectArea('today')} class="flex items-center gap-2.5 shrink-0 text-left cursor-pointer"><img src={pegasusLogo} alt="VaultLingo" class="w-9 h-9 rounded-lg object-cover ring-1 ring-cyan-400/30" /><div class="hidden sm:block"><h1 class="text-base font-bold text-slate-100">VaultLingo <span class="text-[10px] font-medium text-slate-500">v0.1.7</span></h1><p class="text-[10px] text-slate-400">English, every day</p></div></button>
    <nav class="flex min-w-0 flex-1 items-center gap-1 overflow-x-auto">{#each areas as area}{@const Icon = area.icon}<button onclick={() => onSelectArea(area.id)} class={`shrink-0 px-3 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2 cursor-pointer ${activeArea === area.id ? 'bg-cyan-500/15 text-cyan-300' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'}`}><Icon class="w-4 h-4" /><span>{area.label}</span></button>{/each}</nav>
    <div class="flex gap-1 shrink-0"><button onclick={() => onSelectArea('settings')} class={`p-2 rounded-lg cursor-pointer ${activeArea === 'settings' ? 'bg-cyan-500/15 text-cyan-300' : 'text-slate-400 hover:bg-slate-800'}`} title="Settings"><Settings class="w-4 h-4" /></button><button onclick={onToggleColorMode} class="p-2 rounded-lg text-slate-400 hover:bg-slate-800 cursor-pointer" title="Toggle light and dark mode">{#if colorMode === 'dark'}<Sun class="w-4 h-4" />{:else}<Moon class="w-4 h-4" />{/if}</button></div>
  </div>
</header>
