<script lang="ts">
  import { 
    BookOpen, 
    BookA, 
    Headphones, 
    MessageSquare, 
    PenTool, 
    FolderSync, 
    Settings, 
    Sun, 
    Moon, 
    Palette, 
    Check, 
    ChevronDown 
  } from 'lucide-svelte';
  import pegasusLogo from '../../assets/images/pegasus-logo.png';
  import { THEME_PALETTES, type ColorMode, type StyleMode, type ThemePalette } from '../utils/theme';

  let { 
    activeTab = $bindable('vocab'),
    palette = 'default',
    colorMode = 'dark',
    styleMode = 'normal',
    onSelectPalette,
    onToggleColorMode,
    onToggleStyleMode
  } = $props<{ 
    activeTab: string;
    palette: ThemePalette;
    colorMode: ColorMode;
    styleMode: StyleMode;
    onSelectPalette?: (palette: ThemePalette) => void;
    onToggleColorMode?: () => void;
    onToggleStyleMode?: () => void;
  }>();

  let paletteDropdownOpen = $state(false);

  const tabs = [
    { id: 'vocab', label: 'Vocabulary', icon: BookOpen },
    { id: 'dictionary', label: 'Dictionary', icon: BookA },
    { id: 'dictation', label: 'Dictation', icon: Headphones },
    { id: 'listening', label: '75 Topics', icon: MessageSquare },
    { id: 'writing', label: 'AI Writing', icon: PenTool },
    { id: 'obsidian', label: 'Obsidian Vault', icon: FolderSync },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  function handleChoosePalette(pId: ThemePalette) {
    onSelectPalette?.(pId);
    paletteDropdownOpen = false;
  }
</script>

<header class="theme-header border-b backdrop-blur-2xl sticky top-0 z-50 select-none shadow-xl transition-colors duration-200">
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
            v0.1.0
          </span>
        </div>
        <p class={`text-[10px] font-medium ${colorMode === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>
          Daily AI English & Obsidian Vault Sync
        </p>
      </div>
    </div>

    <!-- Right Controls: Navigation Tabs, Palette Selector, Drawing Style & Day/Night Toggle -->
    <div class="flex items-center gap-2">
      <!-- Navigation Tabs -->
      <nav class={`flex items-center gap-1 p-1 rounded-xl border transition-colors ${
        colorMode === 'dark'
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
                : colorMode === 'dark'
                ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/70'
            }`}
          >
            <Icon class="w-3.5 h-3.5" />
            <span>{t.label}</span>
          </button>
        {/each}
      </nav>

      <!-- Palette Dropdown Button -->
      <div class="relative">
        <button
          onclick={() => paletteDropdownOpen = !paletteDropdownOpen}
          class={`px-2.5 py-1.5 rounded-xl border text-xs font-semibold transition-all shadow-md cursor-pointer flex items-center gap-1.5 active:scale-95 ${
            colorMode === 'dark'
              ? 'bg-slate-900/90 hover:bg-slate-800 text-slate-300 border-slate-800/80'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-200'
          }`}
          title="Choose Theme Palette (Nord, Everforest, Catppuccin, etc.)"
        >
          <Palette class="w-3.5 h-3.5 text-cyan-400" />
          <span class="hidden md:inline capitalize">{palette}</span>
          <ChevronDown class="w-3 h-3 text-slate-400" />
        </button>

        {#if paletteDropdownOpen}
          <!-- Backdrop -->
          <!-- svelte-ignore a11y_click_events_have_key_events -->
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <div 
            class="fixed inset-0 z-40" 
            onclick={() => paletteDropdownOpen = false}
          ></div>

          <!-- Dropdown Menu -->
          <div class={`absolute right-0 mt-2 w-56 rounded-2xl p-2 shadow-2xl border z-50 backdrop-blur-xl animate-in fade-in zoom-in-95 duration-100 ${
            colorMode === 'dark'
              ? 'bg-slate-900/95 border-slate-800 text-slate-100'
              : 'bg-white/95 border-slate-200 text-slate-900'
          }`}>
            <div class="px-2.5 py-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
              Theme Palette
            </div>
            <div class="space-y-1 mt-1">
              {#each THEME_PALETTES as p}
                <button
                  onclick={() => handleChoosePalette(p.id)}
                  class={`w-full px-2.5 py-1.5 rounded-xl text-xs flex items-center justify-between transition cursor-pointer ${
                    palette === p.id
                      ? 'bg-cyan-500/20 text-cyan-400 font-bold border border-cyan-500/30'
                      : 'hover:bg-slate-800/50 text-slate-300'
                  }`}
                >
                  <div class="flex items-center gap-2">
                    <!-- 3-dot color preview -->
                    <div class="flex items-center -space-x-1">
                      <span class="w-3 h-3 rounded-full border border-slate-900/40" style={`background-color: ${p.colors.bg};`}></span>
                      <span class="w-3 h-3 rounded-full border border-slate-900/40" style={`background-color: ${p.colors.card};`}></span>
                      <span class="w-3 h-3 rounded-full border border-slate-900/40" style={`background-color: ${p.colors.accent};`}></span>
                    </div>
                    <span>{p.name}</span>
                  </div>
                  {#if palette === p.id}
                    <Check class="w-3.5 h-3.5 text-cyan-400" />
                  {/if}
                </button>
              {/each}
            </div>
          </div>
        {/if}
      </div>

      <!-- Drawing Mode Toggle Button -->
      <button
        onclick={onToggleStyleMode}
        class={`px-2.5 py-1.5 rounded-xl border text-xs font-semibold transition-all shadow-md cursor-pointer flex items-center gap-1.5 active:scale-95 ${
          styleMode === 'drawing'
            ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-amber-500/10'
            : colorMode === 'dark'
            ? 'bg-slate-900/90 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-800/80'
            : 'bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900 border-slate-200'
        }`}
        title={styleMode === 'drawing' ? 'Drawing / Excalidraw Style Active (Click for Normal Style)' : 'Normal Style Active (Click for Drawing / Excalidraw Style ✏️)'}
      >
        <PenTool class={`w-3.5 h-3.5 ${styleMode === 'drawing' ? 'text-amber-400' : ''}`} />
        <span class="hidden sm:inline">{styleMode === 'drawing' ? 'Drawing' : 'Normal'}</span>
      </button>

      <!-- Day / Night Mode Toggle Button -->
      <button
        onclick={onToggleColorMode}
        class={`p-2 rounded-xl border transition-all shadow-md cursor-pointer flex items-center justify-center active:scale-95 ${
          colorMode === 'dark'
            ? 'bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-amber-300 border-slate-800/80'
            : 'bg-slate-100 hover:bg-slate-200 text-slate-700 hover:text-indigo-600 border-slate-200'
        }`}
        title={colorMode === 'dark' ? 'Night Mode 🌙 (Click for Day Mode ☀️)' : 'Day Mode ☀️ (Click for Night Mode 🌙)'}
      >
        {#if colorMode === 'dark'}
          <Sun class="w-4 h-4 text-amber-400" />
        {:else}
          <Moon class="w-4 h-4 text-indigo-600" />
        {/if}
      </button>
    </div>
  </div>
</header>
