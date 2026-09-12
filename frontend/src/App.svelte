<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import Navbar from './lib/components/Navbar.svelte';
  import TodayTab from './lib/tabs/TodayTab.svelte';
  import PracticeHubTab from './lib/tabs/PracticeHubTab.svelte';
  import VocabTab from './lib/tabs/VocabTab.svelte';
  import DictionaryTab from './lib/tabs/DictionaryTab.svelte';
  import GrammarTab from './lib/tabs/GrammarTab.svelte';
  import DictationTab from './lib/tabs/DictationTab.svelte';
  import ListeningTab from './lib/tabs/ListeningTab.svelte';
  import WritingTab from './lib/tabs/WritingTab.svelte';
  import ObsidianTab from './lib/tabs/ObsidianTab.svelte';
  import SettingsTab from './lib/tabs/SettingsTab.svelte';
  import { GetWordCount, GetDailyVocab, GetDailyIdiom, GetSavedObsidianVocab } from '../wailsjs/go/main/App.js';
  import { getInitialThemeState, applyThemeState, type ColorMode, type ThemePalette } from './lib/utils/theme';
  import { markToday, getStreak } from './lib/utils/daily';

  // Bật log debug navigation: localStorage vaultlingo_debug_nav = '1'
  const NAV_DEBUG = (() => {
    try {
      return localStorage.getItem('vaultlingo_debug_nav') === '1';
    } catch {
      return false;
    }
  })();

  type Area = 'today' | 'dictionary' | 'learn' | 'practice' | 'library' | 'settings';

  const defaults: Record<Area, string> = {
    today: 'today',
    dictionary: 'dictionary',
    learn: 'vocab',
    practice: 'hub',
    library: 'obsidian',
    settings: 'settings'
  };

  const subnav: Partial<Record<Area, { id: string; label: string }[]>> = {
    practice: [
      { id: 'hub', label: 'Overview' },
      { id: 'dictation', label: 'Dictation' },
      { id: 'listening', label: 'Listening' },
      { id: 'grammar', label: 'Grammar' },
      { id: 'writing', label: 'Writing Lab' }
    ],
    library: [
      { id: 'obsidian', label: 'Saved & Obsidian' }
    ]
  };

  let activeArea = $state<Area>('today');
  let currentView = $state('today');
  let dictionaryInitialWord = $state('resilience');
  let palette = $state<ThemePalette>('editorial');
  let colorMode = $state<ColorMode>('light');
  let dictionaryWordCount = $state<number | null>(null);
  let dueCount = $state(0);
  let savedCount = $state(0);
  let dayStreak = $state(0);
  let idiom = $state<any>(null);

  interface NavEntry { area: Area; view: string; word: string; scrollY: number; }
  let navHistory = $state<NavEntry[]>([]);
  let viewDirection = $state<1 | -1>(1);
  let canGoBack = $derived(navHistory.length > 0);

  function snapshot(): NavEntry {
    return { area: activeArea, view: currentView, word: dictionaryInitialWord, scrollY: window.scrollY || 0 };
  }

  function pushHistory() {
    const cur = snapshot();
    const last = navHistory[navHistory.length - 1];
    if (last && last.area === cur.area && last.view === cur.view && last.word === cur.word) return;
    navHistory.push(cur);
    if (navHistory.length > 50) navHistory.shift();
  }

  function smoothTop() {
    requestAnimationFrame(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  async function refreshDictionaryWordCount() {
    try {
      dictionaryWordCount = await GetWordCount();
    } catch (e) {
      console.warn(e);
    }
  }

  function selectArea(area: string) {
    if (area === activeArea) return;
    pushHistory();
    viewDirection = 1;
    activeArea = area as Area;
    currentView = defaults[activeArea];
    markToday();
    dayStreak = getStreak();
    smoothTop();
  }

  function selectView(view: string) {
    if (view === currentView) return;
    pushHistory();
    viewDirection = 1;
    currentView = view;
    if (view === 'dictation') markToday('dictation');
    if (view === 'listening') markToday('listening');
    if (view === 'vocab') markToday('review');
    smoothTop();
  }

  function navigateTo(area: string, view?: string) {
    const nextView = view || defaults[area as Area];
    if (area === activeArea && nextView === currentView) return;
    pushHistory();
    viewDirection = 1;
    activeArea = area as Area;
    currentView = nextView;
    markToday();
    if (currentView === 'dictation') markToday('dictation');
    if (currentView === 'listening') markToday('listening');
    if (currentView === 'vocab') markToday('review');
    dayStreak = getStreak();
    smoothTop();
  }

  function openDictionary(word: string) {
    if (activeArea === 'dictionary' && currentView === 'dictionary' && word === dictionaryInitialWord) return;
    pushHistory();
    viewDirection = 1;
    dictionaryInitialWord = word;
    activeArea = 'dictionary';
    currentView = 'dictionary';
    smoothTop();
  }

  async function goBack() {
    const now = Date.now();
    // Chống double-back: XF86Back vừa bắn keydown vừa bắn popstate
    if (now - lastBackAt < 350) return;
    lastBackAt = now;
    const prev = navHistory.pop();
    if (!prev) return;
    viewDirection = -1;
    activeArea = prev.area;
    currentView = prev.view;
    dictionaryInitialWord = prev.word;
    await tick();
    window.scrollTo({ top: prev.scrollY, behavior: 'smooth' });
  }
  let lastBackAt = 0;

  function isEditableTarget(t: EventTarget | null): boolean {
    if (!(t instanceof HTMLElement)) return false;
    const tag = t.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true;
    if (t.isContentEditable) return true;
    return false;
  }

  function toggleMode() {
    colorMode = colorMode === 'dark' ? 'light' : 'dark';
    applyThemeState({ palette, colorMode });
  }

  onMount(() => {
    const initial = getInitialThemeState();
    palette = initial.palette;
    colorMode = initial.colorMode;
    applyThemeState(initial);
    markToday();
    dayStreak = getStreak();
    refreshDictionaryWordCount();

    function onKey(e: KeyboardEvent) {
      const k = e.key as string;
      const kc = (e as KeyboardEvent).keyCode;
      if (NAV_DEBUG) console.debug('[nav] keydown', JSON.stringify(k), kc);
      // Linux/X11: nhiều chuột gửi XF86Back (BrowserBack, keyCode 166)
      // thay vì mouse-button. Browser tự dịch thành Back, app phải tự nghe.
      if (k === 'BrowserBack' || k === 'XF86Back' || kc === 166) {
        e.preventDefault();
        goBack();
        return;
      }
      // Alt+← : back mọi lúc (kể cả đang gõ)
      if (e.altKey && e.key === 'ArrowLeft') {
        e.preventDefault();
        goBack();
        return;
      }
      // Backspace : back chỉ khi KHÔNG typing (tránh nuốt chữ)
      if (
        e.key === 'Backspace' &&
        !e.ctrlKey && !e.metaKey && !e.altKey &&
        !isEditableTarget(e.target)
      ) {
        e.preventDefault();
        goBack();
      }
    }

    function onMouse(e: MouseEvent) {
      // Nút hông chuột: Back (3/8) / Forward (4/9).
      // Dùng capture + chặn cả mousedown/mouseup/auxclick vì
      // WebKit có thể nuốt event thành lệnh navigation thay vì mousedown.
      const b = (e as MouseEvent).button;
      if (NAV_DEBUG) console.debug('[nav] mouse', e.type, b);
      if (b === 3 || (b as number) === 8) {
        e.preventDefault();
        e.stopPropagation();
        goBack();
      }
    }

    function onPop() {
      // Fallback quan trọng: nhiều trình duyệt/WebKit biến nút Back
      // chuột thành browser-back (popstate) thay vì mousedown.
      // Re-push để giữ trap, rồi back trong app.
      if (NAV_DEBUG) console.debug('[nav] popstate');
      try {
        history.pushState({ vl: 'trap' }, '');
      } catch {}
      goBack();
    }

    window.addEventListener('keydown', onKey);
    // capture=true để chặn trước khi WebKit biến thành navigation
    window.addEventListener('mousedown', onMouse, true);
    window.addEventListener('mouseup', onMouse, true);
    window.addEventListener('auxclick', onMouse, true);
    window.addEventListener('popstate', onPop);
    try {
      history.pushState({ vl: 'trap' }, '');
    } catch {}

    (async () => {
      try {
        const [due, dailyIdiom, saved] = await Promise.all([
          GetDailyVocab('due_srs', 10),
          GetDailyIdiom(),
          GetSavedObsidianVocab().catch(() => [])
        ]);
        dueCount = due?.length || 0;
        idiom = dailyIdiom;
        savedCount = (saved as any[])?.length || 0;
      } catch (e) {
        console.warn(e);
      }
    })();

    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('mousedown', onMouse, true);
      window.removeEventListener('mouseup', onMouse, true);
      window.removeEventListener('auxclick', onMouse, true);
      window.removeEventListener('popstate', onPop);
    };
  });
</script>

<div class="min-h-screen flex flex-col app-container transition-colors duration-200">
  <Navbar 
    {activeArea} 
    {colorMode} 
    {dayStreak}
    {canGoBack}
    onSelectArea={selectArea} 
    onToggleColorMode={toggleMode}
    onGoBack={goBack}
    onOpenSearch={() => openDictionary('resilience')}
  />

  {#if subnav[activeArea]}
    <div class="border-b border-[var(--border-main)] bg-[var(--bg-inner)]/50 backdrop-blur-sm">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex gap-1.5 overflow-x-auto py-1.5">
        {#each subnav[activeArea] || [] as item}
          {@const isSelected = currentView === item.id}
          <button 
            onclick={() => selectView(item.id)} 
            class={`px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-all cursor-pointer ${
              isSelected 
                ? 'bg-[var(--accent-primary)] text-white shadow-sm font-semibold' 
                : 'text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--accent-primary-light)]'
            }`}
          >
            {item.label}
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <main class="flex-1 w-full p-4 sm:p-6 lg:p-8 overflow-x-clip">
    {#key currentView + '|' + activeArea + '|' + dictionaryInitialWord}
      <div
        class="view-smooth"
        in:fly={{ x: 36 * viewDirection, duration: 220, easing: cubicOut, opacity: 0 }}
      >
    {#if currentView === 'today'}
      <TodayTab 
        {dueCount}
        {savedCount}
        {dayStreak}
        {idiom} 
        onNavigate={navigateTo} 
        onOpenWord={openDictionary} 
      />
    {:else if currentView === 'hub'}
      <PracticeHubTab 
        {dueCount}
        {savedCount}
        onSelectPracticeTab={(tabId) => selectView(tabId)} 
      />
    {:else if currentView === 'vocab'}
      <VocabTab onNavigateToDictionary={openDictionary} />
    {:else if currentView === 'dictionary'}
      {#key dictionaryInitialWord}
      <DictionaryTab 
        initialWord={dictionaryInitialWord} 
        wordCount={dictionaryWordCount} 
        onWordStored={refreshDictionaryWordCount} 
      />
      {/key}
    {:else if currentView === 'dictation'}
      <DictationTab />
    {:else if currentView === 'listening'}
      <ListeningTab />
    {:else if currentView === 'grammar'}
      <GrammarTab />
    {:else if currentView === 'writing'}
      <WritingTab onNavigateTab={(tab) => navigateTo(tab)} />
    {:else if currentView === 'obsidian'}
      <ObsidianTab onNavigateToDictionary={openDictionary} />
    {:else if currentView === 'settings'}
      <SettingsTab />
    {/if}
      </div>
    {/key}
  </main>
</div>
