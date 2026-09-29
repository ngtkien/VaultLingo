<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import {
    BookOpen, Timer, CheckCircle2, XCircle, ArrowLeft, Clock
  } from 'lucide-svelte';
  import { GetReadingPassages, GetReadingPassage, CheckReadingAnswers, AddMockScore } from '../../../wailsjs/go/main/App.js';

  interface Meta { id: number; title: string; band_level: number; topic: string; word_count: number; question_count: number }
  interface Item { id: number; question: string; options?: string[]; answer: string; explanation?: string }
  interface QSet { type: string; instruction: string; items: Item[] }
  interface Passage { id: number; title: string; band_level: number; topic: string; word_count: number; text: string; questions: QSet[] }

  let passages = $state<Meta[]>([]);
  let current = $state<Passage | null>(null);
  let answers = $state<Record<number, string>>({});
  let result = $state<any>(null);
  let timed = $state(true);
  let left = $state(20 * 60);
  let timerId: ReturnType<typeof setInterval> | null = null;
  let savingScore = $state(false);

  const TYPE_LABEL: Record<string, string> = {
    tfng: 'True / False / Not Given',
    gapfill: 'Gap fill',
    matching_heading: 'Matching headings',
    mcq: 'Multiple choice',
  };
  const TFNG = ['TRUE', 'FALSE', 'NOT GIVEN'];

  async function open(id: number) {
    current = (await GetReadingPassage(id)) as Passage;
    answers = {};
    result = null;
    left = 20 * 60;
    stopTimer();
    if (timed) startTimer();
  }

  function startTimer() {
    timerId = setInterval(() => {
      left--;
      if (left <= 0) { submit(); }
    }, 1000);
  }
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }

  async function submit() {
    if (!current || result) return;
    stopTimer();
    const payload = Object.entries(answers).map(([id, given]) => ({ item_id: Number(id), given }));
    result = await CheckReadingAnswers(current.id, payload);
  }

  async function logAsMock() {
    if (!result) return;
    savingScore = true;
    try { await AddMockScore('R', result.band_estimate, current?.title ?? ''); } catch {}
    savingScore = false;
  }

  function detailFor(itemId: number) {
    return result?.details?.find((d: any) => d.item_id === itemId);
  }

  function fmtTime(s: number) {
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  }

  function back() { current = null; result = null; stopTimer(); }

  onMount(async () => {
    try { passages = (await GetReadingPassages()) || []; } catch (e) { console.warn(e); }
  });
  onDestroy(stopTimer);
</script>

