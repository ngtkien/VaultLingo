<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Map, CheckCircle2, SkipForward, RotateCcw, Flag,
    BookOpen, Mic, Smartphone, ChevronDown, Trophy
  } from 'lucide-svelte';
  import { GetRoadmapProgress, MarkSession, GetMockScores, AddMockScore, DeleteMockScore } from '../../../wailsjs/go/main/App.js';
  import {
    SESSIONS, WEEK_META, PHASES, TOTAL_SESSIONS,
    projectedDates, baseDate, formatDate, type SessionPlan
  } from '../data/roadmap';

  type Status = 'pending' | 'done' | 'missed';

  let progress = $state<Record<number, { status: Status; actual_date?: string }>>({});
  let mockScores = $state<any[]>([]);
  let loading = $state(true);
  let openWeeks = $state<Set<number>>(new Set());
  let mockSkill = $state('R');
  let mockBand = $state(5.0);
  let showMockForm = $state(false);

  let doneIds = $derived(new Set(
    Object.entries(progress).filter(([, p]) => p.status === 'done').map(([id]) => Number(id))
  ));
  let doneCount = $derived(doneIds.size);
  let missedCount = $derived(
    Object.values(progress).filter(p => p.status === 'missed').length
  );
  let projections = $derived(projectedDates(doneIds));

  let nextSession = $derived(SESSIONS.find(s => !doneIds.has(s.id)));
  let endDate = $derived.by(() => {
    const last = SESSIONS[SESSIONS.length - 1];
    return projections.get(last.id) ?? baseDate(last);
  });
  let currentWeek = $derived(nextSession?.week ?? 16);

  function sessionStatus(s: SessionPlan): Status {
    return progress[s.id]?.status ?? 'pending';
  }

  function displayDate(s: SessionPlan): Date {
    return doneIds.has(s.id) ? baseDate(s) : (projections.get(s.id) ?? baseDate(s));
  }

  async function mark(id: number, status: Status) {
    try {
      await MarkSession(id, status === 'pending' ? 'pending' : status, '');
      progress = await GetRoadmapProgress();
    } catch (e) {
      console.warn(e);
    }
  }

  async function saveMock() {
    try {
      await AddMockScore(mockSkill, mockBand, '');
      mockScores = await GetMockScores();
      showMockForm = false;
    } catch (e) {
      console.warn(e);
    }
  }

  async function removeMock(id: number) {
    try {
      await DeleteMockScore(id);
      mockScores = await GetMockScores();
    } catch (e) {
      console.warn(e);
    }
  }

  function toggleWeek(w: number) {
    const next = new Set(openWeeks);
    next.has(w) ? next.delete(w) : next.add(w);
    openWeeks = next;
  }

  const phaseBadge: Record<number, string> = {
    1: 'bg-emerald-500/15 text-emerald-700 border-emerald-500/30',
    2: 'bg-amber-500/15 text-amber-700 border-amber-500/30',
    3: 'bg-rose-500/15 text-rose-700 border-rose-500/30',
  };

  onMount(async () => {
    try {
      const [p, m] = await Promise.all([GetRoadmapProgress(), GetMockScores().catch(() => [])]);
      progress = p || {};
      mockScores = m || [];
      // open current week by default
      const ns = SESSIONS.find(s => progress[s.id]?.status !== 'done');
      openWeeks = new Set([ns?.week ?? 16]);
    } finally {
      loading = false;
    }
  });
</script>

