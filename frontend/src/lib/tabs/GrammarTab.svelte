<script lang="ts">
  import { onMount } from 'svelte';
  import { GetGrammarDrill, GetGrammarCategories, CheckGrammarAnswer } from '../../../wailsjs/go/main/App.js';
  import { playTTS, stopAudio } from '../utils/audio';
  import { 
    Sparkles, 
    RefreshCw, 
    Check, 
    ChevronDown, 
    Volume2, 
    Eye, 
    EyeOff, 
    Award, 
    BookOpen, 
    Zap, 
    RotateCcw,
    Filter,
    Lightbulb,
    CheckCircle2,
    Clock,
    Dumbbell
  } from 'lucide-svelte';

  interface CategoryInfo {
    tense_category: string;
    category_icon: string;
    type: string;
    count: number;
  }

  let activeView = $state<'practice' | 'cheatsheet'>('practice');
  let cheatsheetTab = $state<'mindsets' | 'tenses'>('mindsets');
  let categories = $state<CategoryInfo[]>([]);
  let selectedCategory = $state<string>('all');
  let currentDrill = $state<any>(null);
  let userInput = $state('');
  let checked = $state(false);
  let diffResult = $state<any>(null);
  let showHint = $state(false);
  let loading = $state(false);
  let isAudioPlaying = $state(false);
  let isDropdownOpen = $state(false);
  let topicSearch = $state('');
  let seenIds = $state<number[]>([]);

  // Word Scramble state
  let inputMode = $state<'type' | 'scramble'>('type');
  let availableScrambleTokens = $state<{ id: number; word: string; used: boolean }[]>([]);
  let selectedScrambleTokens = $state<{ id: number; word: string }[]>([]);

  async function loadCategories() {
    try {
      const res = await GetGrammarCategories();
      if (res && res.length > 0) {
        categories = res;
      }
    } catch (e) {
      console.error('Failed to load grammar categories:', e);
    }
  }

  async function loadDrill(category = selectedCategory) {
    loading = true;
    try {
      const drill = await GetGrammarDrill(category, 'all', seenIds);
      currentDrill = drill;
      if (drill?.id && !seenIds.includes(drill.id)) {
        seenIds = [...seenIds, drill.id];
      }
      userInput = '';
      checked = false;
      diffResult = null;
      showHint = false;
      setupScrambleTokens(drill);
    } catch (e) {
      console.error('Failed to load grammar drill:', e);
    } finally {
      loading = false;
    }
  }

  function setupScrambleTokens(drill: any) {
    if (!drill?.target_question) {
      availableScrambleTokens = [];
      selectedScrambleTokens = [];
      return;
    }
    let rawTokens: string[] = [];
    if (drill.scramble_words && drill.scramble_words.length > 0) {
      rawTokens = [...drill.scramble_words];
    } else {
      rawTokens = drill.target_question.replace(/[?.,]/g, (m: string) => ` ${m}`).trim().split(/\s+/);
    }

    const shuffled = rawTokens
      .map((word, idx) => ({ id: idx, word, used: false, sort: Math.random() }))
      .sort((a, b) => a.sort - b.sort)
      .map(item => ({ id: item.id, word: item.word, used: false }));

    availableScrambleTokens = shuffled;
    selectedScrambleTokens = [];
  }

  function handleSelectCategory(cat: string) {
    if (selectedCategory !== cat) {
      selectedCategory = cat;
      seenIds = [];
    }
    isDropdownOpen = false;
    topicSearch = '';
    loadDrill(cat);
  }

  function toggleScrambleWord(token: { id: number; word: string; used: boolean }) {
    if (checked) return;
    if (token.used) {
      selectedScrambleTokens = selectedScrambleTokens.filter(t => t.id !== token.id);
      token.used = false;
    } else {
      selectedScrambleTokens = [...selectedScrambleTokens, { id: token.id, word: token.word }];
      token.used = true;
    }
    userInput = selectedScrambleTokens.map(t => t.word).join(' ').replace(/\s+([?.,!])/g, '$1');
  }

  function removeSelectedToken(token: { id: number; word: string }) {
    if (checked) return;
    selectedScrambleTokens = selectedScrambleTokens.filter(t => t.id !== token.id);
    const origin = availableScrambleTokens.find(t => t.id === token.id);
    if (origin) origin.used = false;
    userInput = selectedScrambleTokens.map(t => t.word).join(' ').replace(/\s+([?.,!])/g, '$1');
  }

  function resetScramble() {
    if (checked) return;
    availableScrambleTokens.forEach(t => t.used = false);
    selectedScrambleTokens = [];
    userInput = '';
  }

  function playAudio(slow = false) {
    if (!currentDrill?.target_question) return;
    isAudioPlaying = true;
    playTTS(currentDrill.target_question, slow ? 0.75 : 1.0, 'grammar').then(() => {
      isAudioPlaying = false;
    });
  }

  async function handleCheck() {
    if (!currentDrill?.target_question || !userInput.trim()) return;
    try {
      diffResult = await CheckGrammarAnswer(currentDrill.target_question, userInput);
      checked = true;
    } catch (e) {
      console.error(e);
    }
  }

  let activeCategoryInfo = $derived(() => {
    if (selectedCategory === 'all') {
      return { tense_category: 'All Tenses & Questions', category_icon: '⚡', count: categories.reduce((acc, c) => acc + c.count, 0) };
    }
    const found = categories.find(c => c.tense_category === selectedCategory);
    return found || { tense_category: selectedCategory, category_icon: '🎯', count: 0 };
  });

  let filteredCategories = $derived(() => {
    if (!topicSearch.trim()) return categories;
    const q = topicSearch.toLowerCase().trim();
    return categories.filter(c => c.tense_category.toLowerCase().includes(q));
  });

  onMount(async () => {
    await loadCategories();
    loadDrill('all');
  });

  const QUESTION_MINDSETS = [
    {
      category: "1. Feasibility & Plans",
      icon: "🚀",
      badge: "Can we? When will we?",
      description: "Ask whether an action is possible or inquire about scheduled timelines directly.",
      triggers: [
        { formula: "Can we [V-inf] by [Time]?", use: "Ask if an action can be finished before a specific deadline", eg: "Can we demo this by Friday?", vi: "Liệu chúng ta có kịp demo vào thứ Sáu không?" },
        { formula: "When are we going to [V-inf]?", use: "Inquire about a pre-scheduled future milestone", eg: "When are we going to launch the beta release?", vi: "Khi nào chúng ta sẽ ra mắt bản beta?" },
        { formula: "Will it be possible to [V-inf]?", use: "Polite formal request regarding project flexibility", eg: "Will it be possible to extend the deadline by two days?", vi: "Liệu có khả năng lùi deadline thêm hai ngày không?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Instead of overthinking, trigger immediately: 'Can we [V] by...?'"
    },
    {
      category: "2. Estimation & Resources",
      icon: "⏱️",
      badge: "How long? How many?",
      description: "Ask about duration, budget estimation, or required team headcount.",
      triggers: [
        { formula: "How long will it take (you) to [V-inf]?", use: "Fixed Lego chunk for time estimation", eg: "How long will it take you to fix this bug?", vi: "Mất bao lâu để bạn sửa xong lỗi này?" },
        { formula: "How many [people/engineers] do you need to [V-inf]?", use: "Ask for headcount / resource allocation", eg: "How many engineers do you need to complete this product?", vi: "Bạn cần bao nhiêu kỹ sư để hoàn thành sản phẩm này?" },
        { formula: "How much does it cost to [V-inf]?", use: "Cost and expense inquiries", eg: "How much does it cost to upgrade the server instance?", vi: "Mất bao nhiêu tiền để nâng cấp máy chủ?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Drop literal 'lose/spend' thinking ➔ Trigger fixed chunk: 'How long will it take you to...'"
    },
    {
      category: "3. Feedback & Problem Solving",
      icon: "💬",
      badge: "What do you think? How to handle?",
      description: "Gather feedback on technical approaches, seek advice, or address edge cases.",
      triggers: [
        { formula: "What do you think about [Noun / V-ing]?", use: "Ask for opinions regarding an idea", eg: "What do you think about migrating to PostgreSQL?", vi: "Bạn nghĩ sao về việc chuyển sang PostgreSQL?" },
        { formula: "How should we handle [Issue / Edge Case]?", use: "Collaborative problem-solving opener", eg: "How should we handle this unexpected edge case?", vi: "Chúng ta nên xử lý trường hợp biên này như thế nào?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Be direct & professional: 'What do you think about...?'"
    },
    {
      category: "4. Status & Confirmation",
      icon: "🔍",
      badge: "Any updates? Ready?",
      description: "Check progress politely and ask if someone has had time to review documents.",
      triggers: [
        { formula: "Have you had a chance to [V-inf]?", use: "Polite inquiry to check if someone reviewed a PR/email", eg: "Have you had a chance to review my pull request?", vi: "Bạn đã có dịp xem qua pull request của tôi chưa?" },
        { formula: "Are we on track for [Deadline / Event]?", use: "Milestone status check", eg: "Are we on track for the Friday release?", vi: "Chúng ta có đang đúng tiến độ cho đợt release thứ Sáu không?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Polite executive formula: 'Have you had a chance to check...?'"
    },
    {
      category: "5. Clarification & Deep Dive",
      icon: "💡",
      badge: "What does it mean? Explain how?",
      description: "Clarify technical specifications, architectural flows, or deep logic.",
      triggers: [
        { formula: "Could you clarify how [S + V]?", use: "Ask for deeper explanation of a mechanism", eg: "Could you clarify how this authentication token works?", vi: "Bạn có thể giải thích rõ hơn mã xác thực này hoạt động thế nào không?" },
        { formula: "What do you mean by [Term / Phrase]?", use: "Ask for definition of technical jargon", eg: "What do you mean by 'asynchronous fallback'?", vi: "Ý bạn là gì khi nói 'dự phòng bất đồng bộ'?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Direct & clear: 'Could you clarify how...?'"
    }
  ];

  const CHEATSHEET_TENSES = [
    {
      group: "Present Tenses",
      items: [
        {
          name: "1. Present Simple",
          formula: "(+) S + V(s/es) | (-) S + do/does not + V | (?) Do/Does + S + V?",
          quasm: "Wh- + do/does + S + V-inf?",
          signals: "always, usually, often, every day, rarely",
          use: "Habits, universal truths, fixed timetables and routines.",
          example: "How often do you review pull requests?"
        },
        {
          name: "2. Present Continuous",
          formula: "(+) S + am/is/are + V-ing | (-) S + am/is/are not + V-ing",
          quasm: "Wh- + am/is/are + S + V-ing?",
          signals: "now, right now, at the moment, currently",
          use: "Actions happening right now or definite planned arrangements.",
          example: "What is the team working on right now?"
        },
        {
          name: "3. Present Perfect",
          formula: "(+) S + have/has + V3/ed | (-) S + have/has not + V3/ed",
          quasm: "Wh- + have/has + S + V3/ed?",
          signals: "already, yet, just, ever, never, since, for, recently",
          use: "Actions starting in past continuing to present, or life experiences.",
          example: "How long have you lived here?"
        }
      ]
    },
    {
      group: "Past Tenses",
      items: [
        {
          name: "4. Past Simple",
          formula: "(+) S + V2/ed | (-) S + did not + V-inf | (?) Did + S + V-inf?",
          quasm: "Wh- + did + S + V-inf?",
          signals: "yesterday, ago, last week, in 2020",
          use: "Completed actions at a definite point in the past.",
          example: "When did you graduate?"
        },
        {
          name: "5. Past Continuous",
          formula: "(+) S + was/were + V-ing | (-) S + wasn't/weren't + V-ing",
          quasm: "Wh- + was/were + S + V-ing?",
          signals: "at 8 PM yesterday, while, when",
          use: "Action in progress at a specific past moment.",
          example: "What were you doing when the alarm rang?"
        }
      ]
    }
  ];
</script>

<svelte:window onclick={(e) => {
  const target = e.target as HTMLElement;
  if (!target.closest('.grammar-dropdown-container')) {
    isDropdownOpen = false;
  }
}} />

<div class="w-full max-w-6xl mx-auto space-y-6 pb-12">
  <!-- Header Title -->
  <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-0.5 rounded text-[10px]">
          Grammar Gym
        </span>
      </div>
      <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)] mt-1">
        Grammar Gym & Interactive Drills
      </h1>
      <p class="text-sm font-serif italic text-[var(--text-muted)] mt-1">
        Master English structures through active recall, sentence unscrambling, and instant feedback.
      </p>
    </div>

    <!-- Mode Switcher: Practice Drills vs Master Cheatsheet -->
    <div class="flex items-center bg-[var(--bg-inner)] p-1 rounded-xl border border-[var(--border-main)]">
      <button
        onclick={() => activeView = 'practice'}
        class={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center gap-1.5 ${
          activeView === 'practice'
            ? 'bg-[var(--accent-primary)] text-white shadow-sm'
            : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
        }`}
      >
        <Dumbbell class="w-3.5 h-3.5" />
        <span>Practice Drills</span>
      </button>

      <button
        onclick={() => activeView = 'cheatsheet'}
        class={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center gap-1.5 ${
          activeView === 'cheatsheet'
            ? 'bg-[var(--accent-primary)] text-white shadow-sm'
            : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
        }`}
      >
        <BookOpen class="w-3.5 h-3.5" />
        <span>Cheatsheet</span>
      </button>
    </div>
  </div>

  {#if activeView === 'practice'}
    <!-- Topic Selection & Filter Bar (matches 7.png) -->
    <section class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-3">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <Filter class="w-4 h-4 text-[var(--accent-primary)]" />
          <span class="text-xs font-semibold text-[var(--text-main)]">Select Structure or Question Type:</span>
        </div>

        <!-- Dropdown Selector -->
        <div class="relative grammar-dropdown-container">
          <button
            onclick={() => isDropdownOpen = !isDropdownOpen}
            class="w-full sm:w-64 px-3.5 py-2 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] hover:border-[var(--accent-primary)] text-[var(--text-main)] text-xs font-semibold flex items-center justify-between transition cursor-pointer"
          >
            <div class="flex items-center gap-2 truncate">
              <span>{activeCategoryInfo().category_icon}</span>
              <span class="truncate">{activeCategoryInfo().tense_category}</span>
            </div>
            <ChevronDown class={`w-3.5 h-3.5 text-[var(--text-muted)] transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {#if isDropdownOpen}
            <div class="absolute right-0 top-full mt-2 w-80 max-h-80 overflow-y-auto bg-[var(--bg-card)] border border-[var(--border-main)] rounded-2xl shadow-xl z-50 p-2 space-y-1">
              <div class="px-1 pb-1">
                <input
                  type="text"
                  bind:value={topicSearch}
                  placeholder="Search tenses..."
                  class="w-full px-3 py-1.5 rounded-lg bg-[var(--bg-inner)] border border-[var(--border-main)] text-[var(--text-main)] text-xs outline-none focus:border-[var(--accent-primary)]"
                />
              </div>

              {#if !topicSearch.trim()}
                <button
                  onclick={() => handleSelectCategory('all')}
                  class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between cursor-pointer ${
                    selectedCategory === 'all'
                      ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold'
                      : 'hover:bg-[var(--bg-inner)] text-[var(--text-main)]'
                  }`}
                >
                  <div class="flex items-center gap-2">
                    <span>⚡</span>
                    <span>All Tenses & Questions</span>
                  </div>
                  {#if selectedCategory === 'all'}
                    <Check class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  {/if}
                </button>
                <div class="h-px bg-[var(--border-main)] my-1"></div>
              {/if}

              {#each filteredCategories() as cat}
                <button
                  onclick={() => handleSelectCategory(cat.tense_category)}
                  class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between cursor-pointer ${
                    selectedCategory === cat.tense_category
                      ? 'bg-[var(--accent-primary-light)] text-[var(--accent-primary)] font-bold'
                      : 'hover:bg-[var(--bg-inner)] text-[var(--text-main)]'
                  }`}
                >
                  <div class="flex items-center gap-2 truncate">
                    <span>{cat.category_icon}</span>
                    <span class="truncate">{cat.tense_category}</span>
                  </div>
                  <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-[var(--bg-inner)] text-[var(--text-subtle)] font-mono">
                    {cat.count}
                  </span>
                </button>
              {/each}
            </div>
          {/if}
        </div>
      </div>

      <!-- Quick Pills -->
      <div class="flex items-center gap-2 overflow-x-auto pb-1 pt-1 no-scrollbar text-xs">
        <button
          onclick={() => handleSelectCategory('all')}
          class={`pill-filter ${selectedCategory === 'all' ? 'active' : ''}`}
        >
          <span>⚡ All</span>
        </button>

        {#each categories as cat}
          <button
            onclick={() => handleSelectCategory(cat.tense_category)}
            class={`pill-filter ${selectedCategory === cat.tense_category ? 'active' : ''}`}
          >
            <span>{cat.category_icon}</span>
            <span>{cat.tense_category}</span>
          </button>
        {/each}
      </div>
    </section>

    <!-- Practice Drill Card -->
    {#if loading}
      <div class="flex flex-col items-center justify-center py-20 text-[var(--text-muted)] space-y-3">
        <RefreshCw class="w-8 h-8 animate-spin text-[var(--accent-primary)]" />
        <p class="text-sm font-medium font-serif italic">Curating grammar drill...</p>
      </div>
    {:else if currentDrill}
      <article class="journal-card p-6 sm:p-8 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-6">
        <!-- Drill Header -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-2xl">{currentDrill.category_icon || '⚡'}</span>
            <div>
              <div class="flex items-center gap-2">
                <h2 class="font-serif text-lg font-bold text-[var(--text-main)]">{currentDrill.tense_category}</h2>
                <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-[var(--accent-primary-light)] text-[var(--accent-primary)] border border-[var(--accent-primary-border)]">
                  {currentDrill.level}
                </span>
              </div>
              <p class="text-xs text-[var(--text-muted)]">
                {currentDrill.type === 'indirect' ? 'Polite Indirect Question' : (currentDrill.type === 'tag_question' ? 'Tag Question Formation' : 'QUASM Question Formation')}
              </p>
            </div>
          </div>

          <button
            onclick={() => loadDrill(selectedCategory)}
            class="p-2.5 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold border border-[var(--border-main)]"
            title="Next question"
          >
            <RefreshCw class="w-3.5 h-3.5" />
            <span>Next Question</span>
          </button>
        </div>

        <!-- Context & Instruction Box -->
        <div class="p-5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-3">
          <div class="space-y-1">
            <span class="journal-badge text-[var(--text-subtle)]">Context Statement</span>
            <p class="text-base font-serif italic font-semibold text-[var(--text-main)] leading-relaxed">
              “{currentDrill.prompt_context}”
            </p>
            {#if currentDrill.prompt_vi}
              <p class="text-xs text-[var(--text-muted)] pt-0.5">
                👉 {currentDrill.prompt_vi}
              </p>
            {/if}
          </div>

          <!-- Goal / Instruction Banner -->
          <div class="p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] flex items-start gap-2.5">
            <Lightbulb class="w-4 h-4 text-[var(--accent-primary)] shrink-0 mt-0.5" />
            <div>
              <span class="text-xs font-bold text-[var(--text-main)]">Instruction:</span>
              <p class="text-xs text-[var(--text-muted)] font-medium">{currentDrill.instruction}</p>
            </div>
          </div>
        </div>

        <!-- Mode Toggle & Input Area -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-[var(--text-main)]">Your Formed Question:</span>

            <!-- Mode Switcher -->
            <div class="flex items-center p-0.5 rounded-lg bg-[var(--bg-inner)] border border-[var(--border-main)] text-xs">
              <button
                onclick={() => inputMode = 'type'}
                class={`px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                  inputMode === 'type'
                    ? 'bg-[var(--accent-primary)] text-white shadow-sm'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
                }`}
              >
                ⌨️ Typing Mode
              </button>
              <button
                onclick={() => inputMode = 'scramble'}
                class={`px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                  inputMode === 'scramble'
                    ? 'bg-[var(--accent-primary)] text-white shadow-sm'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
                }`}
              >
                🧩 Word Tiles
              </button>
            </div>
          </div>

          {#if inputMode === 'scramble'}
            <!-- Word Scramble Interactive Tiles Area -->
            <div class="p-4 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-4">
              <!-- Slot -->
              <div class="min-h-[52px] p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] flex flex-wrap items-center gap-2">
                {#if selectedScrambleTokens.length === 0}
                  <span class="text-xs text-[var(--text-subtle)] font-serif italic">Click word tiles below to form your sentence...</span>
                {:else}
                  {#each selectedScrambleTokens as tok}
                    <button
                      onclick={() => removeSelectedToken(tok)}
                      class="px-3 py-1.5 rounded-xl bg-[var(--accent-primary)] text-white text-xs font-bold shadow-sm hover:bg-red-600 transition cursor-pointer flex items-center gap-1"
                      title="Click to remove"
                    >
                      <span>{tok.word}</span>
                    </button>
                  {/each}
                {/if}
              </div>

              <!-- Available Tiles -->
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="journal-badge text-[var(--text-subtle)]">Word Bank</span>
                  {#if selectedScrambleTokens.length > 0 && !checked}
                    <button
                      onclick={resetScramble}
                      class="text-xs text-[var(--text-muted)] hover:text-[var(--accent-primary)] flex items-center gap-1 transition cursor-pointer"
                    >
                      <RotateCcw class="w-3 h-3" />
                      <span>Reset tiles</span>
                    </button>
                  {/if}
                </div>

                <div class="flex flex-wrap gap-2 pt-1">
                  {#each availableScrambleTokens as tok}
                    <button
                      onclick={() => toggleScrambleWord(tok)}
                      disabled={tok.used || checked}
                      class={`px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer border ${
                        tok.used
                          ? 'opacity-30 bg-[var(--bg-card)] border-[var(--border-main)] text-[var(--text-subtle)] line-through cursor-not-allowed'
                          : 'bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] border-[var(--border-main)] hover:border-[var(--accent-primary)] shadow-sm'
                      }`}
                    >
                      {tok.word}
                    </button>
                  {/each}
                </div>
              </div>
            </div>
          {:else}
            <!-- Typing Area -->
            <input
              type="text"
              bind:value={userInput}
              onkeydown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleCheck();
                }
              }}
              placeholder="Type your question here (e.g., How often does she study...?)"
              class="w-full bg-[var(--bg-inner)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-2xl px-4 py-3.5 text-base text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none transition font-medium"
            />
          {/if}

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <button
              onclick={() => showHint = !showHint}
              class="text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--accent-primary)] flex items-center gap-1.5 transition cursor-pointer"
            >
              {#if showHint}
                <EyeOff class="w-3.5 h-3.5" />
                <span>Hide Structure Hint</span>
              {:else}
                <Eye class="w-3.5 h-3.5" />
                <span>Show Structure Hint</span>
              {/if}
            </button>

            <button
              onclick={handleCheck}
              disabled={!userInput.trim()}
              class="px-6 py-2.5 rounded-xl btn-forest disabled:opacity-50 font-bold text-sm transition shadow-sm cursor-pointer"
            >
              Check Question (Enter)
            </button>
          </div>

          <!-- QUASM Hint Box -->
          {#if showHint && currentDrill.quasm_breakdown}
            <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1">
              <div class="flex items-center gap-1.5 text-[var(--accent-primary)] text-xs font-bold">
                <Sparkles class="w-3.5 h-3.5" />
                <span>QUASM Formula:</span>
              </div>
              <p class="text-xs font-mono text-[var(--text-main)]">{currentDrill.quasm_breakdown}</p>
            </div>
          {/if}
        </div>

        <!-- Result Breakdown & Grammar Rules -->
        {#if checked && diffResult}
          <div class="p-5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <Award class={`w-5 h-5 ${diffResult.passed ? 'text-emerald-600' : 'text-amber-600'}`} />
                <div>
                  <span class="text-sm font-semibold text-[var(--text-main)]">Accuracy: </span>
                  <span class={`text-lg font-bold font-mono ${diffResult.passed ? 'text-emerald-600' : 'text-amber-600'}`}>
                    {diffResult.accuracy}%
                  </span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <button
                  onclick={() => playAudio(false)}
                  class="px-3 py-1.5 rounded-xl bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border border-[var(--border-main)]"
                  title="Play audio"
                >
                  <Volume2 class={`w-3.5 h-3.5 text-[var(--accent-primary)] ${isAudioPlaying ? 'animate-bounce' : ''}`} />
                  <span>Listen</span>
                </button>

                <span class={`px-3 py-1 rounded-full text-xs font-bold ${
                  diffResult.passed ? 'bg-emerald-500/15 text-emerald-700 border border-emerald-400/30' : 'bg-amber-500/15 text-amber-700 border border-amber-400/30'
                }`}>
                  {diffResult.passed ? '🎉 Perfect Question!' : '⚡ Review Formula'}
                </span>
              </div>
            </div>

            <!-- Visual Word Diff -->
            <div class="p-4 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] space-y-2">
              <span class="journal-badge text-[var(--text-subtle)]">Word-by-word Evaluation</span>
              <div class="flex flex-wrap gap-1.5 text-sm font-mono pt-1">
                {#each diffResult.tokens as tok}
                  {#if tok.type === 'correct'}
                    <span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-700 border border-emerald-400/30 font-semibold">
                      {tok.word}
                    </span>
                  {:else if tok.type === 'wrong'}
                    <span class="px-2 py-0.5 rounded bg-red-500/15 text-red-700 line-through border border-red-400/30" title="Incorrect">
                      {tok.word}
                    </span>
                  {:else if tok.type === 'missing'}
                    <span class="px-2 py-0.5 rounded bg-amber-500/15 text-amber-700 underline border border-amber-400/30" title="Missing">
                      [{tok.match}]
                    </span>
                  {/if}
                {/each}
              </div>
            </div>

            <!-- Target Question & QUASM Analysis -->
            <div class="p-4 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] space-y-3 text-sm">
              <div>
                <span class="journal-badge text-[var(--text-subtle)]">Correct Question</span>
                <p class="text-base font-serif font-bold text-[var(--text-main)] pt-0.5">{currentDrill.target_question}</p>
                {#if currentDrill.target_vi}
                  <p class="text-xs text-[var(--text-muted)] font-serif italic pt-0.5">👉 {currentDrill.target_vi}</p>
                {/if}
              </div>

              {#if currentDrill.quasm_breakdown}
                <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1">
                  <span class="text-xs font-bold text-[var(--accent-primary)]">QUASM Structure:</span>
                  <p class="text-xs font-mono text-[var(--text-main)]">{currentDrill.quasm_breakdown}</p>
                </div>
              {/if}

              {#if currentDrill.grammar_tip}
                <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1">
                  <div class="flex items-center gap-1.5 text-xs font-bold text-emerald-700 dark:text-emerald-300">
                    <CheckCircle2 class="w-3.5 h-3.5" />
                    <span>Grammar Tip:</span>
                  </div>
                  <p class="text-xs text-[var(--text-muted)] leading-relaxed">{currentDrill.grammar_tip}</p>
                </div>
              {/if}
            </div>
          </div>
        {/if}
      </article>
    {/if}

  {:else}
    <!-- Cheatsheet View -->
    <div class="space-y-6">
      <div class="flex items-center gap-2 p-1 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
        <button
          onclick={() => cheatsheetTab = 'mindsets'}
          class={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 cursor-pointer ${
            cheatsheetTab === 'mindsets'
              ? 'bg-[var(--accent-primary)] text-white shadow-sm'
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <Lightbulb class="w-4 h-4" />
          <span>💡 5 Question Mindsets</span>
        </button>

        <button
          onclick={() => cheatsheetTab = 'tenses'}
          class={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 cursor-pointer ${
            cheatsheetTab === 'tenses'
              ? 'bg-[var(--accent-primary)] text-white shadow-sm'
              : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <Clock class="w-4 h-4" />
          <span>⏱️ 12 Verb Tenses Reference</span>
        </button>
      </div>

      {#if cheatsheetTab === 'mindsets'}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          {#each QUESTION_MINDSETS as mindset}
            <div class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-4 flex flex-col justify-between">
              <div class="space-y-3">
                <div class="flex items-start justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <span class="text-2xl">{mindset.icon}</span>
                    <h3 class="font-serif font-bold text-sm text-[var(--text-main)]">{mindset.category}</h3>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[var(--bg-inner)] text-[var(--text-muted)] border border-[var(--border-main)]">
                    {mindset.badge}
                  </span>
                </div>

                <p class="text-xs text-[var(--text-muted)] leading-relaxed">{mindset.description}</p>

                <div class="space-y-2 pt-1">
                  {#each mindset.triggers as trig}
                    <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1 text-xs">
                      <div class="font-mono font-bold text-[var(--accent-primary)]">
                        {trig.formula}
                      </div>
                      <div class="text-[var(--text-muted)] italic text-[11px]">
                        👉 {trig.use}
                      </div>
                      <div class="pt-1 font-serif italic text-[var(--text-main)]">
                        “{trig.eg}”
                      </div>
                      <div class="text-[11px] text-[var(--text-subtle)]">
                        ({trig.vi})
                      </div>
                    </div>
                  {/each}
                </div>
              </div>

              <div class="p-2.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] text-[11px] text-[var(--accent-primary)] font-medium">
                {mindset.mindsetTrap}
              </div>
            </div>
          {/each}
        </div>
      {:else}
        <div class="space-y-6">
          {#each CHEATSHEET_TENSES as section}
            <div class="journal-card p-5 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-4">
              <h2 class="font-serif text-base font-bold text-[var(--text-main)] flex items-center gap-2">
                <Clock class="w-4 h-4 text-[var(--accent-primary)]" />
                <span>{section.group}</span>
              </h2>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {#each section.items as item}
                  <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
                    <h3 class="font-bold text-xs text-[var(--accent-primary)]">{item.name}</h3>
                    <p class="text-xs font-mono text-[var(--text-main)]">{item.formula}</p>
                    <p class="text-xs text-[var(--text-muted)] leading-relaxed">{item.use}</p>
                    <div class="text-xs font-serif italic text-[var(--text-main)] pt-1 border-t border-[var(--border-main)]">
                      “{item.example}”
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>
