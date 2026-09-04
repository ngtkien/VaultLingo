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
    Bell
  } from 'lucide-svelte';
  import pegasusLogo from '../../assets/images/pegasus-logo.png';
  import type { ColorMode } from '../utils/theme';

  let { 
    activeArea, 
    colorMode, 
    onSelectArea, 
    onToggleColorMode,
    onOpenSearch
  } = $props<{ 
    activeArea: string; 
    colorMode: ColorMode; 
    dayStreak?: number;
    onSelectArea: (area: string) => void; 
    onToggleColorMode: () => void;
    onOpenSearch?: () => void;
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
    
    <!-- Brand / Title matching design -->
    <button 
      onclick={() => onSelectArea('today')} 
      class="flex items-center gap-3 shrink-0 text-left cursor-pointer group"
    >
      <div class="w-10 h-10 flex items-center justify-center shrink-0">
        <img src={pegasusLogo} alt="VaultLingo" class="w-full h-full object-contain filter contrast-125" />
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
      <!-- Quick Search -->
      <button 
        onclick={onOpenSearch || (() => onSelectArea('dictionary'))}
        class="p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer" 
        title="Search dictionary"
      >
        <Search class="w-4 h-4" />
      </button>

      <!-- Notification Bell -->
      <button 
        class="p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer" 
        title="Notifications"
      >
        <Bell class="w-4 h-4" />
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

      <!-- User Profile Avatar Pill (as in design) -->
      <div 
        class="w-8 h-8 rounded-full bg-[var(--bg-inner)] border border-[var(--border-main)] text-[var(--text-main)] font-semibold text-xs flex items-center justify-center ml-1 shadow-xs"
        title="Learner Profile"
      >
        Z
      </div>
    </div>

  </div>
</header>
