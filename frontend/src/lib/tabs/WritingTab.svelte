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
    FileText,
    LayoutGrid
  } from 'lucide-svelte';
  import { parseAiFeedback } from '../utils/writingFeedbackParser';
  import WritingFeedbackCards from '../components/WritingFeedbackCards.svelte';

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

  onMount(() => {
    loadPrompt();
  });

  onDestroy(() => {
    if (timerInterval) clearInterval(timerInterval);
  });
</script>

<div class="w-full max-w-6xl mx-auto space-y-6 pb-12">
  <!-- Header Title -->
  <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-0.5 rounded text-[10px]">
          Composition Studio
        </span>
      </div>
      <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)] mt-1">
        Writing Lab
      </h1>
      <p class="text-sm font-serif italic text-[var(--text-muted)] mt-1">
        Compose professional emails, essays, and scenarios with real-time feedback and AI critique.
      </p>
    </div>

    <!-- Reload Random Prompt -->
    <button
      onclick={() => loadPrompt(currentLevel)}
      disabled={loadingPrompt}
      class="p-2.5 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] text-xs flex items-center gap-1.5 transition cursor-pointer border border-[var(--border-main)] self-start sm:self-auto"
      title="Load another random topic"
    >
      <RefreshCw class={`w-3.5 h-3.5 ${loadingPrompt ? 'animate-spin' : ''}`} />
      <span>New Topic</span>
    </button>
  </div>

  <!-- Level Selector Tabs (matches 8.png) -->
  <div class="flex items-center gap-2 overflow-x-auto pb-1">
    <button
      onclick={() => loadPrompt('scenario')}
      class={`pill-filter ${currentLevel === 'scenario' ? 'active' : ''}`}
    >
      Micro-Scenario (2-3 sentences)
    </button>
    <button
      onclick={() => loadPrompt('short')}
      class={`pill-filter ${currentLevel === 'short' ? 'active' : ''}`}
    >
      Short Essay (50-90w)
    </button>
    <button
      onclick={() => loadPrompt('medium')}
      class={`pill-filter ${currentLevel === 'medium' ? 'active' : ''}`}
    >
      Medium Essay (120-180w)
    </button>
  </div>

  {#if promptItem}
    <div class="relative">
      <article class="journal-card p-6 sm:p-8 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-6">
        <!-- Topic Header & Stopwatch Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[var(--border-main)] pb-5">
          <div class="flex items-start gap-3">
            <span class="text-3xl p-2.5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
              {promptItem.category_icon || '✍️'}
            </span>
            <div>
              <div class="flex items-center gap-2">
                <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2 py-0.5 rounded text-[10px]">
                  {promptItem.category || 'Workplace'}
                </span>
                <span class="text-xs font-mono text-[var(--text-subtle)]">
                  {promptItem.level}
                </span>
              </div>
              <h2 class="font-serif text-xl sm:text-2xl font-bold text-[var(--text-main)] mt-0.5">
                {promptItem.title}
              </h2>
            </div>
          </div>

          <!-- Stopwatch Widget -->
          <div class="flex items-center gap-2 bg-[var(--bg-inner)] p-2 rounded-2xl border border-[var(--border-main)] self-start sm:self-auto">
            <span class="font-mono text-base font-bold text-[var(--text-main)] px-2 tracking-wider">
              {formattedTime()}
            </span>
            {#if !timerRunning}
              <button
                onclick={startTimer}
                class="p-1.5 rounded-xl bg-[var(--accent-primary-light)] text-[var(--accent-primary)] hover:opacity-80 transition cursor-pointer"
                title="Start Stopwatch"
              >
                <Play class="w-4 h-4" />
              </button>
            {:else}
              <button
                onclick={pauseTimer}
                class="p-1.5 rounded-xl bg-amber-500/20 text-amber-700 transition cursor-pointer"
                title="Pause Stopwatch"
              >
                <Pause class="w-4 h-4" />
              </button>
            {/if}
            <button
              onclick={resetTimer}
              class="p-1.5 rounded-xl bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text-main)] transition cursor-pointer border border-[var(--border-main)]"
              title="Reset Stopwatch"
            >
              <RotateCcw class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Scenario Context & Prompt Requirements -->
        <div class="space-y-4">
          <div class="p-4 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1.5">
            <span class="journal-badge text-[var(--accent-primary)] flex items-center gap-1.5">
              <Lightbulb class="w-3.5 h-3.5" />
              <span>Scenario Context</span>
            </span>
            <p class="text-sm font-serif italic text-[var(--text-main)] leading-relaxed">
              {promptItem.situation_vi}
            </p>
          </div>

          <div class="p-4.5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-1.5">
            <span class="journal-badge text-[var(--text-subtle)] flex items-center gap-1.5">
              <PenTool class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              <span>Prompt Requirement</span>
            </span>
            <p class="text-base font-serif font-bold text-[var(--text-main)] leading-relaxed">
              “{promptItem.prompt}”
            </p>
          </div>
        </div>

        <!-- Quick Starter Chips & Suggested Vocab -->
        {#if (promptItem.sentence_starters && promptItem.sentence_starters.length > 0) || (promptItem.suggested_vocab && promptItem.suggested_vocab.length > 0)}
          <div class="grid sm:grid-cols-2 gap-3 pt-1">
            {#if promptItem.sentence_starters && promptItem.sentence_starters.length > 0}
              <div class="space-y-2 p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
                <span class="journal-badge text-[var(--text-subtle)] block">💡 Quick Sentence Starters (Click to insert):</span>
                <div class="flex flex-wrap gap-1.5">
                  {#each promptItem.sentence_starters as starter}
                    <button
                      onclick={() => insertStarter(starter)}
                      class="text-left text-xs bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] px-3 py-1.5 rounded-xl text-[var(--text-main)] transition cursor-pointer"
                    >
                      + “{starter}”
                    </button>
                  {/each}
                </div>
              </div>
            {/if}

            {#if promptItem.suggested_vocab && promptItem.suggested_vocab.length > 0}
              <div class="space-y-2 p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
                <span class="journal-badge text-[var(--text-subtle)] block">⚡ High-Yield Vocabulary:</span>
                <div class="flex flex-wrap gap-1.5">
                  {#each promptItem.suggested_vocab as vocab}
                    <span class="text-xs bg-[var(--bg-card)] text-[var(--accent-primary)] border border-[var(--border-main)] px-2.5 py-1 rounded-xl font-mono">
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
            class="w-full bg-[var(--bg-inner)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-2xl p-4 text-base text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none transition leading-relaxed font-sans"
          ></textarea>

          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <!-- Word Counter & Range Bar -->
            <div class="flex items-center gap-3">
              <span class="text-xs font-mono text-[var(--text-muted)]">
                Word Count: <strong class="text-[var(--text-main)]">{wordCount}</strong>
                {#if promptItem.target_min}
                  / {promptItem.target_min}-{promptItem.target_max} words
                {/if}
              </span>
              {#if promptItem.target_min && wordCount >= promptItem.target_min && wordCount <= promptItem.target_max}
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/15 text-emerald-700 border border-emerald-400/30">
                  Target Reached ✅
                </span>
              {/if}
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2">
              <button
                onclick={handleEvaluate}
                disabled={!userText.trim() || evaluating}
                class="px-5 py-2.5 rounded-xl btn-forest disabled:opacity-50 font-bold text-xs flex items-center gap-1.5 transition shadow-sm cursor-pointer"
              >
                <Sparkles class={`w-4 h-4 ${evaluating ? 'animate-spin' : ''}`} />
                <span>{evaluating ? 'Evaluating with AI...' : 'Submit to AI Coach'}</span>
              </button>

              <button
                onclick={handleSaveToObsidian}
                disabled={!userText.trim()}
                class={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border ${
                  savedToObsidian
                    ? 'bg-emerald-500/15 text-emerald-700 border-emerald-400/30'
                    : 'bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] border-[var(--border-main)]'
                }`}
                title="Save essay and feedback to Obsidian Vault"
              >
                {#if savedToObsidian}
                  <Check class="w-4 h-4 text-emerald-600" />
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
          <div class="pt-4 border-t border-[var(--border-main)] space-y-4">
            <!-- Header & Toggle View -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="p-1.5 rounded-lg bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
                  <Sparkles class="w-4 h-4" />
                </span>
                <h3 class="text-base font-serif font-bold text-[var(--text-main)]">AI Coach Evaluation & Analysis</h3>
              </div>

              <!-- Switch between Visual Cards and Raw Text -->
              <button
                onclick={() => showRawMarkdown = !showRawMarkdown}
                class="px-3 py-1.5 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-main)] text-xs font-medium flex items-center gap-1.5 transition cursor-pointer border border-[var(--border-main)]"
              >
                {#if showRawMarkdown}
                  <LayoutGrid class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Visual Cards</span>
                {:else}
                  <FileText class="w-3.5 h-3.5 text-[var(--text-muted)]" />
                  <span>Raw Text</span>
                {/if}
              </button>
            </div>

            {#if showRawMarkdown}
              <div class="text-[var(--text-main)] leading-relaxed whitespace-pre-wrap font-mono text-xs bg-[var(--bg-inner)] p-5 rounded-2xl border border-[var(--border-main)]">
                {aiEvaluation}
              </div>
            {:else if parsedFeedback}
              <WritingFeedbackCards feedback={parsedFeedback} onApplyAlternative={applyAlternative} />
            {/if}
          </div>
        {/if}
      </article>

      <!-- Glass Lock Overlay if Token is Missing -->
      {#if !hasAiToken()}
        <div class="absolute inset-0 rounded-2xl bg-[var(--bg-card)]/90 backdrop-blur-md border border-[var(--border-main)] flex flex-col items-center justify-center p-8 text-center space-y-4 shadow-xl z-20">
          <div class="w-14 h-14 rounded-2xl bg-[var(--accent-primary-light)] text-[var(--accent-primary)] flex items-center justify-center">
            <Lock class="w-7 h-7" />
          </div>

          <div class="max-w-md space-y-1.5">
            <h3 class="text-lg font-bold font-serif text-[var(--text-main)]">AI Configuration Required</h3>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed">
              Please choose <strong>Antigravity (agy)</strong> or <strong>OpenCode</strong> for zero-config evaluation, or configure <strong>OpenRouter / Groq / Ollama</strong> in Settings.
            </p>
          </div>

          <div class="flex items-center gap-3 pt-2">
            {#if onNavigateTab}
              <button
                onclick={() => onNavigateTab('settings')}
                class="px-5 py-2.5 rounded-xl btn-forest text-xs font-bold flex items-center gap-2 transition shadow-sm cursor-pointer"
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