<div class="w-full max-w-5xl mx-auto space-y-6 pb-12">
  {#if !current}
    <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] border border-[var(--border-main)]">
      <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-1 rounded-md inline-flex items-center gap-1.5">
        <BookOpen class="w-3.5 h-3.5" /> Reading Lab
      </span>
      <h1 class="font-serif text-3xl font-bold tracking-tight text-[var(--text-main)] mt-2.5">
        Read the structure, not the dictionary.
      </h1>
      <p class="text-sm text-[var(--text-muted)] font-sans mt-1">
        IELTS-style passages · timed 20 min · auto-scored to band estimate
      </p>
      <label class="mt-3 flex items-center gap-2 text-xs text-[var(--text-muted)] cursor-pointer w-fit">
        <input type="checkbox" bind:checked={timed} class="accent-[var(--accent-primary)]" />
        Timed mode (20:00 countdown per passage)
      </label>
    </section>

    <section class="grid sm:grid-cols-2 gap-4">
      {#each passages as p}
        <button onclick={() => open(p.id)}
          class="journal-card p-5 border border-[var(--border-main)] text-left hover:border-[var(--accent-primary)] hover:shadow-md transition-all cursor-pointer group">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              band {p.band_level.toFixed(1)}
            </span>
            <span class="text-[10px] font-mono text-[var(--text-subtle)]">{p.question_count} questions</span>
          </div>
          <h3 class="font-serif font-bold text-lg text-[var(--text-main)] mt-2.5 group-hover:text-[var(--accent-primary)] transition">
            {p.title}
          </h3>
          <p class="text-xs text-[var(--text-muted)] mt-1">{p.topic}</p>
        </button>
      {/each}
    </section>
  {:else}
    <!-- Reader -->
    <section class="journal-card border border-[var(--border-main)]">
      <div class="sticky top-16 z-10 flex items-center justify-between gap-3 px-5 py-3 border-b border-[var(--border-main)] bg-[var(--bg-card)]/95 backdrop-blur-sm">
        <button onclick={back} class="flex items-center gap-1.5 text-xs text-[var(--text-muted)] hover:text-[var(--text-main)] cursor-pointer">
          <ArrowLeft class="w-3.5 h-3.5" /> All passages
        </button>
        <div class="flex items-center gap-3">
          <span class="text-[10px] font-mono text-[var(--text-subtle)]">{current.topic} · band {current.band_level.toFixed(1)}</span>
          {#if timed && !result}
            <span class="text-xs font-mono font-bold flex items-center gap-1 {left < 120 ? 'text-rose-600' : 'text-[var(--text-main)]'}">
              <Clock class="w-3.5 h-3.5" /> {fmtTime(left)}
            </span>
          {/if}
          {#if !result}
            <button onclick={submit} class="px-4 py-1.5 rounded-lg btn-forest text-xs font-semibold cursor-pointer">Submit</button>
          {/if}
        </div>
      </div>

      <div class="p-5 sm:p-7 space-y-6">
        <h2 class="font-serif text-2xl sm:text-3xl font-bold text-[var(--text-main)]">{current.title}</h2>
        <div class="font-serif text-[15px] sm:text-base leading-relaxed text-[var(--text-main)] space-y-4 max-w-prose">
          {#each current.text.split('\n\n') as para}
            <p>{para}</p>
          {/each}
        </div>
      </div>
    </section>

    <!-- Questions -->
    <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] space-y-6">
      {#each current.questions as set}
        <div class="space-y-3">
          <div>
            <span class="text-[10px] font-mono font-bold text-[var(--accent-primary)] uppercase tracking-wider">
              {TYPE_LABEL[set.type] ?? set.type}
            </span>
            <p class="text-xs text-[var(--text-muted)] italic mt-1">{set.instruction}</p>
          </div>

          {#each set.items as item}
            {@const d = detailFor(item.id)}
            <div class="rounded-xl border p-3.5 space-y-2
              {d ? (d.correct ? 'border-emerald-500/40 bg-emerald-500/5' : 'border-rose-500/40 bg-rose-500/5') : 'border-[var(--border-main)]'}">
              <p class="text-sm text-[var(--text-main)] flex gap-2">
                <span class="font-mono text-[var(--text-subtle)] shrink-0">{item.id}.</span>
                <span>{item.question}</span>
                {#if d}
                  {#if d.correct}<CheckCircle2 class="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  {:else}<XCircle class="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />{/if}
                {/if}
              </p>

              {#if set.type === 'tfng'}
                <div class="flex gap-1.5 pl-6">
                  {#each TFNG as opt}
                    <button onclick={() => !result && (answers[item.id] = opt)}
                      class="px-2.5 py-1 rounded-lg text-[11px] font-semibold border transition cursor-pointer
                        {answers[item.id] === opt ? 'bg-[var(--accent-primary)] text-white border-[var(--accent-primary)]' : 'border-[var(--border-main)] text-[var(--text-muted)] hover:border-[var(--accent-primary)]'}">
                      {opt}
                    </button>
                  {/each}
                </div>
              {:else if set.type === 'mcq' && item.options}
                <div class="grid gap-1.5 pl-6">
                  {#each item.options as opt, oi}
                    {@const letter = 'ABCD'[oi]}
                    <button onclick={() => !result && (answers[item.id] = letter)}
                      class="text-left px-3 py-1.5 rounded-lg text-xs border transition cursor-pointer
                        {answers[item.id] === letter ? 'bg-[var(--accent-primary)] text-white border-[var(--accent-primary)]' : 'border-[var(--border-main)] text-[var(--text-muted)] hover:border-[var(--accent-primary)]'}">
                      <b>{letter}.</b> {opt}
                    </button>
                  {/each}
                </div>
              {:else}
                <input
                  bind:value={answers[item.id]} disabled={!!result}
                  placeholder="Your answer…"
                  class="ml-6 w-64 max-w-full px-3 py-1.5 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-sm text-[var(--text-main)] focus:border-[var(--accent-primary)] outline-none disabled:opacity-60" />
              {/if}

              {#if d && !d.correct}
                <p class="text-xs pl-6 text-[var(--text-muted)]">
                  Correct answer: <b class="text-emerald-700">{d.expected}</b>
                  {#if d.explanation}<span class="block mt-0.5 italic">{d.explanation}</span>{/if}
                </p>
              {:else if d?.explanation}
                <p class="text-[11px] pl-6 text-[var(--text-subtle)] italic">{d.explanation}</p>
              {/if}
            </div>
          {/each}
        </div>
      {/each}

      {#if !result}
        <button onclick={submit} class="w-full py-3 rounded-xl btn-forest font-semibold text-sm cursor-pointer">
          Submit answers
        </button>
      {/if}
    </section>

    <!-- Result -->
    {#if result}
      <section class="journal-card p-6 border border-[var(--accent-primary)]/40 bg-[var(--accent-primary-light)]/30">
        <div class="flex items-center justify-between gap-4 flex-wrap">
          <div>
            <p class="text-[11px] font-mono font-semibold text-[var(--accent-primary)] uppercase tracking-wider">Result</p>
            <p class="font-serif text-3xl font-bold text-[var(--text-main)] mt-1">
              {result.correct}/{result.total}
              <span class="text-base font-normal text-[var(--text-muted)]">({result.percentage}%)</span>
            </p>
            <p class="text-sm text-[var(--text-muted)] mt-1">
              Estimated band: <b class="text-[var(--accent-primary)] text-lg">{result.band_estimate.toFixed(1)}</b>
            </p>
          </div>
          <button onclick={logAsMock} disabled={savingScore}
            class="px-4 py-2.5 rounded-xl btn-forest text-xs font-semibold cursor-pointer disabled:opacity-50">
            {savingScore ? 'Saving…' : 'Log as mock score'}
          </button>
        </div>
      </section>
    {/if}
  {/if}
</div>
