<script lang="ts">
  import { onMount } from 'svelte';
  import { GetGrammarDrill, GetGrammarCategories, CheckGrammarAnswer } from '../../../wailsjs/go/main/App.js';
  import { playTTS, stopAudio } from '../utils/audio';
  import { 
    HelpCircle, 
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
    Layers,
    Filter,
    Lightbulb,
    CheckCircle2,
    Clock,
    ArrowRight
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
      if (drill?.id) {
        if (!seenIds.includes(drill.id)) {
          seenIds = [...seenIds, drill.id];
        }
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
    userInput = selectedScrambleTokens.map(t => t.word).join(' ').replace(/\s+([?,.])/g, '$1');
  }

  function removeSelectedToken(token: { id: number; word: string }) {
    if (checked) return;
    selectedScrambleTokens = selectedScrambleTokens.filter(t => t.id !== token.id);
    const found = availableScrambleTokens.find(t => t.id === token.id);
    if (found) found.used = false;
    userInput = selectedScrambleTokens.map(t => t.word).join(' ').replace(/\s+([?,.])/g, '$1');
  }

  function resetScramble() {
    selectedScrambleTokens = [];
    availableScrambleTokens.forEach(t => t.used = false);
    userInput = '';
  }

  async function handleCheck() {
    if (!currentDrill?.target_question || !userInput.trim()) return;
    try {
      diffResult = await CheckGrammarAnswer(currentDrill.target_question, userInput.trim());
      checked = true;
    } catch (e) {
      console.error(e);
    }
  }

  function playAudio(slow = false) {
    if (!currentDrill?.target_question) return;
    isAudioPlaying = true;
    playTTS(currentDrill.target_question, slow ? 0.75 : 1.0, 'grammar').then(() => {
      isAudioPlaying = false;
    });
  }

  let activeCategoryInfo = $derived(() => {
    if (selectedCategory === 'all') {
      return { tense_category: 'All Tenses & Questions', category_icon: '⚡', count: categories.reduce((acc, c) => acc + c.count, 0) };
    }
    const found = categories.find(c => c.tense_category === selectedCategory);
    return found || { tense_category: selectedCategory, category_icon: '⚡', count: 0 };
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

  // 💡 5 Intent-Based Question Mindsets + Buying-Time Fillers
  const QUESTION_MINDSETS = [
    {
      category: "1. Feasibility & Plans",
      icon: "🚀",
      badge: "Can we? When will we?",
      color: "border-blue-500/30 bg-blue-500/5",
      headerColor: "text-blue-400",
      description: "Ask whether an action is possible or inquire about scheduled timelines directly without complex mental translation.",
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
      color: "border-amber-500/30 bg-amber-500/5",
      headerColor: "text-amber-400",
      description: "Ask about duration, budget estimation, or required engineering team headcount (Agile / Sprint planning).",
      triggers: [
        { formula: "How long will it take (you) to [V-inf]?", use: "Fixed Lego chunk for time estimation (Never translate 'lose time')", eg: "How long will it take you to fix this bug?", vi: "Mất bao lâu để bạn sửa xong lỗi này?" },
        { formula: "How many [people/engineers] do you need to [V-inf]?", use: "Ask for headcount / resource allocation", eg: "How many engineers do you need to complete this product?", vi: "Bạn cần bao nhiêu kỹ sư để hoàn thành sản phẩm này?" },
        { formula: "What team size are we looking at to [V-inf]?", use: "Project management phrasing for team capacity", eg: "What team size are we looking at to deliver this feature?", vi: "Quy mô nhóm cần thiết là bao nhiêu để bàn giao tính năng này?" },
        { formula: "How much does it cost to [V-inf]?", use: "Cost and expense inquiries", eg: "How much does it cost to upgrade the server instance?", vi: "Mất bao nhiêu tiền để nâng cấp máy chủ?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Drop literal 'lose/spend' thinking ➔ Trigger fixed chunk: 'How long will it take you to...'"
    },
    {
      category: "3. Feedback & Problem Solving",
      icon: "💬",
      badge: "What do you think? How to handle?",
      color: "border-purple-500/30 bg-purple-500/5",
      headerColor: "text-purple-400",
      description: "Gather feedback on technical approaches, seek advice, or address edge case incidents.",
      triggers: [
        { formula: "What do you think about [Noun / V-ing]?", use: "Ask for opinions regarding an architectural or design idea", eg: "What do you think about migrating to PostgreSQL?", vi: "Bạn nghĩ sao về việc chuyển sang PostgreSQL?" },
        { formula: "How should we handle [Issue / Edge Case]?", use: "Collaborative problem-solving opener", eg: "How should we handle this unexpected edge case?", vi: "Chúng ta nên xử lý trường hợp biên này như thế nào?" },
        { formula: "What are your thoughts on [Topic]?", use: "Polite executive inquiry for partner/stakeholder view", eg: "What are your thoughts on our proposed architecture?", vi: "Suy nghĩ của bạn về kiến trúc đề xuất là gì?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Be direct & professional: 'What do you think about...?'"
    },
    {
      category: "4. Status & Confirmation",
      icon: "🔍",
      badge: "Any updates? Ready?",
      color: "border-emerald-500/30 bg-emerald-500/5",
      headerColor: "text-emerald-400",
      description: "Check progress politely and ask if someone has had time to review documents without applying undue pressure.",
      triggers: [
        { formula: "Have you had a chance to [V-inf]?", use: "Polite inquiry to check if someone reviewed a PR/email", eg: "Have you had a chance to review my pull request?", vi: "Bạn đã có dịp xem qua pull request của tôi chưa?" },
        { formula: "Are we on track for [Deadline / Event]?", use: "Milestone status check", eg: "Are we on track for the Friday release?", vi: "Chúng ta có đang đúng tiến độ cho đợt release thứ Sáu không?" },
        { formula: "Is [Item] ready for [Stage]?", use: "Readiness verification", eg: "Is the staging environment ready for QA testing?", vi: "Môi trường staging đã sẵn sàng cho QA test chưa?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Polite executive formula: 'Have you had a chance to check...?'"
    },
    {
      category: "5. Clarification & Deep Dive",
      icon: "💡",
      badge: "What does it mean? Explain how?",
      color: "border-cyan-500/30 bg-cyan-500/5",
      headerColor: "text-cyan-400",
      description: "Clarify technical specifications, architectural flows, or deep logic.",
      triggers: [
        { formula: "Could you clarify how [S + V]?", use: "Ask for deeper explanation of a mechanism", eg: "Could you clarify how this authentication token works?", vi: "Bạn có thể giải thích rõ hơn mã xác thực này hoạt động thế nào không?" },
        { formula: "What do you mean by [Term / Phrase]?", use: "Ask for definition of technical jargon or ambiguous term", eg: "What do you mean by 'asynchronous fallback'?", vi: "Ý bạn là gì khi nói 'dự phòng bất đồng bộ'?" },
        { formula: "Could you walk me through [Flow / Code]?", use: "Request a step-by-step walkthrough", eg: "Could you walk me through the checkout workflow?", vi: "Bạn có thể dẫn tôi đi qua luồng thanh toán được không?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Direct & clear: 'Could you clarify how...?'"
    },
    {
      category: "6. Buying-Time Fillers",
      icon: "🗣️",
      badge: "Maintain flow & buy thinking time",
      color: "border-rose-500/30 bg-rose-500/5",
      headerColor: "text-rose-400",
      description: "Use natural conversational openers when you need 1-2 seconds to formulate thoughts smoothly without awkward silence.",
      triggers: [
        { formula: "Quick question, [Question]...", use: "Signal that you are asking a brief question", eg: "Quick question, who is in charge of deployment today?", vi: "Hỏi nhanh câu này nhé, hôm nay ai phụ trách việc deploy vậy?" },
        { formula: "Just to make sure, [Question / Statement]...", use: "Confirm alignment smoothly", eg: "Just to make sure, are we meeting at 3 PM today?", vi: "Để cho chắc chắn thì, chúng ta có họp lúc 3h chiều nay không?" },
        { formula: "I was just wondering, [Question]...", use: "Soft, polite opening for sensitive topics", eg: "I was wondering, how long will this task take?", vi: "Tôi chỉ đang thắc mắc là, task này sẽ mất bao lâu?" },
        { formula: "Could you help me understand [Topic]...", use: "Professional way to ask for assistance", eg: "Could you help me understand why this test failed?", vi: "Bạn có thể giúp tôi hiểu tại sao bài test này lại lỗi không?" }
      ],
      mindsetTrap: "💡 Mindset Shift: Opening fillers give your vocal cords a head start while your brain queues the rest!"
    }
  ];

  // 12 Tenses Cheat Sheet Data
  const CHEATSHEET_TENSES = [
    {
      group: "Present Tenses",
      color: "border-blue-500/30 bg-blue-500/5",
      items: [
        {
          name: "1. Present Simple",
          formula: "(+) S + V(s/es) | (-) S + do/does not + V | (?) Do/Does + S + V?",
          quasm: "Wh- + do/does + S + V-inf?",
          signals: "always, usually, often, every day, rarely, once a week",
          use: "Habits, universal truths, fixed timetables and routines.",
          example: "How often do you review pull requests?"
        },
        {
          name: "2. Present Continuous",
          formula: "(+) S + am/is/are + V-ing | (-) S + am/is/are not + V-ing | (?) Am/Is/Are + S + V-ing?",
          quasm: "Wh- + am/is/are + S + V-ing?",
          signals: "now, right now, at the moment, currently, this week",
          use: "Actions happening right now or definite planned future arrangements.",
          example: "What is the frontend team working on right now?"
        },
        {
          name: "3. Present Perfect",
          formula: "(+) S + have/has + V3/ed | (-) S + have/has not + V3/ed | (?) Have/Has + S + V3/ed?",
          quasm: "Wh- + have/has + S + V3/ed?",
          signals: "already, yet, just, ever, never, since, for, recently",
          use: "Actions starting in the past continuing to present, or life experiences.",
          example: "How long have you lived in Melbourne?"
        },
        {
          name: "4. Present Perfect Continuous",
          formula: "(+) S + have/has been + V-ing | (-) S + haven't/hasn't been + V-ing | (?) Have/Has + S + been + V-ing?",
          quasm: "Wh- + have/has + S + been + V-ing?",
          signals: "all day, for [hours], since morning, how long",
          use: "Emphasizes duration and continuous uninterrupted process up to now.",
          example: "How long has he been debugging this memory leak?"
        }
      ]
    },
    {
      group: "Past Tenses",
      color: "border-purple-500/30 bg-purple-500/5",
      items: [
        {
          name: "5. Past Simple",
          formula: "(+) S + V2/ed | (-) S + did not + V-inf | (?) Did + S + V-inf?",
          quasm: "Wh- + did + S + V-inf?",
          signals: "yesterday, ago, last week/month/year, in 2020",
          use: "Completed actions at a specific definite point in the past.",
          example: "When did you graduate from university?"
        },
        {
          name: "6. Past Continuous",
          formula: "(+) S + was/were + V-ing | (-) S + wasn't/weren't + V-ing | (?) Was/Were + S + V-ing?",
          quasm: "Wh- + was/were + S + V-ing?",
          signals: "at 8 PM yesterday, while, when (interrupted action)",
          use: "Action in progress at a specific past moment or interrupted by another event.",
          example: "What were you doing when the fire alarm rang?"
        },
        {
          name: "7. Past Perfect",
          formula: "(+) S + had + V3/ed | (-) S + had not + V3/ed | (?) Had + S + V3/ed?",
          quasm: "Wh- + had + S + V3/ed?",
          signals: "before, after, by the time, as soon as, already",
          use: "Action completed BEFORE another past action or past point in time.",
          example: "Had they finalized the contract before the deadline?"
        }
      ]
    },
    {
      group: "Future & Special Question Structures",
      color: "border-emerald-500/30 bg-emerald-500/5",
      items: [
        {
          name: "8. Future Forms (Will vs Be Going To)",
          formula: "Will + V-inf (Instant decision/Prediction) | Be going to + V-inf (Prior plan/Intent)",
          quasm: "What will you do? vs What are you going to do?",
          signals: "tomorrow, next week, soon, in the future",
          use: "Predictions, spontaneous decisions, or prior established plans.",
          example: "What are you going to do this upcoming weekend?"
        },
        {
          name: "9. Polite Indirect Questions",
          formula: "Could you tell me / Do you know + [Wh- + S + V]?",
          quasm: "Golden Rule: No inversion (Word order returns to affirmative S + V)!",
          signals: "Could you tell me..., Do you know if/whether...",
          use: "Professional communication, emails, hospitality, asking for directions.",
          example: "Could you tell me where the nearest subway station is?"
        },
        {
          name: "10. Tag Questions",
          formula: "Affirmative (+) ➔ Negative Tag (-) | Negative (-) ➔ Affirmative Tag (+)",
          quasm: "Tag auxiliary verb mirrors the tense of the main clause.",
          signals: "..., aren't you? / ..., didn't they? / ..., shall we? (Let's)",
          use: "Confirming information or establishing friendly conversational rapport.",
          example: "You are coming to the team meeting tomorrow, aren't you?"
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

<div class="max-w-4xl mx-auto space-y-6">
  <!-- Top Navigation & View Switcher -->
  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg backdrop-blur-md">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500/20 to-orange-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400 shadow-inner">
        <Zap class="w-5 h-5" />
      </div>
      <div>
        <h1 class="text-base font-bold text-slate-100 flex items-center gap-2">
          Grammar & Question Gym
          <span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-500/20 text-amber-400 border border-amber-500/30">QUASM</span>
        </h1>
        <p class="text-xs text-slate-400">Master 12 English Tenses & QUASM Question Formation</p>
      </div>
    </div>

    <!-- View Mode Switcher -->
    <div class="flex items-center p-1 rounded-xl bg-slate-950 border border-slate-800">
      <button
        onclick={() => activeView = 'practice'}
        class={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
          activeView === 'practice'
            ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
            : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        <Zap class="w-3.5 h-3.5" />
        <span>Practice Gym</span>
      </button>

      <button
        onclick={() => activeView = 'cheatsheet'}
        class={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
          activeView === 'cheatsheet'
            ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
            : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        <BookOpen class="w-3.5 h-3.5" />
        <span>Master Cheatsheet</span>
      </button>
    </div>
  </div>

  {#if activeView === 'practice'}
    <!-- Topic Selection & Filter Bar -->
    <div class="relative z-30 bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg backdrop-blur-md space-y-3">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <Filter class="w-3.5 h-3.5" />
          </div>
          <span class="text-xs font-bold text-slate-200">Select Tense or Question Type</span>
        </div>

        <!-- Dropdown Selector -->
        <div class="relative grammar-dropdown-container">
          <button
            onclick={() => isDropdownOpen = !isDropdownOpen}
            class="w-full sm:w-64 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700/80 hover:border-slate-600 text-slate-200 text-xs font-semibold flex items-center justify-between transition cursor-pointer shadow-inner"
          >
            <div class="flex items-center gap-2 truncate">
              <span>{activeCategoryInfo().category_icon}</span>
              <span class="truncate">{activeCategoryInfo().tense_category}</span>
            </div>
            <ChevronDown class={`w-3.5 h-3.5 text-slate-400 transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {#if isDropdownOpen}
            <div class="absolute right-0 top-full mt-2 w-80 max-h-80 overflow-y-auto bg-slate-950 border border-slate-700 rounded-2xl shadow-2xl shadow-black/90 z-50 p-2 backdrop-blur-xl space-y-1 ring-1 ring-slate-700/50">
              <div class="px-1 pb-1">
                <input
                  type="text"
                  bind:value={topicSearch}
                  placeholder="Search tenses (e.g. Perfect, Past, Tag)..."
                  class="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-slate-200 placeholder-slate-500 text-xs outline-none focus:border-blue-500 transition"
                />
              </div>

              {#if !topicSearch.trim()}
                <button
                  onclick={() => handleSelectCategory('all')}
                  class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between transition cursor-pointer ${
                    selectedCategory === 'all' 
                      ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30' 
                      : 'hover:bg-slate-900 text-slate-300'
                  }`}
                >
                  <div class="flex items-center gap-2.5">
                    <span class="text-base">⚡</span>
                    <span class="font-bold">All Tenses & Questions</span>
                  </div>
                  {#if selectedCategory === 'all'}
                    <Check class="w-3.5 h-3.5 text-blue-400" />
                  {/if}
                </button>
                <div class="h-px bg-slate-800 my-1"></div>
              {/if}

              {#each filteredCategories() as cat}
                <button
                  onclick={() => handleSelectCategory(cat.tense_category)}
                  class={`w-full px-3 py-2 rounded-xl text-left text-xs font-medium flex items-center justify-between transition cursor-pointer ${
                    selectedCategory === cat.tense_category 
                      ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30 font-semibold' 
                      : 'hover:bg-slate-900 text-slate-300'
                  }`}
                >
                  <div class="flex items-center gap-2.5 truncate">
                    <span class="text-base">{cat.category_icon}</span>
                    <span class="truncate">{cat.tense_category}</span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                      {cat.count}
                    </span>
                    {#if selectedCategory === cat.tense_category}
                      <Check class="w-3.5 h-3.5 text-blue-400" />
                    {/if}
                  </div>
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
          class={`px-3 py-1.5 rounded-xl whitespace-nowrap transition cursor-pointer flex items-center gap-1.5 font-medium text-xs ${
            selectedCategory === 'all'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20 font-bold'
              : 'bg-slate-950/70 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800'
          }`}
        >
          <span>⚡ All</span>
        </button>

        {#each categories as cat}
          <button
            onclick={() => handleSelectCategory(cat.tense_category)}
            class={`px-3 py-1.5 rounded-xl whitespace-nowrap transition cursor-pointer flex items-center gap-1.5 font-medium text-xs ${
              selectedCategory === cat.tense_category
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20 font-bold'
                : 'bg-slate-950/70 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <span>{cat.category_icon}</span>
            <span>{cat.tense_category}</span>
          </button>
        {/each}
      </div>
    </div>

    <!-- Practice Question Card -->
    {#if loading}
      <div class="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
        <RefreshCw class="w-8 h-8 animate-spin text-amber-500" />
        <p class="text-sm font-medium">Loading grammar drill...</p>
      </div>
    {:else if currentDrill}
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-6">
        <!-- Drill Header -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-2xl">{currentDrill.category_icon || '⚡'}</span>
            <div>
              <div class="flex items-center gap-2">
                <h2 class="text-lg font-bold text-slate-100">{currentDrill.tense_category}</h2>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  {currentDrill.level}
                </span>
              </div>
              <p class="text-xs text-slate-400">{currentDrill.type === 'indirect' ? 'Polite Indirect Question' : (currentDrill.type === 'tag_question' ? 'Tag Question Formation' : 'QUASM Question Formation')}</p>
            </div>
          </div>

          <button
            onclick={() => loadDrill(selectedCategory)}
            class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold shadow-sm active:scale-95"
            title="Next question"
          >
            <RefreshCw class="w-3.5 h-3.5" />
            <span>Next Question</span>
          </button>
        </div>

        <!-- Context & Instruction Box -->
        <div class="bg-slate-950/70 p-5 rounded-2xl border border-slate-800/90 space-y-3">
          <div class="space-y-1">
            <span class="text-[11px] uppercase tracking-wider font-bold text-slate-400">Context Statement:</span>
            <p class="text-base font-semibold text-slate-100 leading-relaxed">
              "{currentDrill.prompt_context}"
            </p>
            {#if currentDrill.prompt_vi}
              <p class="text-xs text-slate-400 italic">
                👉 {currentDrill.prompt_vi}
              </p>
            {/if}
          </div>

          <!-- Goal / Instruction Banner -->
          <div class="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-start gap-2.5">
            <Lightbulb class="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <span class="text-xs font-bold text-amber-300">Goal & Instruction:</span>
              <p class="text-xs text-amber-200/90 font-medium">{currentDrill.instruction}</p>
            </div>
          </div>
        </div>

        <!-- Mode Toggle & Input Area -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-slate-300">Your Question:</span>

            <!-- Mode Switcher: Type vs Scramble -->
            <div class="flex items-center p-0.5 rounded-lg bg-slate-950 border border-slate-800 text-[11px]">
              <button
                onclick={() => inputMode = 'type'}
                class={`px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                  inputMode === 'type' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                ⌨️ Typing Mode
              </button>
              <button
                onclick={() => inputMode = 'scramble'}
                class={`px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                  inputMode === 'scramble' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                🧩 Word Scramble
              </button>
            </div>
          </div>

          {#if inputMode === 'scramble'}
            <!-- Word Scramble Interactive Area -->
            <div class="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-4">
              <!-- Constructed Sentence Slot -->
              <div class="min-h-[52px] p-3 rounded-xl bg-slate-900/90 border border-slate-700/80 flex flex-wrap items-center gap-2">
                {#if selectedScrambleTokens.length === 0}
                  <span class="text-xs text-slate-500 italic">Click the word tiles below to form your question...</span>
                {:else}
                  {#each selectedScrambleTokens as tok}
                    <button
                      onclick={() => removeSelectedToken(tok)}
                      class="px-3 py-1.5 rounded-xl bg-blue-600 text-white text-xs font-bold shadow-md shadow-blue-500/20 hover:bg-red-500 transition cursor-pointer flex items-center gap-1 active:scale-95"
                      title="Click to remove"
                    >
                      <span>{tok.word}</span>
                    </button>
                  {/each}
                {/if}
              </div>

              <!-- Available Tiles to Click -->
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Word Bank:</span>
                  {#if selectedScrambleTokens.length > 0 && !checked}
                    <button
                      onclick={resetScramble}
                      class="text-[11px] text-slate-400 hover:text-amber-300 flex items-center gap-1 transition cursor-pointer"
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
                      class={`px-3.5 py-2 rounded-xl text-xs font-semibold transition active:scale-95 cursor-pointer border ${
                        tok.used 
                          ? 'opacity-30 bg-slate-900 border-slate-800 text-slate-600 line-through cursor-not-allowed' 
                          : 'bg-slate-900 hover:bg-slate-800 text-slate-200 border-slate-700 hover:border-blue-500 shadow-sm'
                      }`}
                    >
                      {tok.word}
                    </button>
                  {/each}
                </div>
              </div>
            </div>
          {:else}
            <!-- Typing Input Area -->
            <div class="relative">
              <input
                type="text"
                bind:value={userInput}
                onkeydown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleCheck();
                  }
                }}
                placeholder="Type your question here (e.g. How often does she study...?)"
                class="w-full bg-slate-950 border border-slate-700/80 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 rounded-2xl px-4 py-3.5 text-base text-slate-100 placeholder-slate-500 outline-none transition font-medium"
              />
            </div>
          {/if}

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <button
              onclick={() => showHint = !showHint}
              class="text-xs font-semibold text-slate-400 hover:text-slate-200 flex items-center gap-1.5 transition cursor-pointer"
            >
              {#if showHint}
                <EyeOff class="w-3.5 h-3.5" />
                <span>Hide QUASM Breakdown</span>
              {:else}
                <Eye class="w-3.5 h-3.5" />
                <span>Show QUASM Hint</span>
              {/if}
            </button>

            <button
              onclick={handleCheck}
              disabled={!userInput.trim()}
              class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 disabled:opacity-50 text-white font-bold text-sm transition shadow-lg shadow-amber-500/25 active:scale-95 cursor-pointer"
            >
              Check Question (Enter)
            </button>
          </div>

          <!-- QUASM Hint Box -->
          {#if showHint && currentDrill.quasm_breakdown}
            <div class="p-3.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 space-y-1">
              <div class="flex items-center gap-1.5 text-indigo-300 text-xs font-bold">
                <Sparkles class="w-3.5 h-3.5" />
                <span>QUASM Formula Breakdown:</span>
              </div>
              <p class="text-xs font-mono text-indigo-200">{currentDrill.quasm_breakdown}</p>
            </div>
          {/if}
        </div>

        <!-- Result Breakdown & Grammar Rules -->
        {#if checked && diffResult}
          <div class="bg-slate-950/90 rounded-2xl p-5 border border-slate-800 space-y-4 animate-fade-in">
            <!-- Score Header -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <Award class={`w-6 h-6 ${diffResult.passed ? 'text-emerald-400' : 'text-amber-400'}`} />
                <div>
                  <span class="text-sm font-bold text-slate-200">Accuracy Score: </span>
                  <span class={`text-xl font-extrabold ${diffResult.passed ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {diffResult.accuracy}%
                  </span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <button
                  onclick={() => playAudio(false)}
                  class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer"
                  title="Play audio pronunciation"
                >
                  <Volume2 class={`w-3.5 h-3.5 text-blue-400 ${isAudioPlaying ? 'animate-bounce' : ''}`} />
                  <span>Listen</span>
                </button>

                <span class={`px-3 py-1 rounded-full text-xs font-bold ${
                  diffResult.passed ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                }`}>
                  {diffResult.passed ? '🎉 Perfect Question!' : '⚡ Review Formula'}
                </span>
              </div>
            </div>

            <!-- Visual Word Diff -->
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800/80 space-y-2">
              <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Word-by-word Evaluation:</span>
              <div class="flex flex-wrap gap-2 text-base font-mono leading-relaxed pt-1">
                {#each diffResult.tokens as tok}
                  {#if tok.type === 'correct'}
                    <span class="px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                      {tok.word}
                    </span>
                  {:else if tok.type === 'wrong'}
                    <span class="px-2 py-0.5 rounded-lg bg-red-500/20 text-red-300 line-through border border-red-500/40" title="Incorrect word order or auxiliary">
                      {tok.word}
                    </span>
                  {:else if tok.type === 'missing'}
                    <span class="px-2 py-0.5 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 underline" title={`Missing: "${tok.match}"`}>
                      [{tok.match}]
                    </span>
                  {/if}
                {/each}
              </div>
            </div>

            <!-- Target Question & QUASM Analysis -->
            <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3 text-sm">
              <div>
                <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Correct Question:</span>
                <p class="text-base font-bold text-slate-100 pt-0.5">{currentDrill.target_question}</p>
                {#if currentDrill.target_vi}
                  <p class="text-xs text-slate-400 italic pt-0.5">{currentDrill.target_vi}</p>
                {/if}
              </div>

              <!-- QUASM Rule Highlight -->
              {#if currentDrill.quasm_breakdown}
                <div class="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1">
                  <span class="text-xs font-bold text-blue-300">QUASM Structure:</span>
                  <p class="text-xs font-mono text-blue-200">{currentDrill.quasm_breakdown}</p>
                </div>
              {/if}

              <!-- Grammar & Tense Explanation Tip -->
              {#if currentDrill.grammar_tip}
                <div class="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-1">
                  <div class="flex items-center gap-1.5 text-xs font-bold text-emerald-300">
                    <CheckCircle2 class="w-3.5 h-3.5" />
                    <span>Grammar Rule & Tense Explanation:</span>
                  </div>
                  <p class="text-xs text-emerald-200 leading-relaxed">{currentDrill.grammar_tip}</p>
                </div>
              {/if}
            </div>
          </div>
        {/if}
      </div>
    {/if}

  {:else}
    <!-- Master Cheatsheet View with Sub-Navigation -->
    <div class="space-y-6">
      <!-- Cheatsheet Sub-Tabs -->
      <div class="flex items-center gap-2 p-1.5 rounded-2xl bg-slate-900/90 border border-slate-800 backdrop-blur-md">
        <button
          onclick={() => cheatsheetTab = 'mindsets'}
          class={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 cursor-pointer ${
            cheatsheetTab === 'mindsets'
              ? 'bg-gradient-to-r from-amber-600 to-orange-600 text-white shadow-lg shadow-amber-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
          }`}
        >
          <Lightbulb class="w-4 h-4" />
          <span>💡 5 Question Mindsets (Intent Framework)</span>
        </button>

        <button
          onclick={() => cheatsheetTab = 'tenses'}
          class={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 cursor-pointer ${
            cheatsheetTab === 'tenses'
              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
          }`}
        >
          <Clock class="w-4 h-4" />
          <span>⏱️ 12 Verb Tenses Reference</span>
        </button>
      </div>

      {#if cheatsheetTab === 'mindsets'}
        <!-- 💡 5 Intent-Based Question Mindsets Grid -->
        <div class="space-y-6 animate-fade-in">
          <!-- Mindset Intro Banner -->
          <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2 text-xs text-slate-300">
            <div class="flex items-center gap-2 text-amber-400 font-bold text-sm">
              <Zap class="w-4 h-4" />
              <span>Core Mindset Shift: Focus on Communication Intent</span>
            </div>
            <p class="leading-relaxed">
              Instead of translating word-by-word, identify your <strong>core question intent</strong> (Feasibility, Estimation, Opinion, Status, or Clarification), immediately trigger the <strong>opening chunk (0.5s Trigger Hook)</strong>, and attach the target action.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            {#each QUESTION_MINDSETS as mindset}
              <div class={`rounded-2xl p-5 border ${mindset.color} space-y-4 backdrop-blur-md shadow-xl flex flex-col justify-between`}>
                <div class="space-y-3">
                  <!-- Header -->
                  <div class="flex items-start justify-between gap-2">
                    <div class="flex items-center gap-2">
                      <span class="text-2xl">{mindset.icon}</span>
                      <h3 class={`text-sm font-bold ${mindset.headerColor}`}>{mindset.category}</h3>
                    </div>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-900/90 text-slate-300 border border-slate-700/80 shrink-0">
                      {mindset.badge}
                    </span>
                  </div>

                  <p class="text-xs text-slate-400 leading-relaxed">{mindset.description}</p>

                  <!-- Triggers / Formulas -->
                  <div class="space-y-2 pt-1">
                    {#each mindset.triggers as trig}
                      <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-1 text-xs">
                        <div class="font-mono font-bold text-amber-300">
                          {trig.formula}
                        </div>
                        <div class="text-slate-400 italic text-[11px]">
                          👉 {trig.use}
                        </div>
                        <div class="pt-1 flex items-center justify-between text-slate-200">
                          <span class="font-medium text-emerald-300">"{trig.eg}"</span>
                        </div>
                        <div class="text-[11px] text-slate-400">
                          ({trig.vi})
                        </div>
                      </div>
                    {/each}
                  </div>
                </div>

                <!-- Mindset Trap Warning -->
                <div class="p-2.5 rounded-xl bg-slate-950/90 border border-slate-800 text-[11px] text-amber-200/90 font-medium">
                  {mindset.mindsetTrap}
                </div>
              </div>
            {/each}
          </div>
        </div>

      {:else}
        <!-- ⏱️ 12 Tenses & Question Rules Cheat Sheet View -->
        <div class="space-y-6 animate-fade-in">
          {#each CHEATSHEET_TENSES as section}
            <div class={`rounded-2xl p-5 border ${section.color} space-y-4 backdrop-blur-md`}>
              <h2 class="text-sm font-bold text-slate-100 flex items-center gap-2">
                <Clock class="w-4 h-4 text-blue-400" />
                <span>{section.group}</span>
              </h2>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {#each section.items as item}
                  <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2.5 shadow-lg">
                    <h3 class="text-xs font-bold text-blue-300">{item.name}</h3>

                    <div class="space-y-1 text-xs">
                      <div>
                        <span class="text-slate-400 font-semibold">Formula: </span>
                        <span class="font-mono text-slate-200">{item.formula}</span>
                      </div>
                      <div>
                        <span class="text-amber-400 font-semibold">Question Pattern: </span>
                        <span class="font-mono text-amber-200">{item.quasm}</span>
                      </div>
                      <div>
                        <span class="text-slate-400 font-semibold">Signal Words: </span>
                        <span class="text-slate-300 italic">{item.signals}</span>
                      </div>
                      <div>
                        <span class="text-slate-400 font-semibold">Core Usage: </span>
                        <span class="text-slate-300">{item.use}</span>
                      </div>
                    </div>

                    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
                      <span class="text-slate-400 font-semibold">Example: </span>
                      <span class="text-emerald-300 font-medium font-mono">"{item.example}"</span>
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