<div class="w-full max-w-4xl mx-auto space-y-6 pb-12">
  <!-- Header -->
  <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] border border-[var(--border-main)]">
    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-5">
      <div class="space-y-2.5">
        <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-1 rounded-md inline-flex items-center gap-1.5">
          <Map class="w-3.5 h-3.5" /> IELTS Roadmap
        </span>
        <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)]">
          4.5 → 6.0 in 16 weeks
        </h1>
        <p class="text-sm text-[var(--text-muted)] font-sans">
          {TOTAL_SESSIONS} sessions · Mon / Wed / Sat / Sun · 60 min each
        </p>
      </div>

      <div class="p-4 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] min-w-[220px] space-y-2.5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">Progress</span>
          <span class="text-xs font-mono font-bold text-[var(--accent-primary)]">{doneCount}/{TOTAL_SESSIONS}</span>
        </div>
        <div class="w-full h-2 rounded-full bg-[var(--border-main)] overflow-hidden">
          <div class="h-full bg-[var(--accent-primary)] rounded-full transition-all duration-500"
               style="width: {(doneCount / TOTAL_SESSIONS) * 100}%"></div>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs pt-1">
          <div>
            <span class="text-[var(--text-subtle)] block">Missed</span>
            <span class="font-bold text-rose-600 font-mono">{missedCount}</span>
          </div>
          <div>
            <span class="text-[var(--text-subtle)] block">Projected finish</span>
            <span class="font-bold text-[var(--text-main)] font-mono">{formatDate(endDate)}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Phase legend -->
    <div class="flex flex-wrap gap-2 mt-5">
      {#each Object.entries(PHASES) as [k, ph]}
        <span class="text-[11px] px-2.5 py-1 rounded-lg border font-medium {phaseBadge[Number(k)]}"
              title={ph.goal}>
          Phase {k} · {ph.name}
        </span>
      {/each}
    </div>
  </section>

  <!-- Next session -->
  {#if nextSession}
    {@const ns = nextSession}
    <section class="journal-card p-5 border border-[var(--accent-primary)]/40 bg-[var(--accent-primary-light)]/30">
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <div>
          <div class="text-[11px] font-mono font-semibold text-[var(--accent-primary)] uppercase tracking-wider">
            Next up · Session {ns.id} · {ns.dayLabel} {formatDate(displayDate(ns))} · Week {ns.week}
          </div>
          <h3 class="font-serif font-bold text-lg text-[var(--text-main)] mt-1">{ns.blockA}</h3>
          <p class="text-xs text-[var(--text-muted)] mt-0.5">Speaking: {ns.blockB}</p>
        </div>
        <button onclick={() => mark(ns.id, 'done')}
          class="px-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center gap-1.5 cursor-pointer">
          <CheckCircle2 class="w-4 h-4" /> Mark done
        </button>
      </div>
    </section>
  {/if}

  <!-- Weeks -->
  {#if loading}
    <p class="text-sm text-[var(--text-muted)] text-center py-10">Loading roadmap…</p>
  {:else}
    {#each WEEK_META as w}
      {@const sessions = SESSIONS.filter(s => s.week === w.week)}
      {@const wDone = sessions.filter(s => sessionStatus(s) === 'done').length}
      {@const isOpen = openWeeks.has(w.week)}
      {@const phase = sessions[0]?.phase ?? 1}
      <section class="journal-card border border-[var(--border-main)] overflow-hidden">
        <button onclick={() => toggleWeek(w.week)}
          class="w-full flex items-center justify-between gap-3 p-4 cursor-pointer hover:bg-[var(--bg-inner)] transition text-left">
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-[10px] px-2 py-0.5 rounded-md border font-semibold {phaseBadge[phase]} shrink-0">
              P{phase}
            </span>
            <div class="min-w-0">
              <span class="text-sm font-semibold text-[var(--text-main)]">Week {w.week}</span>
              <span class="text-xs text-[var(--text-muted)] ml-2">{w.theme}</span>
            </div>
          </div>
          <div class="flex items-center gap-2.5 shrink-0">
            <span class="text-[11px] font-mono text-[var(--text-subtle)]">{wDone}/4</span>
            <ChevronDown class="w-4 h-4 text-[var(--text-muted)] transition-transform {isOpen ? 'rotate-180' : ''}" />
          </div>
        </button>

        {#if isOpen}
          <div class="border-t border-[var(--border-main)] divide-y divide-[var(--border-main)]/50">
            {#each sessions as s}
              {@const st = sessionStatus(s)}
              <div class="p-4 space-y-2.5 {st === 'done' ? 'opacity-60' : ''} {s.milestone ? 'bg-amber-500/5' : ''}">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0">
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="text-[11px] font-mono font-bold text-[var(--text-muted)]">
                        #{s.id} · {s.dayLabel} {formatDate(displayDate(s))}
                      </span>
                      {#if st === 'done'}
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-700 font-semibold">DONE</span>
                      {:else if st === 'missed'}
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/15 text-rose-700 font-semibold">MISSED — rescheduled</span>
                      {/if}
                      {#if s.milestone}
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/15 text-amber-700 font-semibold inline-flex items-center gap-1">
                          <Flag class="w-3 h-3" /> {s.milestone}
                        </span>
                      {/if}
                    </div>
                    {#if s.milestoneGoal}
                      <p class="text-[11px] text-amber-700 mt-1 font-medium">Goal: {s.milestoneGoal}</p>
                    {/if}
                  </div>

                  <div class="flex items-center gap-1 shrink-0">
                    {#if st !== 'done'}
                      <button onclick={() => mark(s.id, 'done')} title="Mark done"
                        class="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-500/15 transition cursor-pointer">
                        <CheckCircle2 class="w-4.5 h-4.5" />
                      </button>
                    {/if}
                    {#if st !== 'missed' && st !== 'done'}
                      <button onclick={() => mark(s.id, 'missed')} title="Mark missed (shifts schedule)"
                        class="p-1.5 rounded-lg text-rose-500 hover:bg-rose-500/15 transition cursor-pointer">
                        <SkipForward class="w-4.5 h-4.5" />
                      </button>
                    {/if}
                    {#if st !== 'pending'}
                      <button onclick={() => mark(s.id, 'pending')} title="Reset to pending"
                        class="p-1.5 rounded-lg text-[var(--text-muted)] hover:bg-[var(--bg-inner)] transition cursor-pointer">
                        <RotateCcw class="w-4 h-4" />
                      </button>
                    {/if}
                  </div>
                </div>

                <div class="grid sm:grid-cols-3 gap-2 text-xs">
                  <div class="flex gap-1.5 items-start">
                    <BookOpen class="w-3.5 h-3.5 mt-0.5 shrink-0 text-[var(--accent-primary)]" />
                    <span class="text-[var(--text-muted)]"><b class="text-[var(--text-main)] font-medium">Read/Grammar:</b> {s.blockA}</span>
                  </div>
                  <div class="flex gap-1.5 items-start">
                    <Mic class="w-3.5 h-3.5 mt-0.5 shrink-0 text-rose-500" />
                    <span class="text-[var(--text-muted)]"><b class="text-[var(--text-main)] font-medium">Speaking:</b> {s.blockB}</span>
                  </div>
                  <div class="flex gap-1.5 items-start">
                    <Smartphone class="w-3.5 h-3.5 mt-0.5 shrink-0 text-[var(--text-subtle)]" />
                    <span class="text-[var(--text-subtle)]">{s.appTask}</span>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </section>
    {/each}
  {/if}

  <!-- Mock scores -->
  <section class="journal-card p-5 border border-[var(--border-main)]">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Trophy class="w-4 h-4 text-amber-600" />
        <h2 class="text-base font-semibold text-[var(--text-main)]">Mock scores</h2>
      </div>
      <button onclick={() => showMockForm = !showMockForm}
        class="text-xs font-semibold px-3 py-1.5 rounded-lg border border-[var(--border-main)] text-[var(--text-main)] hover:border-[var(--accent-primary)] transition cursor-pointer">
        + Add score
      </button>
    </div>

    {#if showMockForm}
      <div class="mt-3 flex items-center gap-2 flex-wrap">
        <select bind:value={mockSkill}
          class="px-3 py-1.5 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-sm text-[var(--text-main)]">
          <option value="L">Listening</option>
          <option value="R">Reading</option>
          <option value="W">Writing</option>
          <option value="S">Speaking</option>
        </select>
        <select bind:value={mockBand}
          class="px-3 py-1.5 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-sm text-[var(--text-main)]">
          {#each [3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0] as b}
            <option value={b}>{b.toFixed(1)}</option>
          {/each}
        </select>
        <button onclick={saveMock}
          class="px-3 py-1.5 rounded-lg btn-forest text-xs font-semibold cursor-pointer">Save</button>
      </div>
    {/if}

    {#if mockScores.length > 0}
      <div class="mt-3 space-y-1.5">
        {#each mockScores.slice(0, 8) as m}
          <div class="flex items-center justify-between text-xs border-b border-[var(--border-main)]/50 pb-1.5">
            <span class="font-mono text-[var(--text-muted)]">{m.taken_at}</span>
            <span class="font-semibold text-[var(--text-main)]">
              {m.skill} · <span class="text-[var(--accent-primary)]">{m.band.toFixed(1)}</span>
            </span>
            <button onclick={() => removeMock(m.id)} class="text-[var(--text-subtle)] hover:text-rose-500 cursor-pointer">✕</button>
          </div>
        {/each}
      </div>
    {:else}
      <p class="text-xs text-[var(--text-subtle)] mt-3">No mock scores yet — log checkpoint results here to track band progress.</p>
    {/if}
  </section>
</div>
