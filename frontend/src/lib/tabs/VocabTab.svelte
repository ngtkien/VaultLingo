<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    GetDailyVocab, 
    GetDailyIdiom, 
    GetQuickQuiz, 
    GetQuickQuizExcluding,
    GetAvailableTopics, 
    SaveWordToObsidian, 
    SaveAllWordsToObsidian, 
    DeleteWordFromObsidian,
    RecordSrsReview 
  } from '../../../wailsjs/go/main/App.js';
  import { playTTS, stopAudio } from '../utils/audio';
  import { 
    Volume2, 
    ExternalLink, 
    Bookmark, 
    Check, 
    RefreshCw, 
    Layers, 
    Sparkles, 
    HelpCircle, 
    CheckCircle2, 
    XCircle, 
    ChevronLeft, 
    ChevronRight,
    RotateCcw,
    Trash2,
    BookA,
    Dices
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
  let playingWord = $state('');

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

  async function loadData() {
    loading = true;
    try {
      topics = await GetAvailableTopics();
      words = await GetDailyVocab(selectedTopic, 5);
      
      await loadDailyIdiom();
      seenQuizIds = [];
      await loadNextQuiz();
      currentCardIndex = 0;
      cardFlipped = false;
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function handleTopicChange(topicKey: string) {
    selectedTopic = topicKey;
    loading = true;
    try {
      words = await GetDailyVocab(selectedTopic, 5);
      currentCardIndex = 0;
      cardFlipped = false;
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
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

  async function handleDeleteWord(word: string) {
    const key = word.toLowerCase();
    try {
      await DeleteWordFromObsidian(word);
      savedWordsMap[key] = false;
    } catch (e) {
      console.error(e);
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
      if (activeViewMode === 'flashcard' && currentCardIndex < words.length - 1) {
        nextCard();
      }
    } catch (e) {
      console.error(e);
    }
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
    playingWord = word;
    playTTS(word, slow ? 0.75 : 1.0, word).then(() => {
      playingWord = '';
    });
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
    loadData();
    window.addEventListener('keydown', handleKeydown);
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
      window.clearTimeout(midnightTimer);
    };
  });
</script>

<div class="space-y-6">
  <!-- Top Controls & Topic Filter -->
  <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
    <div class="flex items-center gap-2 overflow-x-auto pb-1 max-w-full">
      {#each topics as t}
        <button
          onclick={() => handleTopicChange(t.key)}
          class={`px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition cursor-pointer flex items-center gap-1.5 ${
            selectedTopic === t.key
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25 ring-1 ring-blue-400/50'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700/80 hover:text-white'
          }`}
        >
          <span>{t.icon}</span>
          <span>{t.title}</span>
        </button>
      {/each}
    </div>

    <div class="flex items-center gap-2">
      <!-- Toggle List / Flashcard -->
      <div class="bg-slate-800 p-1 rounded-xl flex items-center gap-1 border border-slate-700/60">
        <button
          onclick={() => activeViewMode = 'list'}
          class={`px-3 py-1 text-xs font-medium rounded-lg transition cursor-pointer ${
            activeViewMode === 'list' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          List
        </button>
        <button
          onclick={() => activeViewMode = 'flashcard'}
          class={`px-3 py-1 text-xs font-medium rounded-lg transition cursor-pointer flex items-center gap-1 ${
            activeViewMode === 'flashcard' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers class="w-3 h-3" />
          Flashcard
        </button>
      </div>

      <!-- Save All -->
      <button
        onclick={handleSaveAll}
        class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 transition shadow-lg shadow-emerald-600/20 cursor-pointer"
        title="Save all 5 words to Obsidian Vault"
      >
        <Bookmark class="w-3.5 h-3.5" />
        <span>Save All to Obsidian</span>
      </button>

      <!-- Refresh -->
      <button
        onclick={loadData}
        class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer border border-slate-700"
        title="Load new word set"
      >
        <RefreshCw class={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
      </button>
    </div>
  </div>

  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-blue-500" />
      <p class="text-sm font-medium">Loading vocabulary & daily items...</p>
    </div>
  {:else if activeViewMode === 'list'}
    <!-- Word List View -->
    <div class="grid gap-4">
      {#each words as w, index}
        <div class="bg-slate-900/70 border border-slate-800/80 hover:border-slate-700 rounded-2xl p-5 transition-all backdrop-blur-md group hover:shadow-xl hover:shadow-blue-500/5 space-y-3">
          <div class="flex items-start justify-between gap-4">
            <div class="flex items-center gap-3">
              <span class="w-7 h-7 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center text-xs font-bold font-mono">
                0{index + 1}
              </span>
              <div>
                <div class="flex items-center gap-2">
                  <button
                    onclick={() => onNavigateToDictionary?.(w.word)}
                    class="text-xl font-bold text-slate-100 tracking-tight hover:text-cyan-400 text-left transition cursor-pointer flex items-center gap-1.5 group/title"
                    title="Click to view detailed Dictionary entry"
                  >
                    <span>{w.word}</span>
                    <BookA class="w-3.5 h-3.5 opacity-0 group-hover/title:opacity-100 text-cyan-400 transition" />
                  </button>
                  <span class="px-2 py-0.5 rounded-md text-[11px] font-semibold bg-slate-800 text-blue-400 border border-slate-700">
                    {w.pos || 'Noun'}
                  </span>
                  <span class="text-xs text-slate-400 font-mono">{w.phonetic}</span>
                </div>
                <div class="text-xs text-slate-500 mt-0.5 flex items-center gap-1">
                  <span>{w.topic_icon}</span>
                  <span>{w.topic_title}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2">
              <button
                onclick={() => onNavigateToDictionary?.(w.word)}
                class="p-2 rounded-xl bg-slate-800 hover:bg-cyan-600 text-slate-300 hover:text-white transition cursor-pointer"
                title="Look up in Smart Dictionary"
              >
                <BookA class="w-4 h-4" />
              </button>
              <button
                onclick={() => playWord(w.word, false)}
                class="p-2 rounded-xl bg-slate-800 hover:bg-blue-600 text-slate-300 hover:text-white transition cursor-pointer"
                title="Pronounce (1.0x)"
              >
                <Volume2 class="w-4 h-4" />
              </button>
              <button
                onclick={() => playWord(w.word, true)}
                class="px-2 py-1 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 text-xs font-mono transition cursor-pointer"
                title="Slow Pronunciation (0.75x)"
              >
                0.75x
              </button>
              <a
                href={w.dict_link}
                target="_blank"
                class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition"
                title="Open Cambridge Dictionary"
              >
                <ExternalLink class="w-4 h-4" />
              </a>
              <button
                onclick={() => handleSaveWord(w)}
                class={`p-2 rounded-xl transition cursor-pointer flex items-center gap-1 text-xs font-medium ${
                  savedWordsMap[w.word.toLowerCase()]
                    ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30'
                    : 'bg-slate-800 hover:bg-emerald-600 text-slate-300 hover:text-white'
                }`}
                title={savedWordsMap[w.word.toLowerCase()] ? "Saved in Vault (Click to unsave)" : "Save to Obsidian Vault"}
              >
                {#if savedWordsMap[w.word.toLowerCase()]}
                  <Check class="w-4 h-4 text-emerald-400" />
                {:else}
                  <Bookmark class="w-4 h-4" />
                {/if}
              </button>

              {#if savedWordsMap[w.word.toLowerCase()]}
                <button
                  onclick={() => handleDeleteWord(w.word)}
                  class="p-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 border border-red-500/30 transition cursor-pointer"
                  title="Delete from Obsidian Vault"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              {/if}
            </div>
          </div>

          <!-- Definition & Examples -->
          <div class="bg-slate-950/50 p-3.5 rounded-xl border border-slate-800/60 space-y-2">
            <div>
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Definition:</span>
              <p class="text-sm text-slate-200 mt-0.5">{w.definition_en}</p>
              {#if w.definition_vi}
                <p class="text-xs text-slate-400 mt-0.5 italic">{w.definition_vi}</p>
              {/if}
            </div>
            {#if w.example_en}
              <div class="pt-2 border-t border-slate-800/50">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Example:</span>
                <p class="text-sm text-slate-300 italic mt-0.5">"{w.example_en}"</p>
                {#if w.example_vi}
                  <p class="text-xs text-slate-500 mt-0.5">{w.example_vi}</p>
                {/if}
              </div>
            {/if}
          </div>

          <!-- SRS Rating Buttons -->
          <div class="flex items-center justify-between pt-1">
            <span class="text-xs text-slate-500">Spaced Repetition (SRS Recall):</span>
            <div class="flex items-center gap-1.5">
              <button
                onclick={() => handleSrsRate(w.id, 1)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 transition cursor-pointer"
              >
                Again (1d)
              </button>
              <button
                onclick={() => handleSrsRate(w.id, 2)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 border border-amber-500/20 transition cursor-pointer"
              >
                Hard (2d)
              </button>
              <button
                onclick={() => handleSrsRate(w.id, 3)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20 transition cursor-pointer"
              >
                Good (4d)
              </button>
              <button
                onclick={() => handleSrsRate(w.id, 4)}
                class="px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/20 transition cursor-pointer"
              >
                Easy (7d)
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <!-- Flashcard Mode with Navigation Buttons & Shortcuts -->
    {#if words.length > 0}
      {@const curWord = words[currentCardIndex]}
      <div class="max-w-xl mx-auto space-y-4">
        <!-- Top Flashcard Header: Dots Navigation & Progress -->
        <div class="flex items-center justify-between bg-slate-900/60 px-4 py-2.5 rounded-2xl border border-slate-800 backdrop-blur-md">
          <div class="flex items-center gap-1.5">
            {#each words as _, idx}
              <button
                onclick={() => goToCard(idx)}
                class={`h-2 rounded-full transition-all cursor-pointer ${
                  currentCardIndex === idx
                    ? 'w-6 bg-blue-500'
                    : 'w-2 bg-slate-700 hover:bg-slate-500'
                }`}
                title={`Go to card ${idx + 1}`}
              ></button>
            {/each}
          </div>

          <div class="flex items-center gap-2 text-xs font-medium text-slate-400">
            <span>Card <strong class="text-slate-200">{currentCardIndex + 1}</strong> of {words.length}</span>
            <span class="text-slate-600">•</span>
            <span>{curWord.topic_title}</span>
          </div>
        </div>

        <!-- 3D Flipping Card Container with Prev / Next side controls -->
        <div class="relative flex items-center gap-3">
          <!-- Previous Card Button -->
          <button
            onclick={prevCard}
            disabled={currentCardIndex === 0}
            class="p-3 rounded-2xl bg-slate-900/90 border border-slate-800 hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed text-slate-300 hover:text-white transition shadow-lg cursor-pointer shrink-0"
            title="Previous Word (Left Arrow key)"
          >
            <ChevronLeft class="w-5 h-5" />
          </button>

          <!-- The Main Flipping Card -->
          <!-- svelte-ignore a11y_click_events_have_key_events -->
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <div
            onclick={() => cardFlipped = !cardFlipped}
            class="flex-1 min-h-[320px] bg-slate-900/90 border border-slate-700/80 rounded-3xl p-8 shadow-2xl backdrop-blur-xl flex flex-col justify-between items-center text-center cursor-pointer transition-all hover:border-blue-500/50 select-none group"
          >
            {#if !cardFlipped}
              <!-- Front Side -->
              <div class="my-auto space-y-3">
                <span class="text-4xl font-extrabold text-slate-100 tracking-tight group-hover:text-blue-300 transition-colors">
                  {curWord.word}
                </span>
                <div class="flex items-center justify-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30">
                    {curWord.pos}
                  </span>
                  <span class="text-sm font-mono text-slate-400">{curWord.phonetic}</span>
                </div>
                <p class="text-xs text-slate-500 pt-6 flex items-center justify-center gap-1">
                  <span>Click card or press <strong>Space</strong> to reveal definition</span>
                  <span>👆</span>
                </p>
              </div>
            {:else}
              <!-- Back Side -->
              <div class="my-auto space-y-4">
                <div class="space-y-1.5">
                  <span class="text-xs uppercase text-slate-400 font-bold tracking-wider">Definition</span>
                  <p class="text-base text-slate-100 font-medium leading-relaxed">{curWord.definition_en}</p>
                  {#if curWord.definition_vi}
                    <p class="text-xs text-slate-400 italic">{curWord.definition_vi}</p>
                  {/if}
                </div>
                {#if curWord.example_en}
                  <div class="pt-3 border-t border-slate-800">
                    <span class="text-xs uppercase text-slate-400 font-bold tracking-wider">Example</span>
                    <p class="text-sm text-slate-300 italic leading-relaxed">"{curWord.example_en}"</p>
                  </div>
                {/if}
              </div>
            {/if}

            <!-- Card Bottom Bar (Audio, Dictionary, Flip Hint & Obsidian Save) -->
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <div class="w-full flex items-center justify-between pt-4 border-t border-slate-800" onclick={(e) => e.stopPropagation()}>
              <div class="flex items-center gap-2">
                <button
                  onclick={() => playWord(curWord.word)}
                  class="p-2 rounded-xl bg-slate-800 hover:bg-blue-600 text-slate-300 hover:text-white transition cursor-pointer"
                  title="Pronounce"
                >
                  <Volume2 class="w-4 h-4" />
                </button>
                <button
                  onclick={() => onNavigateToDictionary?.(curWord.word)}
                  class="p-2 rounded-xl bg-slate-800 hover:bg-cyan-600 text-slate-300 hover:text-white transition cursor-pointer"
                  title="Look up in Smart Dictionary"
                >
                  <BookA class="w-4 h-4" />
                </button>
              </div>

              <button
                onclick={() => cardFlipped = !cardFlipped}
                class="text-xs text-slate-500 hover:text-slate-300 flex items-center gap-1 cursor-pointer"
              >
                <RotateCcw class="w-3 h-3" />
                <span>{cardFlipped ? 'Show Word' : 'Flip Card'}</span>
              </button>

              <button
                onclick={() => handleSaveWord(curWord)}
                class={`p-2 rounded-xl transition cursor-pointer flex items-center gap-1 text-xs font-medium ${
                  savedWordsMap[curWord.word.toLowerCase()]
                    ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30'
                    : 'bg-slate-800 hover:bg-emerald-600 text-slate-300 hover:text-white'
                }`}
                title="Save to Obsidian Vault"
              >
                {#if savedWordsMap[curWord.word.toLowerCase()]}
                  <Check class="w-4 h-4 text-emerald-400" />
                {:else}
                  <Bookmark class="w-4 h-4" />
                {/if}
              </button>
            </div>
          </div>

          <!-- Next Card Button -->
          <button
            onclick={nextCard}
            disabled={currentCardIndex === words.length - 1}
            class="p-3 rounded-2xl bg-slate-900/90 border border-slate-800 hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed text-slate-300 hover:text-white transition shadow-lg cursor-pointer shrink-0"
            title="Next Word (Right Arrow key)"
          >
            <ChevronRight class="w-5 h-5" />
          </button>
        </div>

        <!-- Rating Buttons in Flashcard -->
        <div class="grid grid-cols-4 gap-2">
          <button
            onclick={() => handleSrsRate(curWord.id, 1)}
            class="py-2.5 rounded-xl text-xs font-bold bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/30 transition cursor-pointer"
          >
            Again (1d)
          </button>
          <button
            onclick={() => handleSrsRate(curWord.id, 2)}
            class="py-2.5 rounded-xl text-xs font-bold bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 border border-amber-500/30 transition cursor-pointer"
          >
            Hard (2d)
          </button>
          <button
            onclick={() => handleSrsRate(curWord.id, 3)}
            class="py-2.5 rounded-xl text-xs font-bold bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/30 transition cursor-pointer"
          >
            Good (4d)
          </button>
          <button
            onclick={() => handleSrsRate(curWord.id, 4)}
            class="py-2.5 rounded-xl text-xs font-bold bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30 transition cursor-pointer"
          >
            Easy (7d)
          </button>
        </div>
      </div>
    {/if}
  {/if}

  <!-- Bottom Grid: Daily Idiom & 10s Quick Quiz -->
  <div class="grid md:grid-cols-2 gap-4 pt-4">
    <!-- Daily Idiom Card -->
    {#if idiom}
      <div class="bg-gradient-to-br from-slate-900/90 to-indigo-950/40 border border-indigo-900/30 rounded-2xl p-5 space-y-3 shadow-lg theme-card">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-lg">💡</span>
            <h4 class="text-xs font-bold uppercase tracking-wider text-indigo-400">Daily Idiom</h4>
            <span class="px-2 py-0.5 rounded-full text-[9px] font-mono font-semibold bg-indigo-500/15 text-indigo-300 border border-indigo-500/30">
              📅 Auto-updates daily
            </span>
          </div>

          <div class="flex items-center gap-1.5">
            <!-- Next / Shuffle Idiom -->
            <button
              onclick={handleNextIdiom}
              class="px-2 py-1 rounded-lg bg-indigo-900/40 hover:bg-indigo-600 text-indigo-200 text-xs font-medium transition cursor-pointer flex items-center gap-1 active:scale-95"
              title="Next / Explore Another Idiom"
            >
              <Dices class="w-3.5 h-3.5" />
              <span class="text-[11px]">Next Idiom</span>
            </button>

            <!-- Pronounce -->
            <button
              onclick={() => playTTS(idiom.idiom)}
              class="p-1.5 rounded-lg bg-indigo-900/40 hover:bg-indigo-600 text-indigo-200 transition cursor-pointer"
              title="Pronounce"
            >
              <Volume2 class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div>
          <button
            onclick={() => onNavigateToDictionary?.(idiom.idiom)}
            class="text-lg font-bold text-slate-100 hover:text-cyan-400 text-left transition cursor-pointer flex items-center gap-1.5 group/idm"
            title="Click to view detailed Dictionary entry"
          >
            <span>{idiom.idiom}</span>
            <BookA class="w-3.5 h-3.5 opacity-0 group-hover/idm:opacity-100 text-cyan-400 transition" />
          </button>
          <p class="text-xs font-mono text-slate-400">{idiom.phonetic}</p>
        </div>

        <div class="bg-slate-950/50 p-3 rounded-xl border border-slate-800/60 space-y-1 theme-inner">
          <p class="text-xs text-slate-300"><strong class="text-slate-100">Meaning:</strong> {idiom.meaning_en}</p>
          {#if idiom.meaning_vi}
            <p class="text-xs text-indigo-300 italic">{idiom.meaning_vi}</p>
          {/if}
        </div>

        {#if idiom.example}
          <div class="text-xs text-slate-400 italic">
            <span class="font-semibold text-slate-300">Example:</span> "{idiom.example}"
          </div>
        {/if}
      </div>
    {/if}

    <!-- Quick Quiz Card -->
    {#if quiz}
      <div class="bg-gradient-to-br from-slate-900/90 to-purple-950/40 border border-purple-900/30 rounded-2xl p-5 space-y-3 shadow-lg">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-lg">{quiz.category_icon || '🎯'}</span>
            <h4 class="text-xs font-bold uppercase tracking-wider text-purple-400">10s Quick Quiz ({quiz.category})</h4>
          </div>
          <button
            onclick={loadNextQuiz}
            class="px-2 py-1 rounded-lg bg-purple-900/40 hover:bg-purple-600 text-purple-200 text-[11px] font-medium transition cursor-pointer flex items-center gap-1 active:scale-95"
            title="Choose another question"
          >
            <RefreshCw class="w-3.5 h-3.5" />
            <span>Another</span>
          </button>
        </div>

        <p class="text-sm font-medium text-slate-100">{quiz.question}</p>

        <!-- Quiz Options -->
        <div class="grid grid-cols-2 gap-2">
          {#each quiz.options as opt}
            {@const optKey = opt.trim().charAt(0)}
            <button
              onclick={() => { selectedQuizOption = optKey; quizAnswered = true; }}
              class={`p-2.5 rounded-xl text-xs font-semibold text-left transition cursor-pointer border ${
                quizAnswered
                  ? optKey === quiz.correct
                    ? 'bg-emerald-600/20 text-emerald-300 border-emerald-500'
                    : selectedQuizOption === optKey
                    ? 'bg-red-600/20 text-red-300 border-red-500'
                    : 'bg-slate-900/60 text-slate-400 border-slate-800'
                  : 'bg-slate-900/80 hover:bg-purple-900/30 text-slate-200 border-slate-700/60'
              }`}
            >
              {opt}
            </button>
          {/each}
        </div>

        <!-- Explanation Reveal -->
        {#if quizAnswered}
          <div class="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1 text-xs animate-fade-in">
            <div class="flex items-center gap-1.5 font-bold">
              {#if selectedQuizOption === quiz.correct}
                <CheckCircle2 class="w-4 h-4 text-emerald-400" />
                <span class="text-emerald-400">Correct!</span>
              {:else}
                <XCircle class="w-4 h-4 text-red-400" />
                <span class="text-red-400">Incorrect. Correct answer: {quiz.correct}</span>
              {/if}
            </div>
            <p class="text-slate-300">{quiz.explanation}</p>
            {#if quiz.tip}
              <p class="text-purple-300 font-mono text-[11px]">{quiz.tip}</p>
            {/if}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>
