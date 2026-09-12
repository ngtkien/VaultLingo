<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Flame,
    BookOpen,
    Headphones,
    Sparkles,
    ArrowRight,
    FileText,
    ChevronRight,
    CheckCircle2,
    Circle
  } from 'lucide-svelte';
  import { GetSavedObsidianVocab } from '../../../wailsjs/go/main/App.js';
  import { getStreak, getTodayProgress, markToday } from '../utils/daily';

  let {
    dueCount = 0,
    savedCount = 0,
    dayStreak = 0,
    idiom = null,
    onNavigate,
    onOpenWord
  } = $props<{
    dueCount?: number;
    savedCount?: number;
    dayStreak?: number;
    idiom?: any;
    onNavigate: (area: string, view?: string) => void;
    onOpenWord?: (word: string) => void;
  }>();

  let recent = $state<any[]>([]);
  let streak = $state(dayStreak);
  let progress = $state({ done: 0, total: 3, pct: 0, rec: { visited: false, review: false, dictation: false, listening: false } });

  const fallbackQuote = {
    word: 'architecture',
    pos: 'noun',
    phonetic: '/ˈɑːr.kə.tek.tʃɚ/',
    definition: 'The structure, design, or intentional framework of a complex system.',
    quoteText: 'Language is the architecture of thought.',
    author: 'Joseph Joubert'
  };

  function refreshLocal() {
    streak = getStreak();
    progress = getTodayProgress();
  }

  $effect(() => {
    if (dayStreak > streak) streak = dayStreak;
  });

  onMount(async () => {
    markToday();
    refreshLocal();
    try {
      const items = await GetSavedObsidianVocab();
      recent = (items || []).slice(-2).reverse();
    } catch {
      recent = [];
    }
  });
</script>

