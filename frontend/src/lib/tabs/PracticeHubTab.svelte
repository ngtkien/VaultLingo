<script lang="ts">
  import {
    Headphones,
    Ear,
    Dumbbell,
    PenTool,
    ArrowRight,
    CheckCircle2
  } from 'lucide-svelte';
  import { getTodayProgress, getStreak } from '../utils/daily';

  let { onSelectPracticeTab, dueCount = 0, savedCount = 0 } = $props<{
    onSelectPracticeTab: (tabId: 'dictation' | 'listening' | 'grammar' | 'writing') => void;
    dueCount?: number;
    savedCount?: number;
  }>();

  const progress = getTodayProgress();
  const streak = getStreak();

  const practiceModules = [
    {
      id: 'dictation' as const,
      title: 'Dictation',
      desc: 'Train your ear and refine your spelling with real-world audio dictation.',
      duration: '10-20 min',
      icon: Headphones,
      cta: 'Start Dictation',
      done: progress.rec.dictation
    },
    {
      id: 'listening' as const,
      title: 'Listening',
      desc: 'Improve comprehension with conversational topics, transcripts, and targeted listening practice.',
      duration: '10-25 min',
      icon: Ear,
      cta: 'Start Listening',
      done: progress.rec.listening
    },
    {
      id: 'grammar' as const,
      title: 'Grammar Gym',
      desc: 'Strengthen grammar and usage through focused exercises and questions.',
      duration: '10-20 min',
      icon: Dumbbell,
      cta: 'Start Grammar Gym',
      done: false
    },
    {
      id: 'writing' as const,
      title: 'Writing Lab',
      desc: 'Build clarity and structure with guided scenarios and AI feedback.',
      duration: '15-30 min',
      icon: PenTool,
      cta: 'Start Writing Lab',
      done: false
    }
  ];
</script>

<div class="w-full max-w-6xl mx-auto space-y-6 pb-12">
  <!-- Hero Banner -->
  <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] border border-[var(--border-main)]">
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
      <div class="max-w-2xl space-y-2.5">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-1 rounded-md">
            Welcome to Practice
          </span>
          {#if streak > 0}
            <span class="text-xs font-mono font-bold text-amber-700 bg-amber-500/15 border border-amber-500/30 px-2 py-0.5 rounded-full">
              🔥 {streak}-day streak
            </span>
          {/if}
        </div>

        <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)]">
          Sharpen your English through intentional practice.
        </h1>

        <p class="text-sm text-[var(--text-muted)] leading-relaxed font-sans">
          {dueCount} word{dueCount === 1 ? '' : 's'} due · {savedCount} saved in vault · {progress.done}/{progress.total} habits done today.
        </p>
      </div>

      <!-- Quick stats overview — real -->
      <div class="p-5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] min-w-[280px] space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">
            Today's Progress
          </span>
          <span class="text-xs font-mono font-bold text-[var(--accent-primary)]">
            {progress.pct}%
          </span>
        </div>

        <div class="w-full h-2 rounded-full bg-[var(--border-main)] overflow-hidden">
          <div
            class="h-full bg-[var(--accent-primary)] rounded-full transition-all duration-500"
            style="width: {progress.pct}%"
          ></div>
        </div>

        <div class="grid grid-cols-2 gap-2 text-xs pt-1">
          <div>
            <span class="text-[var(--text-subtle)] block">Habits</span>
            <span class="font-bold text-[var(--text-main)] font-mono">{progress.done} / {progress.total} done</span>
          </div>
          <div>
            <span class="text-[var(--text-subtle)] block">Streak</span>
            <span class="font-bold text-amber-600 font-mono">{streak} days</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 4 Practice Feature Modules -->
  <section class="space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-base font-semibold text-[var(--text-main)]">Core Practice Labs</h2>
        <p class="text-xs text-[var(--text-muted)]">Select a laboratory to build deep mastery.</p>
      </div>
    </div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {#each practiceModules as mod}
        {@const Icon = mod.icon}
        <div class="journal-card p-5 border border-[var(--border-main)] flex flex-col justify-between hover:border-[var(--accent-primary)] hover:shadow-md transition-all group">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 rounded-xl bg-[var(--accent-primary-light)] text-[var(--accent-primary)] flex items-center justify-center">
                <Icon class="w-5 h-5" />
              </div>
              <span class="flex items-center gap-1.5">
                {#if mod.done}
                  <CheckCircle2 class="w-4 h-4 text-emerald-600" />
                {/if}
                <span class="px-2 py-0.5 rounded text-[10px] font-mono text-[var(--text-subtle)] bg-[var(--bg-inner)] border border-[var(--border-main)]">
                  {mod.duration}
                </span>
              </span>
            </div>

            <div>
              <h3 class="font-serif font-bold text-lg text-[var(--text-main)] group-hover:text-[var(--accent-primary)] transition">
                {mod.title}
              </h3>
              <p class="text-xs text-[var(--text-muted)] mt-1.5 leading-relaxed">
                {mod.desc}
              </p>
            </div>
          </div>

          <button
            onclick={() => onSelectPracticeTab(mod.id)}
            class="mt-5 w-full py-2.5 px-3 rounded-xl border border-[var(--border-main)] hover:border-[var(--accent-primary)] bg-[var(--bg-inner)] hover:bg-[var(--accent-primary)] text-[var(--text-main)] hover:text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer shadow-sm"
          >
            <span>{mod.cta}</span>
            <ArrowRight class="w-3.5 h-3.5" />
          </button>
        </div>
      {/each}
    </div>
  </section>

  <!-- Highlighted Focus Session — honest -->
  <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] bg-[var(--bg-card)]">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div class="space-y-1.5">
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
            {dueCount > 0 ? `${dueCount} due` : 'All clear'}
          </span>
          <span class="text-xs text-[var(--text-muted)] font-serif italic">Recommended next step</span>
        </div>
        <h3 class="text-base font-bold font-serif text-[var(--text-main)]">
          {dueCount > 0 ? 'Clear your due words first — 4 minutes.' : 'Go deeper with Writing Lab today.'}
        </h3>
        <p class="text-xs text-[var(--text-muted)]">
          {dueCount > 0
            ? 'SRS works only when you show up daily. Small batch, big memory.'
            : 'Practice phrasing requests, giving feedback, and structuring technical summaries.'}
        </p>
      </div>

      <button
        onclick={() => onSelectPracticeTab(dueCount > 0 ? 'dictation' : 'writing')}
        class="px-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center justify-center gap-1.5 shrink-0 shadow-sm cursor-pointer"
      >
        <span>{dueCount > 0 ? 'Start Dictation' : 'Continue Focus Session'}</span>
        <ArrowRight class="w-3.5 h-3.5" />
      </button>
    </div>
  </section>

  <!-- Vault Connected Footer Info -->
  <footer class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[var(--text-muted)]">
    <div class="flex items-center gap-2">
      <span>📚 {savedCount} words in vault</span>
      <span class="text-[var(--text-subtle)] font-mono">· Due: {dueCount}</span>
    </div>

    <div class="font-serif italic text-center sm:text-right">
      “Language is the architecture of thought.” — Joseph Joubert
    </div>
  </footer>
</div>
