<script lang="ts">
  import {
    Calendar,
    BookA,
    BookOpen,
    Headphones,
    Library,
    Settings,
    Moon,
    Sun,
    Search,
    ArrowLeft
  } from 'lucide-svelte';
  import vaultlingoMark from '../../assets/images/vaultlingo-mark-128.png';
  import type { ColorMode } from '../utils/theme';

  let {
    activeArea,
    colorMode,
    onSelectArea,
    onToggleColorMode,
    onOpenSearch,
    onGoBack,
    canGoBack = false,
    dayStreak = 0
  } = $props<{
    activeArea: string;
    colorMode: ColorMode;
    dayStreak?: number;
    onSelectArea: (area: string) => void;
    onToggleColorMode: () => void;
    onOpenSearch?: () => void;
    onGoBack?: () => void;
    canGoBack?: boolean;
  }>();

  // Exactly matching the design tabs and icons
  const navItems = [
    { id: 'today', label: 'Today', icon: Calendar },
    { id: 'dictionary', label: 'Dictionary', icon: BookA },
    { id: 'learn', label: 'Learn', icon: BookOpen },
    { id: 'practice', label: 'Practice', icon: Headphones },
    { id: 'library', label: 'Library', icon: Library }
  ];
</script>

<header class="theme-header sticky top-0 z-50 border-b border-[var(--border-main)] transition-colors duration-200 backdrop-blur-md bg-[var(--bg-main)]/95">
  <div class="w-full max-w-7xl mx-auto h-16 px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4">
    <div class="flex items-center gap-2 shrink-0">
    <!-- Back -->
    <button
      onclick={() => onGoBack?.()}
      disabled={!canGoBack}
      class="p-2 rounded-xl transition cursor-pointer disabled:opacity-25 disabled:cursor-default text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)]"
      title={canGoBack ? 'Back (Alt+← / Backspace / chuột nút Back)' : 'No previous view'}
      aria-label="Go back"
    >
      <ArrowLeft class="w-4 h-4" />
    </button>
    <!-- Brand / Title matching design -->
    <button
      onclick={() => onSelectArea('today')}
      class="flex items-center gap-3 text-left cursor-pointer group"
    >
      <div class="w-10 h-10 flex items-center justify-center shrink-0 overflow-hidden rounded-2xl border border-[var(--border-main)] bg-[var(--bg-inner)] shadow-xs">
        <img src={vaultlingoMark} alt="VaultLingo" class="w-full h-full object-cover" />
      </div>
      <div>
        <span class="font-serif text-xl sm:text-2xl font-bold tracking-tight text-[var(--text-main)] group-hover:text-[var(--accent-primary)] transition block leading-tight">
          VaultLingo
        </span>
        <p class="text-[11px] font-sans text-[var(--text-muted)] -mt-0.5">
          English, every day.
        </p>
      </div>
    </button>
    </div>

    <!-- Navigation Tabs with elegant design underline -->
    <nav class="flex items-center gap-1 sm:gap-2 h-16">
      {#each navItems as item}
        {@const Icon = item.icon}
        {@const isActive = activeArea === item.id}
        <button 
          onclick={() => onSelectArea(item.id)} 
          class={`relative h-full px-3.5 flex items-center gap-2 text-sm transition-all cursor-pointer ${
            isActive 
              ? 'text-[var(--accent-primary)] font-semibold' 
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)] font-normal'
          }`}
        >
          <Icon class="w-4 h-4" />
          <span>{item.label}</span>
          
          {#if isActive}
            <div class="absolute bottom-0 left-2 right-2 h-0.5 bg-[var(--accent-primary)] rounded-full"></div>
          {/if}
        </button>
      {/each}
    </nav>

    <!-- Right Utility Controls matching design -->
    <div class="flex items-center gap-1 sm:gap-1.5 shrink-0">
      {#if dayStreak > 0}
        <span class="hidden sm:flex mr-1 px-2.5 py-1 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-700 text-xs font-bold font-mono" title="Daily streak — open app every day to keep it">
          🔥 {dayStreak}
        </span>
      {/if}
      <!-- Quick Search -->
      <button 
        onclick={onOpenSearch || (() => onSelectArea('dictionary'))}
        class="p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer" 
        title="Search dictionary"
      >
        <Search class="w-4 h-4" />
      </button>

      <!-- Theme Switcher / Mode -->
      <button 
        onclick={onToggleColorMode} 
        class="p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer" 
        title="Toggle color theme"
      >
        {#if colorMode === 'dark'}
          <Sun class="w-4 h-4" />
        {:else}
          <Moon class="w-4 h-4" />
        {/if}
      </button>

      <!-- Settings -->
      <button 
        onclick={() => onSelectArea('settings')} 
        class={`p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer ${
          activeArea === 'settings' ? 'text-[var(--accent-primary)] bg-[var(--accent-primary-light)]' : ''
        }`}
        title="Application Settings"
      >
        <Settings class="w-4 h-4" />
      </button>
    </div>

  </div>
</header>