<div class="w-full max-w-6xl mx-auto space-y-6 pb-12">
  <!-- Top Editorial Hero: Daily Practice & Plan -->
  <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] relative overflow-hidden border border-[var(--border-main)]">
    <div class="max-w-3xl space-y-3">
      <div class="flex items-center gap-2 flex-wrap">
        <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-1 rounded-md">
          Your Daily Practice
        </span>
        {#if streak > 0}
          <span class="text-xs font-mono font-bold text-amber-700 bg-amber-500/15 border border-amber-500/30 px-2 py-0.5 rounded-full">
            🔥 {streak}-day streak
          </span>
        {:else}
          <span class="text-xs text-[var(--text-muted)] font-serif italic">
            Open app daily to build a streak
          </span>
        {/if}
        <span class="text-xs text-[var(--text-muted)] font-mono">
          {progress.done}/{progress.total} done today
        </span>
      </div>

      <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)]">
        Make progress in 20 minutes.
      </h1>

      <p class="text-sm sm:text-base text-[var(--text-muted)] leading-relaxed font-sans">
        Review what is due, learn a few useful words, then practise with one focused lesson.
      </p>
    </div>

    <!-- Today's Plan Grid -->
    <div class="mt-6 pt-6 border-t border-[var(--border-main)]">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-base font-semibold text-[var(--text-main)]">Today's Plan</h2>
          <p class="text-xs text-[var(--text-muted)]">Tick off 3 small wins. Streak grows when you show up.</p>
        </div>
      </div>

      <div class="grid sm:grid-cols-3 gap-4">
        <!-- Card 1: Review due words -->
        <button
          onclick={() => onNavigate('learn', 'vocab')}
          class="p-4 rounded-xl text-left bg-[var(--bg-inner)] border border-[var(--border-main)] hover:border-[var(--accent-primary)] transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div class="flex items-center justify-between w-full">
            <span class="px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              4 min
            </span>
            <span class="flex items-center gap-1.5">
              {#if progress.rec.review}
                <CheckCircle2 class="w-4 h-4 text-emerald-600" />
              {:else}
                <Circle class="w-4 h-4 text-[var(--text-subtle)]" />
              {/if}
              <BookOpen class="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] transition" />
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-sm font-bold text-[var(--text-main)] group-hover:text-[var(--accent-primary)] transition">
              Review due words
            </h3>
            <p class="text-xs text-[var(--text-muted)] mt-0.5">
              {dueCount} word{dueCount === 1 ? '' : 's'} due · {savedCount} saved in vault
            </p>
          </div>
        </button>

        <!-- Card 2: Practice dictation -->
        <button
          onclick={() => onNavigate('practice', 'dictation')}
          class="p-4 rounded-xl text-left bg-[var(--bg-inner)] border border-[var(--border-main)] hover:border-[var(--accent-primary)] transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div class="flex items-center justify-between w-full">
            <span class="px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              6 min
            </span>
            <span class="flex items-center gap-1.5">
              {#if progress.rec.dictation}
                <CheckCircle2 class="w-4 h-4 text-emerald-600" />
              {:else}
                <Circle class="w-4 h-4 text-[var(--text-subtle)]" />
              {/if}
              <Headphones class="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] transition" />
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-sm font-bold text-[var(--text-main)] group-hover:text-[var(--accent-primary)] transition">
              Practice dictation
            </h3>
            <p class="text-xs text-[var(--text-muted)] mt-0.5">
              1 focused audio session
            </p>
          </div>
        </button>

        <!-- Card 3: Listen and repeat -->
        <button
          onclick={() => onNavigate('practice', 'listening')}
          class="p-4 rounded-xl text-left bg-[var(--bg-inner)] border border-[var(--border-main)] hover:border-[var(--accent-primary)] transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div class="flex items-center justify-between w-full">
            <span class="px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              8 min
            </span>
            <span class="flex items-center gap-1.5">
              {#if progress.rec.listening}
                <CheckCircle2 class="w-4 h-4 text-emerald-600" />
              {:else}
                <Circle class="w-4 h-4 text-[var(--text-subtle)]" />
              {/if}
              <Sparkles class="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] transition" />
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-sm font-bold text-[var(--text-main)] group-hover:text-[var(--accent-primary)] transition">
              Listen and repeat
            </h3>
            <p class="text-xs text-[var(--text-muted)] mt-0.5">
              Short dialogue, exact transcript
            </p>
          </div>
        </button>
      </div>
    </div>
  </section>

  <!-- Middle Grid: Real status -->
  <div class="grid lg:grid-cols-3 gap-6">
    <div class="lg:col-span-2 space-y-6">
      <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)]">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-semibold text-[var(--text-main)]">Your Progress</h2>
          <span class="text-xs text-[var(--text-muted)] font-mono">Stored locally · honest counts</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Day streak</span>
              <Flame class="w-4 h-4 text-amber-500" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {streak}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              Consecutive visiting days
            </p>
          </div>

          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Due now</span>
              <BookOpen class="w-4 h-4 text-[var(--accent-primary)]" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {dueCount}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              SRS words waiting
            </p>
          </div>

          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Vault</span>
              <FileText class="w-4 h-4 text-emerald-600" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {savedCount}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              Notes in Obsidian
            </p>
          </div>
        </div>

        <div class="mt-3">
          <div class="flex items-center justify-between text-xs mb-1.5">
            <span class="text-[var(--text-muted)]">Today: {progress.done}/{progress.total} habits</span>
            <span class="font-mono font-bold text-[var(--accent-primary)]">{progress.pct}%</span>
          </div>
          <div class="w-full h-2 rounded-full bg-[var(--border-main)] overflow-hidden">
            <div class="h-full bg-[var(--accent-primary)] rounded-full transition-all duration-500" style="width: {progress.pct}%"></div>
          </div>
        </div>
      </section>

      <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] bg-gradient-to-r from-[var(--bg-card)] to-[var(--bg-inner)]">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="space-y-1.5">
            <div class="flex items-center gap-2">
              <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2 py-0.5 rounded text-[10px]">
                Focus Session
              </span>
              <span class="text-xs text-[var(--text-muted)]">
                {dueCount > 0 ? `${dueCount} words waiting — clear them first` : 'All clear — go deeper with writing'}
              </span>
            </div>
            <h3 class="text-lg font-bold font-serif text-[var(--text-main)]">
              {dueCount > 0 ? 'Clear your review queue' : 'Workplace Communication & Clarity'}
            </h3>
            <p class="text-xs text-[var(--text-muted)] max-w-md">
              {dueCount > 0
                ? 'Small batch, big memory. 4 minutes is enough to keep the streak.'
                : 'Refine your professional tone and phrasing for real-world engineering syncs.'}
            </p>
          </div>

          <button
            onclick={() => onNavigate(dueCount > 0 ? 'learn' : 'practice', dueCount > 0 ? 'vocab' : 'writing')}
            class="px-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center justify-center gap-1.5 shrink-0 shadow-sm cursor-pointer"
          >
            <span>{dueCount > 0 ? 'Review now' : 'Continue Session'}</span>
            <ArrowRight class="w-3.5 h-3.5" />
          </button>
        </div>
      </section>
    </div>

    <div class="space-y-6">
      <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] h-full flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border-main)]">
            <div>
              <h2 class="text-base font-semibold text-[var(--text-main)]">Review Queue</h2>
              <p class="text-xs text-[var(--text-muted)]">Keep your knowledge fresh.</p>
            </div>
            <span class="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              {dueCount} due
            </span>
          </div>

          <div class="divide-y divide-[var(--border-main)] text-sm">
            <button
              onclick={() => onNavigate('learn', 'vocab')}
              class="w-full py-3 flex items-center justify-between hover:text-[var(--accent-primary)] transition cursor-pointer text-left"
            >
              <div class="flex items-center gap-2.5">
                <BookOpen class="w-4 h-4 text-[var(--accent-primary)]" />
                <span class="font-medium text-[var(--text-main)]">Words</span>
              </div>
              <span class="text-xs text-[var(--text-muted)] flex items-center gap-1 font-mono">
                {dueCount} due <ChevronRight class="w-3.5 h-3.5" />
              </span>
            </button>

            <button
              onclick={() => onNavigate('practice', 'dictation')}
              class="w-full py-3 flex items-center justify-between hover:text-[var(--accent-primary)] transition cursor-pointer text-left"
            >
              <div class="flex items-center gap-2.5">
                <Headphones class="w-4 h-4 text-[var(--accent-primary)]" />
                <span class="font-medium text-[var(--text-main)]">Dictation</span>
              </div>
              <span class="text-xs text-[var(--text-muted)] flex items-center gap-1 font-mono">
                {#if progress.rec.dictation}done{:else}today{/if} <ChevronRight class="w-3.5 h-3.5" />
              </span>
            </button>

            <button
              onclick={() => onNavigate('practice', 'listening')}
              class="w-full py-3 flex items-center justify-between hover:text-[var(--accent-primary)] transition cursor-pointer text-left"
            >
              <div class="flex items-center gap-2.5">
                <Sparkles class="w-4 h-4 text-[var(--accent-primary)]" />
                <span class="font-medium text-[var(--text-main)]">Lessons</span>
              </div>
              <span class="text-xs text-[var(--text-muted)] flex items-center gap-1 font-mono">
                {#if progress.rec.listening}done{:else}today{/if} <ChevronRight class="w-3.5 h-3.5" />
              </span>
            </button>
          </div>
        </div>

        <button
          onclick={() => onNavigate('learn', 'vocab')}
          class="w-full mt-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
        >
          <span>Go to review</span>
          <ArrowRight class="w-3.5 h-3.5" />
        </button>
      </section>
    </div>
  </div>

  <!-- Bottom Row: Recently Saved & Word Journal -->
  <div class="grid md:grid-cols-2 gap-6">
    <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)]">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-base font-semibold text-[var(--text-main)]">Recently Saved</h2>
        <button onclick={() => onNavigate('library')} class="text-xs text-[var(--accent-primary)] hover:underline cursor-pointer">
          View all
        </button>
      </div>

      {#if recent.length === 0}
        <p class="text-xs text-[var(--text-muted)] leading-relaxed">
          No saved words yet. Save from Learn or Dictionary and they will appear here as your daily pull.
        </p>
      {:else}
        <div class="space-y-2.5">
          {#each recent as note}
            <button onclick={() => onOpenWord?.(note.word)} class="w-full p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex items-center justify-between hover:border-[var(--accent-primary)] transition cursor-pointer text-left">
              <div class="flex items-center gap-3">
                <FileText class="w-4 h-4 text-[var(--accent-primary)]" />
                <div>
                  <h3 class="text-xs font-semibold text-[var(--text-main)]">{note.word}</h3>
                  <span class="text-[10px] text-[var(--text-subtle)] font-mono line-clamp-1">{note.definition_en || note.topic_title || ''}</span>
                </div>
              </div>
              <ChevronRight class="w-3.5 h-3.5 text-[var(--text-subtle)]" />
            </button>
          {/each}
        </div>
      {/if}
    </section>

    <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] flex flex-col justify-between">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-base font-semibold text-[var(--text-main)]">Word Journal</h2>
        {#if idiom?.idiom}
          <span class="text-[10px] px-2 py-0.5 rounded-full bg-[var(--bg-inner)] border border-[var(--border-main)] text-[var(--text-muted)]">Daily idiom · real</span>
        {/if}
      </div>

      {#if idiom?.idiom}
        <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-serif font-bold text-base text-[var(--text-main)]">{idiom.idiom}</span>
          </div>
          <p class="text-xs text-[var(--text-muted)]">{idiom.meaning_en}</p>
          {#if idiom.example}
            <blockquote class="pt-2 border-t border-[var(--border-main)] mt-2">
              <p class="font-serif italic text-sm text-[var(--text-main)] leading-snug">“{idiom.example}”</p>
            </blockquote>
          {/if}
        </div>
      {:else}
        <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
          <div class="flex items-center justify-between">
            <div>
              <span class="font-serif font-bold text-base text-[var(--text-main)]">{fallbackQuote.word}</span>
              <span class="text-xs text-[var(--text-muted)] font-mono ml-2">{fallbackQuote.phonetic}</span>
            </div>
            <span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              {fallbackQuote.pos}
            </span>
          </div>
          <p class="text-xs text-[var(--text-muted)]">{fallbackQuote.definition}</p>
          <blockquote class="pt-2 border-t border-[var(--border-main)] mt-2">
            <p class="font-serif italic text-sm text-[var(--text-main)] leading-snug">“{fallbackQuote.quoteText}”</p>
            <cite class="text-[11px] text-[var(--text-subtle)] block mt-1">— {fallbackQuote.author}</cite>
          </blockquote>
        </div>
      {/if}

      <div class="mt-4 pt-3 flex items-center justify-between border-t border-[var(--border-main)]">
        <button
          onclick={() => onOpenWord?.(idiom?.idiom || fallbackQuote.word)}
          class="text-xs font-semibold text-[var(--accent-primary)] hover:underline flex items-center gap-1 cursor-pointer"
        >
          <span>Open journal entry</span>
          <ArrowRight class="w-3 h-3" />
        </button>
        <span class="text-xs font-serif italic text-[var(--text-muted)]">
          Keep learning, keep growing.
        </span>
      </div>
    </section>
  </div>
</div>
