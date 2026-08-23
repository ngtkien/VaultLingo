<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    GetDailyVocab, 
    GetDailyIdiom, 
    GetQuickQuiz, 
    GetAvailableTopics, 
    SaveWordToObsidian, 
    SaveAllWordsToObsidian, 
    RecordSrsReview 
  } from '../../../wailsjs/go/main/App.js';
  import { playTTS, stopAudio } from '../utils/audio';
  import { Volume2, ExternalLink, Bookmark, Check, RefreshCw, Layers, Sparkles, HelpCircle, CheckCircle2, XCircle } from 'lucide-svelte';

  let words = $state<any[]>([]);
  let topics = $state<any[]>([]);
  let selectedTopic = $state('all');
  let idiom = $state<any>(null);
  let quiz = $state<any>(null);
  let selectedQuizOption = $state('');
  let quizAnswered = $state(false);
  let loading = $state(false);
  let savedWordsMap = $state<Record<string, boolean>>({});
  let activeViewMode = $state<'list' | 'flashcard'>('list');
  let currentCardIndex = $state(0);
  let cardFlipped = $state(false);
  let playingWord = $state('');

  async function loadData() {
    loading = true;
    try {
      topics = await GetAvailableTopics();
      words = await GetDailyVocab(selectedTopic, 5);
      idiom = await GetDailyIdiom();
      quiz = await GetQuickQuiz();
      selectedQuizOption = '';
      quizAnswered = false;
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
    try {
      const res = await SaveWordToObsidian(word);
      if (res.success) {
        savedWordsMap[word.word.toLowerCase()] = true;
      }
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
      // Move to next card in flashcard mode
      if (activeViewMode === 'flashcard' && currentCardIndex < words.length - 1) {
        currentCardIndex++;
        cardFlipped = false;
      }
    } catch (e) {
      console.error(e);
    }
  }

  function playWord(word: string, slow = false) {
    playingWord = word;
    playTTS(word, slow ? 0.75 : 1.0, word).then(() => {
      playingWord = '';
    });
  }

  onMount(() => {
    loadData();
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
        title="Lưu tất cả 5 từ vào Obsidian Vault"
      >
        <Bookmark class="w-3.5 h-3.5" />
        <span>Save All to Obsidian</span>
      </button>

      <!-- Refresh -->
      <button
        onclick={loadData}
        class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer border border-slate-700"
        title="Đổi bộ từ vựng mới"
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
                  <h3 class="text-xl font-bold text-slate-100 tracking-tight">{w.word}</h3>
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
                onclick={() => playWord(w.word, false)}
                class="p-2 rounded-xl bg-slate-800 hover:bg-blue-600 text-slate-300 hover:text-white transition cursor-pointer"
                title="Phát âm (1.0x)"
              >
                <Volume2 class="w-4 h-4" />
              </button>
              <button
                onclick={() => playWord(w.word, true)}
                class="px-2 py-1 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 text-xs font-mono transition cursor-pointer"
                title="Phát âm chậm (0.75x)"
              >
                0.75x
              </button>
              <a
                href={w.dict_link}
                target="_blank"
                class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition"
                title="Mở từ điển Cambridge"
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
                title="Lưu vào Obsidian Vault"
              >
                {#if savedWordsMap[w.word.toLowerCase()]}
                  <Check class="w-4 h-4 text-emerald-400" />
                {:else}
                  <Bookmark class="w-4 h-4" />
                {/if}
              </button>
            </div>
          </div>

          <!-- Definition & Examples -->
          <div class="bg-slate-950/50 p-3.5 rounded-xl border border-slate-800/60 space-y-2">
            <div>
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Định nghĩa:</span>
              <p class="text-sm text-slate-200 mt-0.5">{w.definition_en}</p>
              {#if w.definition_vi}
                <p class="text-xs text-slate-400 mt-0.5 italic">{w.definition_vi}</p>
              {/if}
            </div>
            {#if w.example_en}
              <div class="pt-2 border-t border-slate-800/50">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Ví dụ:</span>
                <p class="text-sm text-slate-300 italic mt-0.5">"{w.example_en}"</p>
                {#if w.example_vi}
                  <p class="text-xs text-slate-500 mt-0.5">{w.example_vi}</p>
                {/if}
              </div>
            {/if}
          </div>

          <!-- SRS Rating Buttons -->
          <div class="flex items-center justify-between pt-1">
            <span class="text-xs text-slate-500">Đánh giá ghi nhớ (SRS):</span>
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
    <!-- Flashcard Mode -->
    {#if words.length > 0}
      {@const curWord = words[currentCardIndex]}
      <div class="max-w-xl mx-auto space-y-4">
        <!-- Progress Bar -->
        <div class="flex items-center justify-between text-xs text-slate-400">
          <span>Card {currentCardIndex + 1} of {words.length}</span>
          <span>{curWord.topic_title}</span>
        </div>

        <!-- 3D Flipping Card -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
          onclick={() => cardFlipped = !cardFlipped}
          class="min-h-[300px] bg-slate-900/90 border border-slate-700/80 rounded-3xl p-8 shadow-2xl backdrop-blur-xl flex flex-col justify-between items-center text-center cursor-pointer transition-all hover:border-blue-500/50"
        >
          {#if !cardFlipped}
            <!-- Front -->
            <div class="my-auto space-y-3">
              <span class="text-4xl font-extrabold text-slate-100 tracking-tight">{curWord.word}</span>
              <div class="flex items-center justify-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30">
                  {curWord.pos}
                </span>
                <span class="text-sm font-mono text-slate-400">{curWord.phonetic}</span>
              </div>
              <p class="text-xs text-slate-500 pt-6">Click card to reveal definition & example 👆</p>
            </div>
          {:else}
            <!-- Back -->
            <div class="my-auto space-y-4">
              <div class="space-y-1">
                <span class="text-xs uppercase text-slate-400 font-bold tracking-wider">Định nghĩa</span>
                <p class="text-base text-slate-100 font-medium">{curWord.definition_en}</p>
                {#if curWord.definition_vi}
                  <p class="text-xs text-slate-400 italic">{curWord.definition_vi}</p>
                {/if}
              </div>
              {#if curWord.example_en}
                <div class="pt-3 border-t border-slate-800">
                  <span class="text-xs uppercase text-slate-400 font-bold tracking-wider">Ví dụ</span>
                  <p class="text-sm text-slate-300 italic">"{curWord.example_en}"</p>
                </div>
              {/if}
            </div>
          {/if}

          <!-- Card Footer Audio Button -->
          <!-- svelte-ignore a11y_click_events_have_key_events -->
          <div class="w-full flex items-center justify-between pt-4 border-t border-slate-800" onclick={(e) => e.stopPropagation()}>
            <button
              onclick={() => playWord(curWord.word)}
              class="p-2 rounded-xl bg-slate-800 hover:bg-blue-600 text-slate-300 hover:text-white transition cursor-pointer"
            >
              <Volume2 class="w-4 h-4" />
            </button>
            <span class="text-xs text-slate-500">Rate your recall:</span>
            <button
              onclick={() => handleSaveWord(curWord)}
              class="p-2 rounded-xl bg-slate-800 hover:bg-emerald-600 text-slate-300 hover:text-white transition cursor-pointer"
            >
              <Bookmark class="w-4 h-4" />
            </button>
          </div>
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
      <div class="bg-gradient-to-br from-slate-900/90 to-indigo-950/40 border border-indigo-900/30 rounded-2xl p-5 space-y-3 shadow-lg">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-lg">💡</span>
            <h4 class="text-xs font-bold uppercase tracking-wider text-indigo-400">Daily Idiom</h4>
          </div>
          <button
            onclick={() => playTTS(idiom.idiom)}
            class="p-1.5 rounded-lg bg-indigo-900/40 hover:bg-indigo-600 text-indigo-200 transition cursor-pointer"
          >
            <Volume2 class="w-3.5 h-3.5" />
          </button>
        </div>

        <div>
          <h5 class="text-lg font-bold text-slate-100">{idiom.idiom}</h5>
          <p class="text-xs font-mono text-slate-400">{idiom.phonetic}</p>
        </div>

        <div class="bg-slate-950/50 p-3 rounded-xl border border-slate-800/60 space-y-1">
          <p class="text-xs text-slate-300"><strong class="text-slate-100">Nghĩa:</strong> {idiom.meaning_en}</p>
          {#if idiom.meaning_vi}
            <p class="text-xs text-indigo-300 italic">{idiom.meaning_vi}</p>
          {/if}
        </div>

        {#if idiom.example}
          <div class="text-xs text-slate-400 italic">
            <span class="font-semibold text-slate-300">Ví dụ:</span> "{idiom.example}"
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
          <HelpCircle class="w-4 h-4 text-purple-400" />
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
                <span class="text-emerald-400">Chính xác!</span>
              {:else}
                <XCircle class="w-4 h-4 text-red-400" />
                <span class="text-red-400">Chưa đúng. Đáp án: {quiz.correct}</span>
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
