<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { GetWritingPrompt, EvaluateWriting, SaveWritingToObsidian } from '../../../wailsjs/go/main/App.js';
  import { Sparkles, RefreshCw, Bookmark, Check, Play, Pause, RotateCcw, PenTool, Lightbulb } from 'lucide-svelte';

  let currentLevel = $state('scenario');
  let promptItem = $state<any>(null);
  let userText = $state('');
  let loadingPrompt = $state(false);
  let evaluating = $state(false);
  let aiEvaluation = $state('');
  let savedToObsidian = $state(false);

  // Stopwatch state
  let timerSeconds = $state(0);
  let timerRunning = $state(false);
  let timerInterval: any = null;

  let wordCount = $derived(
    userText.trim() ? userText.trim().split(/\s+/).length : 0
  );

  let formattedTime = $derived(() => {
    const mins = Math.floor(timerSeconds / 60);
    const secs = timerSeconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  });

  function startTimer() {
    if (timerRunning) return;
    timerRunning = true;
    timerInterval = setInterval(() => {
      timerSeconds++;
    }, 1000);
  }

  function pauseTimer() {
    timerRunning = false;
    if (timerInterval) clearInterval(timerInterval);
  }

  function resetTimer() {
    pauseTimer();
    timerSeconds = 0;
  }

  async function loadPrompt(level = currentLevel) {
    loadingPrompt = true;
    currentLevel = level;
    try {
      promptItem = await GetWritingPrompt(currentLevel);
      userText = '';
      aiEvaluation = '';
      savedToObsidian = false;
      resetTimer();
    } catch (e) {
      console.error(e);
    } finally {
      loadingPrompt = false;
    }
  }

  async function handleEvaluate() {
    if (!promptItem || !userText.trim() || evaluating) return;
    evaluating = true;
    pauseTimer();
    try {
      aiEvaluation = await EvaluateWriting(promptItem.prompt, userText, promptItem.situation_vi);
    } catch (e) {
      aiEvaluation = `Lỗi khi gọi AI: ${e}`;
    } finally {
      evaluating = false;
    }
  }

  async function handleSaveToObsidian() {
    if (!promptItem || !userText.trim()) return;
    try {
      const res = await SaveWritingToObsidian(
        promptItem.title,
        promptItem.situation_vi,
        promptItem.prompt,
        userText,
        aiEvaluation
      );
      if (res.success) {
        savedToObsidian = true;
      }
    } catch (e) {
      console.error(e);
    }
  }

  function insertStarter(text: string) {
    if (!userText.trim()) {
      userText = text + ' ';
    } else {
      userText += ' ' + text;
    }
  }

  onMount(() => {
    loadPrompt();
  });

  onDestroy(() => {
    if (timerInterval) clearInterval(timerInterval);
  });
</script>

