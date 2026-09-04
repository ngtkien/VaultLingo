<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    GetDailyVocab, 
    GetDailyIdiom, 
    GetQuickQuizExcluding,
    GetAvailableTopics, 
    SaveWordToObsidian, 
    SaveAllWordsToObsidian, 
    DeleteWordFromObsidian,
    RecordSrsReview 
  } from '../../../wailsjs/go/main/App.js';
  import { playTTS } from '../utils/audio';
  import WordPracticeModal from '../components/WordPracticeModal.svelte';
  import { 
    Volume2, 
    Bookmark, 
    RefreshCw, 
    Layers, 
    List,
    CheckCircle2, 
    XCircle, 
    ChevronLeft, 
    ChevronRight,
    ChevronDown,
    RotateCcw,
    BookA,
    Dices,
    PenTool,
    Zap,
    Lock,
    Unlock
  } from 'lucide-svelte';

  let { onNavigateToDictionary } = $props<{ onNavigateToDictionary?: (word: string) => void }>();

  const IDIOM_BANK = [
    {
      id: 1,
      idiom: 'Back to the drawing board',
      phonetic: '/bæk tə ðə ˈdrɔː.ɪŋ bɔːd/',
      meaning_en: 'To start planning something again because the previous plan failed.',
      meaning_vi: 'Làm lại từ đầu, lên lại kế hoạch từ con số không.',
      example: 'Our first design prototype was too expensive to manufacture, so it is back to the drawing board.'
    },
    {
      id: 2,
      idiom: 'Bite the bullet',
      phonetic: '/baɪt ðə ˈbʊl.ɪt/',
      meaning_en: 'To face a difficult or painful situation with courage and fortitude.',
      meaning_vi: 'Cắn răng chịu đựng, dũng cảm đương đầu với khó khăn không thể né tránh.',
      example: 'I decided to bite the bullet and have that tough conversation with my manager.'
    },
    {
      id: 3,
      idiom: 'Burn the midnight oil',
      phonetic: '/bɜːn ðə ˈmɪd.naɪt ɔɪl/',
      meaning_en: 'To work or study late into the night.',
      meaning_vi: 'Thức khuya miệt mài học tập hoặc làm việc đến tận đêm muộn.',
      example: 'She has been burning the midnight oil all week to finish the engineering thesis.'
    },
    {
      id: 4,
      idiom: 'Break the ice',
      phonetic: '/breɪk ði aɪs/',
      meaning_en: 'To say or do something that makes people feel relaxed in a social setting.',
      meaning_vi: 'Phá vỡ bầu không khí ngượng ngùng ban đầu, tạo sự cởi mở.',
      example: 'A lighthearted joke is a wonderful way to break the ice at new meetings.'
    },
    {
      id: 5,
      idiom: 'Call it a day',
      phonetic: '/kɔːl ɪt ə deɪ/',
      meaning_en: 'To stop working on something for the rest of the day.',
      meaning_vi: 'Tạm dừng công việc trong ngày, kết thúc một ngày làm việc.',
      example: 'We have made tremendous progress today; let us call it a day.'
    },
    {
      id: 6,
      idiom: 'Hit the nail on the head',
      phonetic: '/hɪt ðə neɪl ɒn ðə hed/',
      meaning_en: 'To describe exactly what is causing a situation or problem.',
      meaning_vi: 'Nói trúng phóc, chỉ ra đúng trọng tâm của vấn đề.',
      example: 'Her analysis hit the nail on the head regarding our app performance issue.'
    },
    {
      id: 7,
      idiom: 'Piece of cake',
      phonetic: '/piːs əv keɪk/',
      meaning_en: 'Something that is very easy to achieve or complete.',
      meaning_vi: 'Dễ như trở bàn tay, chuyện vô cùng đơn giản.',
      example: 'After months of practice, passing the driving exam was a piece of cake.'
    },
    {
      id: 8,
      idiom: 'Once in a blue moon',
      phonetic: '/wʌns ɪn ə bluː muːn/',
      meaning_en: 'Occurring very rarely or almost never.',
      meaning_vi: 'Năm thì mười họa, rất hiếm khi xảy ra.',
      example: 'He only visits his hometown once in a blue moon due to his busy schedule.'
    },
    {
      id: 9,
      idiom: 'Through thick and thin',
      phonetic: '/θruː θɪk ænd θɪn/',
      meaning_en: 'Under all circumstances, supporting each other through good and bad times.',
      meaning_vi: 'Cùng nhau trải qua mọi thăng trầm, hoạn nạn có nhau.',
      example: 'True friends stand by each other through thick and thin.'
    },
    {
      id: 10,
      idiom: 'Blessing in disguise',
      phonetic: '/ˈbles.ɪŋ ɪn dɪsˈɡaɪz/',
      meaning_en: 'An apparent misfortune that eventually has good or fortunate results.',
      meaning_vi: 'Trong cái rủi có cái may, họa hóa thành phúc.',
      example: 'Losing that old job turned out to be a blessing in disguise as I found my true passion.'
    }
  ];

  let words = $state<any[]>([]);
  let topics = $state<any[]>([]);
  let selectedTopic = $state('all');
  let idiomIndex = $state(0);
  let idiom = $state<any>(null);
  let quiz = $state<any>(null);
  let selectedQuizOption = $state('');
  let quizAnswered = $state(false);
  let seenQuizIds = $state<number[]>([]);
  let loading = $state(false);
  let savedWordsMap = $state<Record<string, boolean>>({});
  let activeViewMode = $state<'list' | 'flashcard'>('list');
  let currentCardIndex = $state(0);
  let cardFlipped = $state(false);
  let openSrsWordId = $state<number | null>(null);
  let practiceWord = $state<any>(null);
  let isPracticeModalOpen = $state(false);

  // Session persistence and topic scroll state
  const CACHE_KEY_WORDS = 'vaultlingo_learn_words';
  const CACHE_KEY_TOPIC = 'vaultlingo_learn_topic';
  const CACHE_KEY_LOCKED = 'vaultlingo_learn_locked';

  let topicScrollRef = $state<HTMLElement | null>(null);
  let canScrollLeft = $state(false);
  let canScrollRight = $state(false);
  let isLocked = $state(true);

  function updateScrollIndicators() {
    if (!topicScrollRef) return;
    canScrollLeft = topicScrollRef.scrollLeft > 10;
    canScrollRight = topicScrollRef.scrollLeft < topicScrollRef.scrollWidth - topicScrollRef.clientWidth - 10;
  }

  function scrollTopics(direction: 'left' | 'right') {
    if (topicScrollRef) {
      const offset = direction === 'left' ? -240 : 240;
      topicScrollRef.scrollBy({ left: offset, behavior: 'smooth' });
      setTimeout(updateScrollIndicators, 250);
    }
  }

  function handleTopicWheel(e: WheelEvent) {
    if (topicScrollRef && Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      e.preventDefault();
      topicScrollRef.scrollLeft += e.deltaY;
      updateScrollIndicators();
    }
  }

  function toggleLock() {
    isLocked = !isLocked;
    try {
      localStorage.setItem(CACHE_KEY_LOCKED, String(isLocked));
    } catch (e) {
      console.warn('Failed to save lock state', e);
    }
  }

  function openPracticeModal(w: any) {
    practiceWord = w;
    isPracticeModalOpen = true;
  }

  function closePracticeModal() {
    isPracticeModalOpen = false;
    practiceWord = null;
  }

  function cleanString(text: string | undefined | null): string {
    if (!text) return '';
    return text
      .replace(/:\s*:\s*id=[^"'\s]*/gi, '')
      .replace(/id=[a-zA-Z0-9._&=-]+/gi, '')
      .replace(/\s*\b\d{3,}\b\s*$/, '')
      .trim();
  }

    function formatExamplePairs(rawEn: string | undefined | null, rawVi: string | undefined | null): { en: string; vi: string }[] {
    if (!rawEn) return [];

    const en = cleanString(rawEn);
    const rawEnParts = en.split(/\s*[/|]\s*|\n+/).map(s => s.trim()).filter(Boolean);
    let enSents: string[] = [];
    for (const p of rawEnParts) {
      const sents = p.match(/[^.!?]+[.!?]/g);
      if (sents && sents.length > 0) {
        for (const s of sents) {
          const sc = s.trim();
          if (sc.length > 5) enSents.push(sc);
        }
      } else if (p.length > 5) {
        enSents.push(p.replace(/[.!?]*$/, "") + ".");
      }
    }

    const vi = cleanString(rawVi || "");
    const viRawParts = vi.split(/\s*[/|]\s*|\n+/).map(s => s.trim()).filter(Boolean);
    let viSents: string[] = [];
    for (const p of viRawParts) {
      const sents = p.match(/[^.!?]+[.!?]/g);
      if (sents && sents.length > 0 && viRawParts.length === 1 && enSents.length > 1) {
        for (const s of sents) {
          const sc = s.trim();
          if (sc.length > 3) viSents.push(sc);
        }
      } else if (p.length > 3) {
        viSents.push(p.trim());
      }
    }

    const maxCount = Math.min(enSents.length, 2);
    const pairs: { en: string; vi: string }[] = [];
    for (let i = 0; i < maxCount; i++) {
      pairs.push({
        en: enSents[i],
        vi: viSents[i] || ""
      });
    }

    if (pairs.length === 0 && en.length > 0) {
      pairs.push({ en, vi });
    }

    return pairs;
  }

  async function loadDailyIdiom() {
    idiom = await GetDailyIdiom();
  }

  function handleNextIdiom() {
    idiomIndex = (idiomIndex + 1) % IDIOM_BANK.length;
    idiom = IDIOM_BANK[idiomIndex];
  }

  async function loadNextQuiz() {
    const nextQuiz = await GetQuickQuizExcluding(seenQuizIds);
    quiz = nextQuiz;
    seenQuizIds = nextQuiz?.id ? [...seenQuizIds, nextQuiz.id] : [];
    selectedQuizOption = '';
    quizAnswered = false;
  }

  async function fetchWords(topicKey: string) {
    loading = true;
    try {
      words = await GetDailyVocab(topicKey, 5);
      currentCardIndex = 0;
      cardFlipped = false;
      openSrsWordId = null;
      try {
        localStorage.setItem(CACHE_KEY_WORDS, JSON.stringify(words));
        localStorage.setItem(CACHE_KEY_TOPIC, topicKey);
      } catch (err) {
        console.warn('Failed to save words to cache', err);
      }
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function handleRefresh() {
    await fetchWords(selectedTopic);
    await loadNextQuiz();
  }

  async function handleTopicChange(topicKey: string) {
    selectedTopic = topicKey;
    await fetchWords(topicKey);
  }

  async function handleSaveWord(word: any) {
    const key = word.word.toLowerCase();
    if (savedWordsMap[key]) {
      try {
        await DeleteWordFromObsidian(word.word);
        savedWordsMap[key] = false;
      } catch (e) {
        console.error(e);
      }
    } else {
      try {
        const res = await SaveWordToObsidian(word);
        if (res.success) {
          savedWordsMap[key] = true;
        }
      } catch (e) {
        console.error(e);
      }
    }
  }

  async function handleSaveAll() {
    try {
      const results = await SaveAllWordsToObsidian(words);
      for (const res of results) {
        if (res.success && res.word) {
          savedWordsMap[res.word.toLowerCase()] = true;
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function handleSrsRate(wordId: number, rating: number) {
    try {
      await RecordSrsReview(wordId, rating);
      openSrsWordId = null;
      if (activeViewMode === 'flashcard' && currentCardIndex < words.length - 1) {
        nextCard();
      }
    } catch (e) {
      console.error(e);
    }
  }

  function toggleSrsDropdown(wordId: number, e?: Event) {
    if (e) e.stopPropagation();
    openSrsWordId = openSrsWordId === wordId ? null : wordId;
  }

  function prevCard() {
    if (currentCardIndex > 0) {
      currentCardIndex--;
      cardFlipped = false;
    }
  }

  function nextCard() {
    if (currentCardIndex < words.length - 1) {
      currentCardIndex++;
      cardFlipped = false;
    }
  }

  function goToCard(idx: number) {
    currentCardIndex = idx;
    cardFlipped = false;
  }

  function playWord(word: string, slow = false) {
    playTTS(word, slow ? 0.75 : 1.0, word);
  }

  function handleKeydown(e: KeyboardEvent) {
    if (activeViewMode !== 'flashcard') return;
    if (e.key === 'ArrowLeft') {
      prevCard();
    } else if (e.key === 'ArrowRight') {
      nextCard();
    } else if (e.key === ' ' || e.key === 'Enter') {
      if (document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'TEXTAREA') return;
      e.preventDefault();
      cardFlipped = !cardFlipped;
    }
  }

  onMount(() => {
    async function init() {
      try {
        const savedLocked = localStorage.getItem(CACHE_KEY_LOCKED);
        isLocked = savedLocked !== null ? savedLocked === 'true' : true;
      } catch (e) {
        isLocked = true;
      }

      try {
        topics = await GetAvailableTopics();
        setTimeout(updateScrollIndicators, 150);
      } catch (e) {
        console.error('Failed to load topics', e);
      }

      let hasRestored = false;
      try {
        const cachedWordsRaw = localStorage.getItem(CACHE_KEY_WORDS);
        const cachedTopic = localStorage.getItem(CACHE_KEY_TOPIC);
        if (cachedWordsRaw) {
          const parsed = JSON.parse(cachedWordsRaw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            words = parsed;
            if (cachedTopic) {
              selectedTopic = cachedTopic;
            }
            hasRestored = true;
          }
        }
      } catch (e) {
        console.warn('Failed to restore cached words', e);
      }

      if (!hasRestored || !isLocked) {
        await fetchWords(selectedTopic);
      }

      await loadDailyIdiom();
      seenQuizIds = [];
      await loadNextQuiz();
    }

    init();

    window.addEventListener('keydown', handleKeydown);
    const closeDropdownOnOutside = () => { openSrsWordId = null; };
    window.addEventListener('click', closeDropdownOnOutside);
    window.addEventListener('resize', updateScrollIndicators);

    const scheduleNextDay = () => {
      const now = new Date();
      const next = new Date(now);
      next.setHours(24, 0, 2, 0);
      return window.setTimeout(async () => {
        await loadDailyIdiom();
        midnightTimer = scheduleNextDay();
      }, next.getTime() - now.getTime());
    };
    let midnightTimer = scheduleNextDay();

    return () => {
      window.removeEventListener('keydown', handleKeydown);
      window.removeEventListener('click', closeDropdownOnOutside);
      window.removeEventListener('resize', updateScrollIndicators);
      window.clearTimeout(midnightTimer);
    };
  });
</script>

<div class="max-w-6xl mx-auto space-y-6">
  <!-- Top Title & Subtitle matching design -->
  <div class="flex items-center justify-between">
    <div>
      <div class="flex items-center gap-2">
        <h1 class="font-serif text-3xl sm:text-4xl font-bold text-[var(--text-main)] tracking-tight">
          Vocabulary
        </h1>
        <span class="text-xl">🌿</span>
      </div>
      <p class="text-sm text-[var(--text-muted)] mt-1 font-sans">
        Build your words. Build your world.
      </p>
    </div>
  </div>

  <!-- Topic Filters Row: Deduplicated, smooth scrolling, navigation chevrons -->
  <div class="relative flex items-center max-w-full">
    {#if canScrollLeft}
      <button
        onclick={() => scrollTopics('left')}
        class="absolute left-0 z-20 p-1.5 rounded-full bg-[var(--bg-card)]/90 backdrop-blur-xs border border-[var(--border-main)] shadow-sm text-[var(--text-muted)] hover:text-[var(--accent-primary)] hover:border-[var(--accent-primary-border)] transition cursor-pointer"
        aria-label="Scroll topics left"
        title="Scroll left"
      >
        <ChevronLeft class="w-3.5 h-3.5" />
      </button>
    {/if}

    <div
      bind:this={topicScrollRef}
      onwheel={handleTopicWheel}
      onscroll={updateScrollIndicators}
      class="flex items-center gap-1.5 overflow-x-auto py-1 px-1 max-w-full no-scrollbar scroll-smooth"
    >
      <button
        onclick={() => handleTopicChange('all')}
        class={`pill-filter ${selectedTopic === 'all' ? 'active' : ''}`}
      >
        <span>🏷️</span>
        <span>All Topics</span>
      </button>
      {#each topics.filter(t => t.key !== 'all') as t}
        <button
          onclick={() => handleTopicChange(t.key)}
          class={`pill-filter ${selectedTopic === t.key ? 'active' : ''}`}
        >
          <span>{t.icon}</span>
          <span>{t.title}</span>
        </button>
      {/each}
    </div>

    {#if canScrollRight}
      <button
        onclick={() => scrollTopics('right')}
        class="absolute right-0 z-20 p-1.5 rounded-full bg-[var(--bg-card)]/90 backdrop-blur-xs border border-[var(--border-main)] shadow-sm text-[var(--text-muted)] hover:text-[var(--accent-primary)] hover:border-[var(--accent-primary-border)] transition cursor-pointer"
        aria-label="Scroll topics right"
        title="Scroll right"
      >
        <ChevronRight class="w-3.5 h-3.5" />
      </button>
    {/if}
  </div>

  <!-- Controls Bar: List/Flashcard segmented toggle + Save All + Lock + Refresh -->
  <div class="flex items-center justify-between gap-3 flex-wrap">
    <div class="flex items-center gap-2">
      <!-- Toggle List / Flashcard -->
      <div class="p-1 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] flex items-center gap-1 shadow-xs">
        <button
          onclick={() => activeViewMode = 'list'}
          class={`px-3 py-1.5 text-xs font-semibold rounded-lg transition cursor-pointer flex items-center gap-1.5 ${
            activeViewMode === 'list' 
              ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold' 
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <List class="w-3.5 h-3.5" />
          <span>List</span>
        </button>
        <button
          onclick={() => activeViewMode = 'flashcard'}
          class={`px-3 py-1.5 text-xs font-semibold rounded-lg transition cursor-pointer flex items-center gap-1.5 ${
            activeViewMode === 'flashcard' 
              ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold' 
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <Layers class="w-3.5 h-3.5" />
          <span>Flashcard</span>
        </button>
      </div>

      <!-- Save All to Obsidian -->
      <button
        onclick={handleSaveAll}
        class="px-3.5 py-1.5 rounded-xl text-xs font-semibold btn-forest flex items-center gap-1.5 shadow-sm transition cursor-pointer"
        title="Save all 5 words to Obsidian Vault"
      >
        <Bookmark class="w-3.5 h-3.5" />
        <span class="hidden sm:inline">Save All to Obsidian</span>
        <span class="sm:hidden">Save All</span>
      </button>
    </div>

    <!-- Right Controls: Lock Status Toggle + Refresh Word Set -->
    <div class="flex items-center gap-2">
      <!-- Lock Toggle -->
      <button
        onclick={toggleLock}
        class={`px-3 py-1.5 rounded-xl border text-xs font-semibold transition cursor-pointer flex items-center gap-1.5 shadow-xs ${
          isLocked 
            ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary-border)] text-[var(--accent-primary)] font-bold' 
            : 'bg-[var(--bg-card)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
        }`}
        title={isLocked 
          ? "Session is locked: words remain pinned when navigating between tabs. Only refresh or topic change will load new words." 
          : "Session is unlocked: words will randomize when navigating between tabs."}
      >
        {#if isLocked}
          <Lock class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
          <span>Locked</span>
        {:else}
          <Unlock class="w-3.5 h-3.5" />
          <span>Unlocked</span>
        {/if}
      </button>

      <!-- Refresh word set -->
      <button
        onclick={handleRefresh}
        class="px-3 py-1.5 rounded-xl bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer border border-[var(--border-main)] hover:border-[var(--accent-primary-border)] shadow-xs flex items-center gap-1.5"
        title="Shuffle and load a new set of 5 words for this topic"
      >
        <RefreshCw class={`w-3.5 h-3.5 ${loading ? 'animate-spin text-[var(--accent-primary)]' : ''}`} />
        <span class="text-xs font-semibold">Refresh</span>
      </button>
    </div>
  </div>

  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 text-[var(--text-muted)] space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-[var(--accent-primary)]" />
      <p class="text-sm font-medium font-serif">Curating vocabulary set...</p>
    </div>
  {:else if activeViewMode === 'list'}
    <!-- Word List View: SRS is listdown dropdown to maximize room for EXAMPLE -->
    <div class="space-y-3.5">
      {#each words as w, index}
        {@const examplePairs = formatExamplePairs(w.example_en, w.example_vi)}
        <div class="journal-card p-5 sm:p-6 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-2xl shadow-xs transition-all hover:border-[var(--border-highlight)]">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
            
            <!-- Col 1: Word identity & metadata (lg:col-span-3) -->
            <div class="lg:col-span-3 flex items-start gap-3">
              <div class="w-8 h-8 rounded-full bg-[var(--bg-inner)] text-[var(--text-muted)] border border-[var(--border-main)] flex items-center justify-center text-xs font-semibold font-mono shrink-0">
                {String(index + 1).padStart(2, '0')}
              </div>
              <div class="space-y-1.5 flex-1 min-w-0">
                <div>
                  <button
                    onclick={() => onNavigateToDictionary?.(w.word)}
                    class="font-serif text-xl sm:text-2xl font-bold text-[var(--text-main)] hover:text-[var(--accent-primary)] transition cursor-pointer text-left block truncate"
                    title="Click to view detailed Dictionary entry"
                  >
                    {w.word}
                  </button>
                  <div class="flex items-center gap-1.5 mt-0.5 flex-wrap">
                    {#if w.phonetic}
                      <span class="text-xs text-[var(--text-muted)] font-mono">[{w.phonetic}]</span>
                    {/if}
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-[#eaf2ec] text-[#386848] border border-[#c4d9cb]/50">
                      {w.pos || 'noun'}
                    </span>
                  </div>
                </div>

                {#if w.topic_title}
                  <div class="flex items-center gap-1.5 text-[11px] text-[var(--text-subtle)] pt-0.5 truncate">
                    <span>{w.topic_icon || '📖'}</span>
                    <span>{w.topic_title}</span>
                  </div>
                {/if}
              </div>
            </div>

            <!-- Col 2: DEFINITION (lg:col-span-3) -->
            <div class="lg:col-span-3 space-y-1">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-subtle)] block">DEFINITION</span>
              <p class="text-sm font-medium text-[var(--text-main)] leading-relaxed">
                {cleanString(w.definition_en)}
              </p>
              {#if w.definition_vi}
                <p class="text-xs text-[var(--text-muted)] leading-relaxed">
                  {cleanString(w.definition_vi)}
                </p>
              {/if}
            </div>

            <!-- Col 3: EXAMPLE (lg:col-span-4 - Bilingual Paired Sentences) -->
            <div class="lg:col-span-4 space-y-2">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-subtle)] block">EXAMPLE</span>
              {#if examplePairs.length > 0}
                <div class="space-y-2.5">
                  {#each examplePairs as pair}
                    <div class="space-y-0.5">
                      <p class="font-serif italic text-sm text-[var(--text-main)] leading-relaxed">
                        {pair.en}
                      </p>
                      {#if pair.vi}
                        <p class="text-xs text-[var(--text-muted)] leading-relaxed">
                          {pair.vi}
                        </p>
                      {/if}
                    </div>
                  {/each}
                </div>
              {:else}
                <p class="text-xs text-[var(--text-muted)] italic">No example sentence available.</p>
              {/if}
            </div>

            <!-- Col 4: Audio Actions & SRS Listdown Dropdown (lg:col-span-2) -->
            <div class="lg:col-span-2 flex flex-col items-end space-y-3 relative">
              <!-- Top Row: Audio, 0.75x, Bookmark -->
              <div class="flex items-center gap-1">
                <button
                  onclick={() => playWord(w.word, false)}
                  class="p-1.5 rounded-lg hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer"
                  title="Pronounce (1.0x)"
                >
                  <Volume2 class="w-4 h-4" />
                </button>
                <button
                  onclick={() => playWord(w.word, true)}
                  class="px-2 py-1 rounded-lg hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] text-xs font-mono transition cursor-pointer"
                  title="Slow Pronunciation (0.75x)"
                >
                  0.75x
                </button>
                <button
                  onclick={() => handleSaveWord(w)}
                  class={`p-1.5 rounded-lg transition cursor-pointer ${
                    savedWordsMap[w.word.toLowerCase()] 
                      ? 'text-[var(--accent-primary)] bg-[var(--accent-primary-light)]' 
                      : 'text-[var(--text-muted)] hover:text-[var(--accent-primary)] hover:bg-[var(--accent-primary-light)]'
                  }`}
                  title={savedWordsMap[w.word.toLowerCase()] ? "Saved in Obsidian Vault (Click to remove)" : "Save to Obsidian Vault"}
                >
                  <Bookmark class={`w-4 h-4 ${savedWordsMap[w.word.toLowerCase()] ? 'fill-[var(--accent-primary)] text-[var(--accent-primary)]' : ''}`} />
                </button>
              </div>

              <!-- Practice Word Button (⚡) -->
              <button
                type="button"
                onclick={() => openPracticeModal(w)}
                class="w-full py-1.5 px-3 rounded-xl border border-[var(--border-main)] hover:border-[var(--accent-primary-border)] bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-xs font-semibold text-[var(--text-main)] hover:text-[var(--accent-primary)] flex items-center justify-center gap-1.5 shadow-2xs transition cursor-pointer active:scale-95"
                title="Practice this word (5-step active recall drill)"
              >
                <Zap class="w-3.5 h-3.5 text-[var(--accent-primary)] fill-[var(--accent-primary)]/20" />
                <span>Practice</span>
              </button>
            </div>

          </div>
        </div>
      {/each}
    </div>
  {:else}
    <!-- Flashcard Mode -->
    {#if words.length > 0}
      {@const curWord = words[currentCardIndex]}
      {@const cardExamplePairs = formatExamplePairs(curWord.example_en, curWord.example_vi)}
      <div class="max-w-xl mx-auto space-y-4">
        <!-- Progress Dots & Counter -->
        <div class="flex items-center justify-between journal-card px-4 py-2.5 border border-[var(--border-main)] bg-[var(--bg-card)]">
          <div class="flex items-center gap-1.5">
            {#each words as _, idx}
              <button
                onclick={() => goToCard(idx)}
                class={`h-2 rounded-full transition-all cursor-pointer ${
                  currentCardIndex === idx
                    ? 'w-6 bg-[var(--accent-primary)]'
                    : 'w-2 bg-[var(--border-main)] hover:bg-[var(--text-subtle)]'
                }`}
                title={`Go to card ${idx + 1}`}
              ></button>
            {/each}
          </div>

          <div class="flex items-center gap-2 text-xs font-medium text-[var(--text-muted)]">
            <span>Card <strong class="text-[var(--text-main)]">{currentCardIndex + 1}</strong> of {words.length}</span>
            <span>•</span>
            <span>{curWord.topic_title || 'Vocabulary'}</span>
          </div>
        </div>

        <!-- 3D Card Container with Prev/Next buttons -->
        <div class="relative flex items-center gap-3">
          <button
            onclick={prevCard}
            disabled={currentCardIndex === 0}
            class="p-3 rounded-2xl journal-card border border-[var(--border-main)] disabled:opacity-30 disabled:cursor-not-allowed text-[var(--text-muted)] hover:text-[var(--text-main)] transition shadow-sm cursor-pointer shrink-0"
            title="Previous (Left Arrow)"
          >
            <ChevronLeft class="w-5 h-5" />
          </button>

          <!-- svelte-ignore a11y_click_events_have_key_events -->
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <div
            onclick={() => cardFlipped = !cardFlipped}
            class="flex-1 min-h-[320px] journal-card border border-[var(--border-main)] rounded-3xl p-8 shadow-sm flex flex-col justify-between items-center text-center cursor-pointer transition-all hover:border-[var(--accent-primary)] select-none bg-[var(--bg-card)]"
          >
            {#if !cardFlipped}
              <!-- Front Side -->
              <div class="my-auto space-y-3">
                <span class="font-serif text-4xl sm:text-5xl font-bold text-[var(--text-main)] tracking-tight">
                  {curWord.word}
                </span>
                <div class="flex items-center justify-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#eaf2ec] text-[#386848] border border-[#c4d9cb]/50">
                    {curWord.pos || 'noun'}
                  </span>
                  {#if curWord.phonetic}
                    <span class="text-sm font-mono text-[var(--text-muted)]">[{curWord.phonetic}]</span>
                  {/if}
                </div>
                <p class="text-xs text-[var(--text-subtle)] pt-6">
                  Click card or press <strong>Space</strong> to reveal definition
                </p>
              </div>
            {:else}
              <!-- Back Side -->
              <div class="my-auto space-y-4 w-full text-center">
                <div class="space-y-1">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-subtle)]">DEFINITION</span>
                  <p class="text-base text-[var(--text-main)] font-medium leading-relaxed">{cleanString(curWord.definition_en)}</p>
                  {#if curWord.definition_vi}
                    <p class="text-xs text-[var(--text-muted)] leading-relaxed">{cleanString(curWord.definition_vi)}</p>
                  {/if}
                </div>

                {#if cardExamplePairs.length > 0}
                  <div class="pt-3 border-t border-[var(--border-main)] text-center space-y-2.5">
                    <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-subtle)]">EXAMPLE</span>
                    {#each cardExamplePairs as pair}
                      <div class="space-y-0.5">
                        <p class="font-serif italic text-sm text-[var(--text-main)] leading-relaxed">
                          {pair.en}
                        </p>
                        {#if pair.vi}
                          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
                            {pair.vi}
                          </p>
                        {/if}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            {/if}

            <!-- Bottom Controls on Card -->
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <div class="w-full flex items-center justify-between pt-4 border-t border-[var(--border-main)]" onclick={(e) => e.stopPropagation()}>
              <div class="flex items-center gap-2">
                <button
                  onclick={() => playWord(curWord.word)}
                  class="p-2 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer"
                  title="Pronounce"
                >
                  <Volume2 class="w-4 h-4" />
                </button>
                <button
                  onclick={() => onNavigateToDictionary?.(curWord.word)}
                  class="p-2 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer"
                  title="Look up in Dictionary"
                >
                  <BookA class="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onclick={() => openPracticeModal(curWord)}
                  class="p-2 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center gap-1 text-xs font-semibold border border-[var(--border-main)]"
                  title="Practice this word"
                >
                  <Zap class="w-3.5 h-3.5 text-[var(--accent-primary)] fill-[var(--accent-primary)]/20" />
                  <span>Practice</span>
                </button>
              </div>

              <button
                onclick={() => cardFlipped = !cardFlipped}
                class="text-xs text-[var(--text-muted)] hover:text-[var(--text-main)] flex items-center gap-1 cursor-pointer"
              >
                <RotateCcw class="w-3.5 h-3.5" />
                <span>{cardFlipped ? 'Show Word' : 'Flip Card'}</span>
              </button>

              <button
                onclick={() => handleSaveWord(curWord)}
                class={`p-2 rounded-xl transition cursor-pointer border ${
                  savedWordsMap[curWord.word.toLowerCase()]
                    ? 'bg-emerald-500/15 text-emerald-700 border-emerald-400/40'
                    : 'bg-[var(--bg-inner)] text-[var(--text-muted)] hover:text-[var(--text-main)] border-[var(--border-main)]'
                }`}
                title={savedWordsMap[curWord.word.toLowerCase()] ? "Saved in Vault" : "Save to Obsidian Vault"}
              >
                <Bookmark class={`w-4 h-4 ${savedWordsMap[curWord.word.toLowerCase()] ? 'fill-[var(--accent-primary)] text-[var(--accent-primary)]' : ''}`} />
              </button>
            </div>
          </div>

          <button
            onclick={nextCard}
            disabled={currentCardIndex === words.length - 1}
            class="p-3 rounded-2xl journal-card border border-[var(--border-main)] disabled:opacity-30 disabled:cursor-not-allowed text-[var(--text-muted)] hover:text-[var(--text-main)] transition shadow-sm cursor-pointer shrink-0"
            title="Next (Right Arrow)"
          >
            <ChevronRight class="w-5 h-5" />
          </button>
        </div>

        <!-- Card SRS Grading Row -->
        <div class="journal-card p-3 border border-[var(--border-main)] flex items-center justify-between text-xs bg-[var(--bg-card)]">
          <span class="text-[var(--text-muted)] font-medium">SRS Grade:</span>
          <div class="flex items-center gap-1.5">
            <button
              onclick={() => handleSrsRate(curWord.id, 1)}
              class="px-3 py-1.5 rounded-lg bg-[var(--bg-inner)] hover:bg-red-500/15 text-red-600 font-semibold border border-[var(--border-main)] transition cursor-pointer"
            >
              Again (0d)
            </button>
            <button
              onclick={() => handleSrsRate(curWord.id, 2)}
              class="px-3 py-1.5 rounded-lg bg-[var(--bg-inner)] hover:bg-amber-500/15 text-amber-700 font-semibold border border-[var(--border-main)] transition cursor-pointer"
            >
              Hard (3d)
            </button>
            <button
              onclick={() => handleSrsRate(curWord.id, 3)}
              class="px-3 py-1.5 rounded-lg bg-[var(--bg-inner)] hover:bg-blue-500/15 text-blue-700 font-semibold border border-[var(--border-main)] transition cursor-pointer"
            >
              Good (6d)
            </button>
            <button
              onclick={() => handleSrsRate(curWord.id, 4)}
              class="px-3 py-1.5 rounded-lg bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold border border-[var(--accent-primary-border)] transition cursor-pointer"
            >
              Easy (7d)
            </button>
          </div>
        </div>
      </div>
    {/if}
  {/if}

  <!-- Bottom Grid: Daily Idiom & Quick Quiz matching 3.png -->
  <div class="grid md:grid-cols-2 gap-4 pt-2">
    <!-- Daily Idiom Card -->
    {#if idiom}
      <div class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-2xl shadow-xs space-y-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-base">🌿</span>
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-subtle)]">DAILY IDIOM</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-[var(--bg-inner)] border border-[var(--border-main)] text-[var(--text-muted)]">
              Life & Spoken English
            </span>
          </div>

          <div class="flex items-center gap-1.5">
            <button
              onclick={() => playTTS(idiom.idiom)}
              class="px-2.5 py-1 rounded-lg bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer border border-[var(--border-main)] flex items-center gap-1 text-xs"
              title="Listen"
            >
              <Volume2 class="w-3.5 h-3.5" />
              <span>Listen</span>
            </button>

            <button
              onclick={handleNextIdiom}
              class="p-1.5 rounded-lg bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer border border-[var(--border-main)]"
              title="Next Idiom"
            >
              <Dices class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div>
          <button
            onclick={() => onNavigateToDictionary?.(idiom.idiom)}
            class="font-serif text-xl sm:text-2xl font-bold text-[var(--text-main)] hover:text-[var(--accent-primary)] text-left transition cursor-pointer flex items-center gap-1.5 group/idm"
            title="Click to view detailed Dictionary entry"
          >
            <span>{idiom.idiom}</span>
            <BookA class="w-3.5 h-3.5 opacity-0 group-hover/idm:opacity-100 text-[var(--accent-primary)] transition" />
          </button>
        </div>

        <div class="space-y-1.5 text-xs text-[var(--text-main)] leading-relaxed">
          <p>
            <strong class="font-semibold text-[var(--text-subtle)]">Meaning:</strong> {idiom.meaning_en}
          </p>
          {#if idiom.example}
            <p class="text-[var(--text-muted)] font-serif italic">
              <span class="font-semibold not-italic font-sans text-[var(--text-subtle)]">Example:</span> {idiom.example}
            </p>
          {/if}
        </div>
      </div>
    {/if}

    <!-- Quick Quiz Card -->
    {#if quiz}
      <div class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-2xl shadow-xs space-y-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-base">🌿</span>
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-subtle)]">QUICK QUIZ</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-[var(--bg-inner)] border border-[var(--border-main)] text-[var(--text-muted)]">
              Prepositions & Phrasal Verbs
            </span>
          </div>
          <button
            onclick={loadNextQuiz}
            class="px-2.5 py-1 rounded-lg bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] text-xs font-medium transition cursor-pointer flex items-center gap-1 border border-[var(--border-main)]"
            title="Choose another question"
          >
            <PenTool class="w-3 h-3" />
            <span>Practice</span>
          </button>
        </div>

        <p class="text-sm font-medium text-[var(--text-main)]">{quiz.question}</p>

        <!-- Quiz Options -->
        <div class="grid grid-cols-2 gap-2">
          {#each quiz.options as opt}
            {@const optKey = opt.trim().charAt(0)}
            <button
              onclick={() => { selectedQuizOption = optKey; quizAnswered = true; }}
              class={`p-2.5 rounded-xl text-xs font-semibold text-left transition cursor-pointer border ${
                quizAnswered
                  ? optKey === quiz.correct
                    ? 'bg-emerald-500/15 text-emerald-700 border-emerald-500'
                    : selectedQuizOption === optKey
                    ? 'bg-red-500/15 text-red-700 border-red-500'
                    : 'bg-[var(--bg-inner)] text-[var(--text-muted)] border-[var(--border-main)]'
                  : 'bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] border-[var(--border-main)]'
              }`}
            >
              {opt}
            </button>
          {/each}
        </div>

        <!-- Explanation Reveal -->
        {#if quizAnswered}
          <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1 text-xs">
            <div class="flex items-center gap-1.5 font-bold">
              {#if selectedQuizOption === quiz.correct}
                <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                <span class="text-emerald-700">Correct!</span>
              {:else}
                <XCircle class="w-4 h-4 text-red-600" />
                <span class="text-red-700">Incorrect. Correct answer: {quiz.correct}</span>
              {/if}
            </div>
            <p class="text-[var(--text-main)]">{quiz.explanation}</p>
            {#if quiz.tip}
              <p class="text-[var(--text-muted)] font-mono text-[11px]">{quiz.tip}</p>
            {/if}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>

{#if practiceWord}
  <WordPracticeModal
    word={practiceWord}
    isOpen={isPracticeModalOpen}
    onClose={closePracticeModal}
    onWordSaved={(w) => {
      savedWordsMap[w.word.toLowerCase()] = true;
    }}
  />
{/if}
