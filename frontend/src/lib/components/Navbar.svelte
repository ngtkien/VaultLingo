<script lang="ts">
  import { CalendarDays, BookOpen, BookA, Headphones, LibraryBig, Settings, Moon, Sun, ShieldCheck } from 'lucide-svelte';
  import editorialLogo from '../../assets/images/vaultlingo-app-icon.png';
  import type { ColorMode } from '../utils/theme';
  let { activeArea, colorMode, onSelectArea, onToggleColorMode } = $props<{ activeArea: string; colorMode: ColorMode; onSelectArea: (area: string) => void; onToggleColorMode: () => void; }>();
  const areas = [{ id: 'today', label: 'Today', icon: CalendarDays }, { id: 'dictionary', label: 'Dictionary', icon: BookA }, { id: 'learn', label: 'Learn', icon: BookOpen }, { id: 'practice', label: 'Practice', icon: Headphones }, { id: 'library', label: 'Library', icon: LibraryBig }];
</script>
<header class="journal-mobile-header lg:hidden"><button onclick={() => onSelectArea('today')} class="flex items-center gap-2 cursor-pointer"><img src={editorialLogo} alt="VaultLingo" class="w-8 h-8 rounded-lg object-cover"/><span class="font-serif text-lg">VaultLingo</span></button><div class="flex gap-1"><button onclick={() => onSelectArea('dictionary')} class="p-2"><BookA class="w-4 h-4"/></button><button onclick={onToggleColorMode} class="p-2">{#if colorMode === 'dark'}<Sun class="w-4 h-4"/>{:else}<Moon class="w-4 h-4"/>{/if}</button></div></header>
<aside class="journal-sidebar hidden lg:flex">
  <button onclick={() => onSelectArea('today')} class="flex items-center gap-3 text-left cursor-pointer"><img src={editorialLogo} alt="VaultLingo" class="w-11 h-11 rounded-xl object-cover"/><span><b class="block font-serif text-xl">VaultLingo</b><i class="text-xs text-stone-500">Editorial Language Journal</i></span></button>
  <div class="journal-local"><ShieldCheck class="w-4 h-4"/><span><b>Local-first</b><small>Your learning stays on your device.</small></span></div>
  <p class="journal-nav-label">Journal</p><nav class="space-y-1">{#each areas as area}{@const Icon=area.icon}<button onclick={() => onSelectArea(area.id)} class:journal-nav-active={activeArea===area.id} class="journal-nav"><Icon class="w-4 h-4"/><span>{area.label}</span></button>{/each}</nav>
  <div class="mt-auto"><p class="journal-nav-label">Preferences</p><button onclick={() => onSelectArea('settings')} class:journal-nav-active={activeArea==='settings'} class="journal-nav"><Settings class="w-4 h-4"/><span>Settings</span></button><button onclick={onToggleColorMode} class="journal-nav mt-1">{#if colorMode === 'dark'}<Sun class="w-4 h-4"/>{:else}<Moon class="w-4 h-4"/>{/if}<span>{colorMode === 'dark' ? 'Light journal' : 'Dark journal'}</span></button><p class="mt-6 text-xs text-emerald-700">● Vault connected</p></div>
</aside>