<div class="max-w-4xl mx-auto space-y-6">
  <!-- Level Selector Tabs -->
  <div class="flex items-center justify-between bg-slate-900/60 p-2.5 rounded-2xl border border-slate-800 backdrop-blur-md">
    <div class="flex items-center gap-1.5">
      <button
        onclick={() => loadPrompt('scenario')}
        class={`px-4 py-2 rounded-xl text-xs font-bold transition cursor-pointer ${
          currentLevel === 'scenario' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25' : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        Micro-Scenario (2-3 câu)
      </button>
      <button
        onclick={() => loadPrompt('short')}
        class={`px-4 py-2 rounded-xl text-xs font-bold transition cursor-pointer ${
          currentLevel === 'short' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25' : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        Short Essay (50-90w)
      </button>
      <button
        onclick={() => loadPrompt('medium')}
        class={`px-4 py-2 rounded-xl text-xs font-bold transition cursor-pointer ${
          currentLevel === 'medium' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25' : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        Medium Essay (120-180w)
      </button>
    </div>

    <button
      onclick={() => loadPrompt()}
      class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
      title="Đổi đề bài khác"
    >
      <RefreshCw class={`w-4 h-4 ${loadingPrompt ? 'animate-spin' : ''}`} />
    </button>
  </div>

  {#if loadingPrompt}
    <div class="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
      <RefreshCw class="w-8 h-8 animate-spin text-blue-500" />
      <p class="text-sm font-medium">Loading writing scenario...</p>
    </div>
  {:else if promptItem}
    <!-- Prompt & Scenario Details -->
    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-5">
      <div class="flex items-start justify-between gap-4">
        <div class="flex items-center gap-3">
          <span class="text-3xl">{promptItem.category_icon || '✍️'}</span>
          <div>
            <h3 class="text-xl font-bold text-slate-100">{promptItem.title}</h3>
            <span class="text-xs text-slate-400">{promptItem.category}</span>
          </div>
        </div>

        <!-- Stopwatch Display -->
        <div class="flex items-center gap-2 bg-slate-950 px-3.5 py-1.5 rounded-xl border border-slate-800 font-mono text-sm">
          <span class="text-blue-400 font-bold">{formattedTime()}</span>
          {#if !timerRunning}
            <button onclick={startTimer} class="text-slate-400 hover:text-emerald-400 transition cursor-pointer" title="Bắt đầu">
              <Play class="w-3.5 h-3.5" />
            </button>
          {:else}
            <button onclick={pauseTimer} class="text-slate-400 hover:text-amber-400 transition cursor-pointer" title="Tạm dừng">
              <Pause class="w-3.5 h-3.5" />
            </button>
          {/if}
          <button onclick={resetTimer} class="text-slate-400 hover:text-red-400 transition cursor-pointer" title="Đặt lại">
            <RotateCcw class="w-3 h-3" />
          </button>
        </div>
      </div>

      <!-- Situation Box (Vietnamese) -->
      <div class="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 text-sm space-y-1">
        <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Tình huống thực tế:</span>
        <p class="text-slate-200">{promptItem.situation_vi}</p>
      </div>

      <!-- English Prompt -->
      <div class="text-sm font-semibold text-slate-200">
        <strong class="text-blue-400">Đề bài:</strong> {promptItem.prompt}
      </div>

      <!-- Sentence Starters & Suggested Vocab -->
      <div class="grid md:grid-cols-2 gap-3 pt-1">
        {#if promptItem.sentence_starters && promptItem.sentence_starters.length > 0}
          <div class="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
            <div class="flex items-center gap-1.5 text-xs font-bold text-slate-400">
              <Lightbulb class="w-3.5 h-3.5 text-amber-400" />
              <span>Gợi ý mở câu (click để chèn):</span>
            </div>
            <div class="space-y-1.5">
              {#each promptItem.sentence_starters as starter}
                <!-- svelte-ignore a11y_click_events_have_key_events -->
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <div
                  onclick={() => insertStarter(starter)}
                  class="text-xs text-slate-300 hover:text-blue-300 hover:bg-slate-900 p-1.5 rounded-lg transition cursor-pointer italic"
                >
                  "{starter}"
                </div>
              {/each}
            </div>
          </div>
        {/if}

        {#if promptItem.suggested_vocab && promptItem.suggested_vocab.length > 0}
          <div class="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
            <span class="text-xs font-bold text-slate-400">Từ vựng nên dùng:</span>
            <div class="flex flex-wrap gap-1.5">
              {#each promptItem.suggested_vocab as vocab}
                <span class="px-2.5 py-1 rounded-lg text-xs font-medium bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                  {vocab}
                </span>
              {/each}
            </div>
          </div>
        {/if}
      </div>

      <!-- Text Editor Area -->
      <div class="space-y-3 pt-2">
        <textarea
          bind:value={userText}
          onfocus={() => { if (!timerRunning && timerSeconds === 0) startTimer(); }}
          placeholder="Start writing your response here..."
          rows="6"
          class="w-full bg-slate-950 border border-slate-700/80 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-2xl p-4 text-base text-slate-100 placeholder-slate-500 outline-none transition leading-relaxed"
        ></textarea>

        <div class="flex items-center justify-between">
          <!-- Word Counter & Range Bar -->
          <div class="flex items-center gap-3">
            <span class="text-xs font-mono text-slate-400">
              Số từ: <strong class="text-slate-100">{wordCount}</strong>
              {#if promptItem.target_min}
                / {promptItem.target_min}-{promptItem.target_max} words
              {/if}
            </span>
            {#if promptItem.target_min && wordCount >= promptItem.target_min && wordCount <= promptItem.target_max}
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Target Reached ✅
              </span>
            {/if}
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2">
            <button
              onclick={handleEvaluate}
              disabled={!userText.trim() || evaluating}
              class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 disabled:opacity-50 text-white font-bold text-xs flex items-center gap-1.5 transition shadow-lg shadow-blue-500/25 active:scale-95 cursor-pointer"
            >
              <Sparkles class={`w-4 h-4 ${evaluating ? 'animate-spin' : ''}`} />
              <span>{evaluating ? 'Evaluating with AI...' : 'Submit to AI Coach'}</span>
            </button>

            <button
              onclick={handleSaveToObsidian}
              disabled={!userText.trim()}
              class={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer ${
                savedToObsidian
                  ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
              }`}
              title="Lưu bài viết vào Obsidian Vault"
            >
              {#if savedToObsidian}
                <Check class="w-4 h-4 text-emerald-400" />
                <span>Saved to Obsidian</span>
              {:else}
                <Bookmark class="w-4 h-4" />
                <span>Save to Obsidian</span>
              {/if}
            </button>
          </div>
        </div>
      </div>

      <!-- AI Evaluation Result -->
      {#if aiEvaluation}
        <div class="p-5 rounded-2xl bg-slate-950/90 border border-blue-500/30 space-y-3 text-sm animate-fade-in">
          <div class="flex items-center gap-2 text-blue-400 font-bold">
            <Sparkles class="w-4 h-4" />
            <span>Nhận Xét & Đánh Giá Chi Tiết Của AI Coach</span>
          </div>

          <div class="text-slate-300 leading-relaxed whitespace-pre-wrap font-sans text-xs bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            {aiEvaluation}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>
