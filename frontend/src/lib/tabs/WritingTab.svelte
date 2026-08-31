<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { GetWritingPrompt, EvaluateWriting, SaveWritingToObsidian, GetConfig } from '../../../wailsjs/go/main/App.js';
  import { 
    Sparkles, 
    RefreshCw, 
    Bookmark, 
    Check, 
    Play, 
    Pause, 
    RotateCcw, 
    PenTool, 
    Lightbulb, 
    Lock, 
    KeyRound, 
    ArrowRight, 
    Copy, 
    CheckCircle2, 
    AlertCircle, 
    FileText, 
    LayoutGrid, 
    BookOpen, 
    Award,
    Briefcase,
    MessageSquare
  } from 'lucide-svelte';
  import { parseAiFeedback } from '../utils/writingFeedbackParser';

  let { onNavigateTab } = $props<{ onNavigateTab?: (tab: string) => void }>();

  let currentLevel = $state('scenario');
  let promptItem = $state<any>(null);
  let userText = $state('');
  let loadingPrompt = $state(false);
  let evaluating = $state(false);
  let aiEvaluation = $state('');
  let savedToObsidian = $state(false);
  let config = $state<any>(null);
  let showRawMarkdown = $state(false);
  let copiedIndex = $state<number | null>(null);

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

  let hasAiToken = $derived(() => {
    if (!config) return true;
    if (config.ai_provider === 'agy' || config.ai_provider === 'opencode' || config.ai_provider === 'ollama') return true;
    if (config.ai_provider === 'openrouter') return !!(config.openrouter_api_key && config.openrouter_api_key.trim().length > 5);
    if (config.ai_provider === 'groq') return !!(config.groq_api_key && config.groq_api_key.trim().length > 5);
    return true;
  });

  let parsedFeedback = $derived(
    aiEvaluation ? parseAiFeedback(aiEvaluation) : null
  );

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
      config = await GetConfig();
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
      aiEvaluation = `AI evaluation error: ${e}`;
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

  function applyAlternative(text: string) {
    userText = text;
  }

  async function copyText(text: string, index: number) {
    try {
      await navigator.clipboard.writeText(text);
      copiedIndex = index;
      setTimeout(() => {
        if (copiedIndex === index) copiedIndex = null;
      }, 2000);
    } catch (e) {
      console.error(e);
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
        Micro-Scenario (2-3 sentences)
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

    <!-- Reload Random Prompt -->
    <button
      onclick={() => loadPrompt(currentLevel)}
      disabled={loadingPrompt}
      class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs flex items-center gap-1.5 transition cursor-pointer active:scale-95"
      title="Load another random topic"
    >
      <RefreshCw class={`w-4 h-4 ${loadingPrompt ? 'animate-spin' : ''}`} />
      <span class="hidden sm:inline">New Topic</span>
    </button>
  </div>

  {#if promptItem}
    <div class="relative">
      <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 backdrop-blur-xl shadow-2xl space-y-6">
        <!-- Topic Header & Stopwatch Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
          <div class="flex items-start gap-3">
            <span class="text-3xl p-2.5 rounded-2xl bg-slate-800/80 border border-slate-700 shadow-inner">
              {promptItem.category_icon || '✍️'}
            </span>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">
                  {promptItem.category || 'Workplace'}
                </span>
                <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300">
                  {promptItem.level}
                </span>
              </div>
              <h3 class="text-xl font-black text-slate-100 mt-0.5 tracking-tight">
                {promptItem.title}
              </h3>
            </div>
          </div>

          <!-- Stopwatch Widget -->
          <div class="flex items-center gap-2 bg-slate-950 p-2 rounded-2xl border border-slate-800 self-start sm:self-auto">
            <span class="font-mono text-base font-bold text-slate-200 px-2 tracking-wider">
              {formattedTime()}
            </span>
            {#if !timerRunning}
              <button
                onclick={startTimer}
                class="p-1.5 rounded-xl bg-blue-600/20 text-blue-400 hover:bg-blue-600/30 transition cursor-pointer"
                title="Start Stopwatch"
              >
                <Play class="w-4 h-4" />
              </button>
            {:else}
              <button
                onclick={pauseTimer}
                class="p-1.5 rounded-xl bg-amber-600/20 text-amber-400 hover:bg-amber-600/30 transition cursor-pointer"
                title="Pause Stopwatch"
              >
                <Pause class="w-4 h-4" />
              </button>
            {/if}
            <button
              onclick={resetTimer}
              class="p-1.5 rounded-xl bg-slate-800 text-slate-400 hover:bg-slate-700 transition cursor-pointer"
              title="Reset Stopwatch"
            >
              <RotateCcw class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Scenario Context & Prompt -->
        <div class="space-y-4">
          <div class="p-4 rounded-2xl bg-gradient-to-r from-blue-950/30 to-indigo-950/30 border border-blue-500/20 space-y-1.5">
            <span class="text-[11px] font-bold text-blue-400 uppercase tracking-wider flex items-center gap-1.5">
              <Lightbulb class="w-3.5 h-3.5" />
              <span>Scenario Context (Ngữ cảnh thực tế)</span>
            </span>
            <p class="text-sm text-slate-200 font-medium leading-relaxed">
              {promptItem.situation_vi}
            </p>
          </div>

          <div class="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <PenTool class="w-3.5 h-3.5 text-indigo-400" />
              <span>Prompt Requirement (Yêu cầu bài viết)</span>
            </span>
            <p class="text-base text-slate-100 font-semibold leading-relaxed">
              "{promptItem.prompt}"
            </p>
          </div>
        </div>

        <!-- Quick Starter Chips & Suggested Vocab -->
        {#if (promptItem.sentence_starters && promptItem.sentence_starters.length > 0) || (promptItem.suggested_vocab && promptItem.suggested_vocab.length > 0)}
          <div class="grid sm:grid-cols-2 gap-3 pt-1">
            {#if promptItem.sentence_starters && promptItem.sentence_starters.length > 0}
              <div class="space-y-2">
                <span class="text-[11px] font-bold text-slate-400 block">💡 Quick Sentence Starters (Bấm để chèn):</span>
                <div class="flex flex-wrap gap-1.5">
                  {#each promptItem.sentence_starters as starter}
                    <button
                      onclick={() => insertStarter(starter)}
                      class="text-left text-xs bg-slate-800/80 hover:bg-blue-600/20 hover:text-blue-300 hover:border-blue-500/30 border border-slate-700/80 px-3 py-1.5 rounded-xl text-slate-300 transition cursor-pointer"
                    >
                      + "{starter}"
                    </button>
                  {/each}
                </div>
              </div>
            {/if}

            {#if promptItem.suggested_vocab && promptItem.suggested_vocab.length > 0}
              <div class="space-y-2">
                <span class="text-[11px] font-bold text-slate-400 block">⚡ High-Yield Vocabulary (Từ vựng gợi ý):</span>
                <div class="flex flex-wrap gap-1.5">
                  {#each promptItem.suggested_vocab as vocab}
                    <span class="text-xs bg-indigo-950/40 text-indigo-300 border border-indigo-500/30 px-2.5 py-1 rounded-xl font-mono">
                      {vocab}
                    </span>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
        {/if}

        <!-- Textarea Editor Area -->
        <div class="space-y-3 pt-2">
          <textarea
            bind:value={userText}
            onfocus={() => { if (!timerRunning && timerSeconds === 0) startTimer(); }}
            placeholder="Start writing your response here..."
            rows="6"
            class="w-full bg-slate-950 border border-slate-700/80 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-2xl p-4 text-base text-slate-100 placeholder-slate-500 outline-none transition leading-relaxed"
          ></textarea>

          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <!-- Word Counter & Range Bar -->
            <div class="flex items-center gap-3">
              <span class="text-xs font-mono text-slate-400">
                Word Count: <strong class="text-slate-100">{wordCount}</strong>
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
                title="Save essay and feedback to Obsidian Vault"
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

        <!-- AI Evaluation Result (Visual Dashboard) -->
        {#if aiEvaluation}
          <div class="pt-4 border-t border-slate-800 space-y-4 animate-fade-in">
            <!-- Header & Toggle View -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="p-1.5 rounded-lg bg-blue-500/20 text-blue-400 border border-blue-500/30">
                  <Sparkles class="w-4 h-4" />
                </span>
                <h4 class="text-base font-bold text-slate-100">AI Coach Evaluation & Analysis</h4>
              </div>

              <!-- Switch between Visual Cards and Raw Text -->
              <button
                onclick={() => showRawMarkdown = !showRawMarkdown}
                class="px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-medium flex items-center gap-1.5 transition cursor-pointer border border-slate-700/60"
              >
                {#if showRawMarkdown}
                  <LayoutGrid class="w-3.5 h-3.5 text-blue-400" />
                  <span>Visual Cards View</span>
                {:else}
                  <FileText class="w-3.5 h-3.5 text-slate-400" />
                  <span>Raw Text View</span>
                {/if}
              </button>
            </div>

            {#if showRawMarkdown}
              <!-- Raw Text / Markdown Mode -->
              <div class="text-slate-300 leading-relaxed whitespace-pre-wrap font-sans text-xs bg-slate-950/80 p-5 rounded-2xl border border-slate-800">
                {aiEvaluation}
              </div>
            {:else if parsedFeedback}
              <!-- Structured Visual Cards Dashboard -->
              <div class="space-y-4">
                <!-- 1. Score & Overall Impression Hero Banner -->
                <div class="p-5 rounded-2xl bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-xl">
                  <div class="flex items-center gap-4">
                    <!-- Circular / Pill Score Badge -->
                    <div class={`px-4 py-3 rounded-2xl border flex flex-col items-center justify-center shrink-0 ${
                      parsedFeedback.score >= 8.0
                        ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40 shadow-lg shadow-emerald-500/10'
                        : parsedFeedback.score >= 6.5
                        ? 'bg-blue-500/20 text-blue-400 border-blue-500/40 shadow-lg shadow-blue-500/10'
                        : 'bg-amber-500/20 text-amber-400 border-amber-500/40 shadow-lg shadow-amber-500/10'
                    }`}>
                      <span class="text-2xl font-black tracking-tight">{parsedFeedback.score}</span>
                      <span class="text-[10px] font-bold uppercase tracking-wider opacity-80">/ 10</span>
                    </div>

                    <div class="space-y-1">
                      <div class="flex items-center gap-2">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Overall Assessment:</span>
                        <span class={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          parsedFeedback.score >= 8.0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-blue-500/20 text-blue-400'
                        }`}>
                          {parsedFeedback.scoreLabel}
                        </span>
                      </div>
                      <p class="text-sm text-slate-200 font-medium leading-relaxed">
                        {parsedFeedback.overallFeedback}
                      </p>
                    </div>
                  </div>

                  {#if parsedFeedback.promptAlignment}
                    <div class="px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700/80 text-[11px] text-slate-300 shrink-0 self-start sm:self-center">
                      <span class="font-bold text-indigo-300 block">🎯 Prompt Adherence:</span>
                      <span>{parsedFeedback.promptAlignment}</span>
                    </div>
                  {/if}
                </div>

                <!-- 2. Grammar & Spelling Fixes (Before ➔ After Cards) -->
                <div class="space-y-2.5">
                  <div class="flex items-center justify-between text-xs font-bold text-slate-300">
                    <span class="flex items-center gap-1.5 text-rose-400">
                      <AlertCircle class="w-4 h-4" />
                      <span>Grammar & Spelling Corrections ({parsedFeedback.corrections.length})</span>
                    </span>
                    <span class="text-[11px] text-slate-500 font-normal">Spot errors & polished native forms</span>
                  </div>

                  {#if parsedFeedback.corrections.length === 0}
                    <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                      <CheckCircle2 class="w-4 h-4 text-emerald-400 shrink-0" />
                      <span>Tuyệt vời! Không phát hiện lỗi sai ngữ pháp hoặc chính tả đáng kể nào trong đoạn văn của bạn.</span>
                    </div>
                  {:else}
                    <div class="grid gap-2.5">
                      {#each parsedFeedback.corrections as item}
                        <div class="p-3.5 rounded-xl bg-slate-950/90 border border-slate-800/90 space-y-2">
                          <div class="flex flex-col sm:flex-row sm:items-center gap-2 text-xs">
                            <!-- Original (Mistake) -->
                            <div class="flex items-center gap-1.5 flex-1 bg-rose-950/30 text-rose-300 px-3 py-1.5 rounded-lg border border-rose-500/30 font-medium">
                              <span class="text-rose-400 font-bold">❌ Original:</span>
                              <span class="line-through decoration-rose-400/70">{item.original}</span>
                            </div>

                            <ArrowRight class="w-3.5 h-3.5 text-slate-500 shrink-0 hidden sm:block" />

                            <!-- Correction -->
                            <div class="flex items-center gap-1.5 flex-1 bg-emerald-950/30 text-emerald-300 px-3 py-1.5 rounded-lg border border-emerald-500/30 font-semibold">
                              <span class="text-emerald-400 font-bold">✅ Fix:</span>
                              <span>{item.correction}</span>
                            </div>
                          </div>

                          {#if item.reason}
                            <div class="text-[11px] text-slate-400 pl-1 flex items-start gap-1">
                              <span class="text-slate-500">💡</span>
                              <span>{item.reason}</span>
                            </div>
                          {/if}
                        </div>
                      {/each}
                    </div>
                  {/if}
                </div>

                <!-- 3. Natural Phrasing & Alternatives (Professional vs Casual) -->
                {#if parsedFeedback.alternatives.length > 0}
                  <div class="space-y-2.5 pt-1">
                    <div class="flex items-center justify-between text-xs font-bold text-slate-300">
                      <span class="flex items-center gap-1.5 text-indigo-400">
                        <Sparkles class="w-4 h-4" />
                        <span>Native Phrasing Alternatives (Cách diễn đạt tự nhiên chuẩn bản xứ)</span>
                      </span>
                    </div>

                    <div class="grid gap-3">
                      {#each parsedFeedback.alternatives as alt, idx}
                        <div class="p-4 rounded-2xl bg-gradient-to-br from-indigo-950/20 via-slate-950 to-slate-900 border border-indigo-500/20 space-y-2.5">
                          <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-indigo-300 flex items-center gap-1.5 bg-indigo-500/10 px-2.5 py-1 rounded-lg border border-indigo-500/20">
                              {#if alt.style.toLowerCase().includes('prof')}
                                <Briefcase class="w-3.5 h-3.5 text-indigo-400" />
                              {:else}
                                <MessageSquare class="w-3.5 h-3.5 text-cyan-400" />
                              {/if}
                              <span>{alt.style}</span>
                            </span>

                            <div class="flex items-center gap-1.5">
                              <button
                                onclick={() => copyText(alt.text, idx)}
                                class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-medium flex items-center gap-1 transition cursor-pointer border border-slate-700"
                                title="Copy sentence"
                              >
                                {#if copiedIndex === idx}
                                  <Check class="w-3 h-3 text-emerald-400" />
                                  <span class="text-emerald-400">Copied</span>
                                {:else}
                                  <Copy class="w-3 h-3" />
                                  <span>Copy</span>
                                {/if}
                              </button>

                              <button
                                onclick={() => applyAlternative(alt.text)}
                                class="px-2.5 py-1 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 text-[11px] font-semibold flex items-center gap-1 transition cursor-pointer"
                                title="Replace your editor text with this alternative"
                              >
                                <span>Use in Editor</span>
                              </button>
                            </div>
                          </div>

                          <p class="text-sm font-medium text-slate-100 leading-relaxed font-sans pl-1">
                            "{alt.text}"
                          </p>
                        </div>
                      {/each}
                    </div>
                  </div>
                {/if}

                <!-- 4. Key Vocabulary Highlights -->
                {#if parsedFeedback.vocabularyHighlights.length > 0}
                  <div class="space-y-2 pt-1">
                    <span class="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                      <BookOpen class="w-4 h-4 text-cyan-400" />
                      <span>Vocabulary & Collocation Highlights:</span>
                    </span>

                    <div class="grid sm:grid-cols-2 gap-2">
                      {#each parsedFeedback.vocabularyHighlights as v}
                        <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 flex items-start gap-2 text-xs">
                          <span class="font-bold text-cyan-300 font-mono shrink-0 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-500/30">
                            {v.term}
                          </span>
                          <span class="text-slate-300 text-[11px] leading-relaxed mt-0.5">
                            {v.meaning}
                          </span>
                        </div>
                      {/each}
                    </div>
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        {/if}
      </div>

      <!-- Blurred Glass Lock Overlay when Token is Missing -->
      {#if !hasAiToken()}
        <div class="absolute inset-0 rounded-2xl bg-slate-950/70 backdrop-blur-md border border-slate-700/80 flex flex-col items-center justify-center p-8 text-center space-y-4 shadow-2xl z-20">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-violet-500/20 to-cyan-500/20 border border-violet-500/40 flex items-center justify-center text-violet-400 shadow-lg shadow-violet-500/10">
            <Lock class="w-7 h-7" />
          </div>

          <div class="max-w-md space-y-1.5">
            <h4 class="text-lg font-bold text-slate-100">AI Configuration Required</h4>
            <p class="text-xs text-slate-400 leading-relaxed">
              Please choose <strong>Antigravity (agy)</strong> or <strong>OpenCode</strong> for zero-config evaluation, or configure <strong>OpenRouter / Groq / Ollama</strong> in Settings.
            </p>
          </div>

          <div class="flex items-center gap-3 pt-2">
            {#if onNavigateTab}
              <button
                onclick={() => onNavigateTab('settings')}
                class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-cyan-600 hover:from-violet-500 hover:to-cyan-500 text-white text-xs font-bold flex items-center gap-2 transition shadow-lg shadow-violet-500/25 cursor-pointer active:scale-95"
              >
                <KeyRound class="w-4 h-4" />
                <span>Go to Settings</span>
                <ArrowRight class="w-3.5 h-3.5" />
              </button>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>
