<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Map, CheckCircle2, SkipForward, RotateCcw, Flag,
    BookOpen, Mic, Smartphone, ChevronDown, Trophy,
    Headphones, PenLine, ClipboardCheck, Play, StickyNote,
    TrendingUp, TrendingDown, Minus
  } from 'lucide-svelte';
  import { GetRoadmapProgress, MarkSession, GetMockScores, AddMockScore, DeleteMockScore, SetSessionNote } from '../../../wailsjs/go/main/App.js';
  import { markToday } from '../utils/daily';
  import {
    SESSIONS, WEEK_META, PHASES, TOTAL_SESSIONS, SKILL_META,
    projectedDates, baseDate, formatDate, type SessionPlan, type SessionSkill
  } from '../data/roadmap';

  let { onNavigate } = $props<{
    onNavigate?: (area: string, view?: string) => void;
  }>();

  type Status = 'pending' | 'done' | 'missed';
  type ProgressEntry = { status: Status; actual_date?: string; note?: string };

  let progress = $state<Record<number, ProgressEntry>>({});
  let mockScores = $state<any[]>([]);
  let loading = $state(true);
  let openWeeks = $state<Set<number>>(new Set());
  let mockSkill = $state('R');
  let mockBand = $state(5.0);
  let mockNote = $state('');
  let showMockForm = $state(false);
  let noteEditingId = $state<number | null>(null);
  let noteDraft = $state('');

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
  let currentWeek = $derived(nextSession?.week ?? 24);

  // Latest band per skill (+ delta vs the previous attempt) for the summary row.
  let skillBands = $derived.by(() => {
    const out: Record<string, { band: number; prev?: number }> = {};
    for (const m of mockScores) {
      if (!out[m.skill]) out[m.skill] = { band: m.band };
      else if (out[m.skill].prev === undefined) out[m.skill].prev = m.band;
    }
    return out;
  });

  function sessionStatus(s: SessionPlan): Status {
    return progress[s.id]?.status ?? 'pending';
  }

  function sessionNote(s: SessionPlan): string {
    return progress[s.id]?.note ?? '';
  }

  function displayDate(s: SessionPlan): Date {
    return doneIds.has(s.id) ? baseDate(s) : (projections.get(s.id) ?? baseDate(s));
  }

  function openPractice(view: string) {
    if (!onNavigate || !view) return;
    onNavigate(view === 'vocab' ? 'learn' : 'practice', view);
  }

  async function mark(id: number, status: Status) {
    try {
      await MarkSession(id, status === 'pending' ? 'pending' : status, sessionNote(SESSIONS[id - 1]));
      progress = await GetRoadmapProgress();
      if (status === 'done') markToday('roadmap');
    } catch (e) {
      console.warn(e);
    }
  }

  function startNoteEdit(s: SessionPlan) {
    noteEditingId = s.id;
    noteDraft = sessionNote(s);
  }

  async function saveNote(id: number) {
    try {
      await SetSessionNote(id, noteDraft.trim());
      progress = await GetRoadmapProgress();
      noteEditingId = null;
      noteDraft = '';
    } catch (e) {
      console.warn(e);
    }
  }

  async function saveMock() {
    try {
      await AddMockScore(mockSkill, mockBand, mockNote.trim());
      mockScores = await GetMockScores();
      showMockForm = false;
      mockNote = '';
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

  let allOpen = $derived(openWeeks.size >= WEEK_META.length);
  function toggleAllWeeks() {
    openWeeks = allOpen ? new Set([currentWeek]) : new Set(WEEK_META.map(w => w.week));
  }

  const phaseBadge: Record<number, string> = {
    1: 'bg-emerald-500/15 text-emerald-700 border-emerald-500/30',
    2: 'bg-amber-500/15 text-amber-700 border-amber-500/30',
    3: 'bg-sky-500/15 text-sky-700 border-sky-500/30',
    4: 'bg-rose-500/15 text-rose-700 border-rose-500/30',
  };

  const skillBadge: Record<SessionSkill, string> = {
    reading:   'bg-emerald-500/15 text-emerald-700 border-emerald-500/30',
    listening: 'bg-sky-500/15 text-sky-700 border-sky-500/30',
    writing:   'bg-violet-500/15 text-violet-700 border-violet-500/30',
    review:    'bg-slate-500/15 text-slate-600 border-slate-500/30',
  };

  const skillIconColor: Record<SessionSkill, string> = {
    reading:   'text-emerald-600',
    listening: 'text-sky-600',
    writing:   'text-violet-600',
    review:    'text-slate-500',
  };

  const MOCK_SKILLS: Record<string, string> = { L: 'Listening', R: 'Reading', W: 'Writing', S: 'Speaking' };

  onMount(async () => {
    try {
      const [p, m] = await Promise.all([GetRoadmapProgress(), GetMockScores().catch(() => [])]);
      progress = p || {};
      mockScores = m || [];
      // open current week by default
      const ns = SESSIONS.find(s => progress[s.id]?.status !== 'done');
      openWeeks = new Set([ns?.week ?? 24]);
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
          4.5 → 6.5 in 24 weeks
        </h1>
        <p class="text-sm text-[var(--text-muted)] font-sans">
          {TOTAL_SESSIONS} sessions · Mon / Wed / Sat / Sun · 60 min each · all 4 skills
        </p>
        <p class="text-xs text-[var(--text-subtle)] font-sans">
          Mon Reading · Wed Listening · Sat Writing · Sun Review — every session ends with Speaking
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
        <div class="min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-[11px] font-mono font-semibold text-[var(--accent-primary)] uppercase tracking-wider">
              Next up · Session {ns.id} · {ns.dayLabel} {formatDate(displayDate(ns))} · Week {ns.week}
            </span>
            <span class="text-[10px] px-1.5 py-0.5 rounded border font-semibold {skillBadge[ns.skill]}">
              {SKILL_META[ns.skill].label}
            </span>
          </div>
          <h3 class="font-serif font-bold text-lg text-[var(--text-main)] mt-1">{ns.blockA}</h3>
          <p class="text-xs text-[var(--text-muted)] mt-0.5">Speaking: {ns.blockB}</p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          {#if onNavigate && ns.appView}
            <button onclick={() => openPractice(ns.appView)}
              class="px-3.5 py-2.5 rounded-xl border border-[var(--accent-primary)]/50 text-[var(--accent-primary)] font-semibold text-xs flex items-center gap-1.5 cursor-pointer hover:bg-[var(--accent-primary-light)] transition">
              <Play class="w-3.5 h-3.5" /> Practice
            </button>
          {/if}
          <button onclick={() => mark(ns.id, 'done')}
            class="px-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center gap-1.5 cursor-pointer">
            <CheckCircle2 class="w-4 h-4" /> Mark done
          </button>
        </div>
      </div>
    </section>
  {/if}

  <!-- Weeks -->
  {#if loading}
    <p class="text-sm text-[var(--text-muted)] text-center py-10">Loading roadmap…</p>
  {:else}
    <div class="flex items-center justify-between">
      <h2 class="text-base font-semibold text-[var(--text-main)]">Study plan — {WEEK_META.length} weeks</h2>
      <button onclick={toggleAllWeeks}
        class="text-[11px] font-semibold px-2.5 py-1 rounded-lg border border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] hover:border-[var(--accent-primary)] transition cursor-pointer">
        {allOpen ? 'Collapse all' : 'Expand all'}
      </button>
    </div>
    {#each WEEK_META as w}
      {@const sessions = SESSIONS.filter(s => s.week === w.week)}
      {@const wDone = sessions.filter(s => sessionStatus(s) === 'done').length}
      {@const isOpen = openWeeks.has(w.week)}
      {@const phase = sessions[0]?.phase ?? 1}
      {@const isCurrent = w.week === currentWeek}
      <section class="journal-card border overflow-hidden {isCurrent ? 'border-[var(--accent-primary)]/50' : 'border-[var(--border-main)]'}">
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
            {#if isCurrent}
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] font-bold">NOW</span>
            {/if}
            <span class="text-[11px] font-mono text-[var(--text-subtle)]">{wDone}/{sessions.length}</span>
            <ChevronDown class="w-4 h-4 text-[var(--text-muted)] transition-transform {isOpen ? 'rotate-180' : ''}" />
          </div>
        </button>

        {#if isOpen}
          <div class="border-t border-[var(--border-main)] divide-y divide-[var(--border-main)]/50">
            {#each sessions as s}
              {@const st = sessionStatus(s)}
              {@const note = sessionNote(s)}
              <div class="p-4 space-y-2.5 {st === 'done' ? 'opacity-60' : ''} {s.milestone ? 'bg-amber-500/5' : ''}">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0">
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="text-[11px] font-mono font-bold text-[var(--text-muted)]">
                        #{s.id} · {s.dayLabel} {formatDate(displayDate(s))}
                      </span>
                      <span class="text-[10px] px-1.5 py-0.5 rounded border font-semibold {skillBadge[s.skill]}">
                        {SKILL_META[s.skill].label}
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
                    <button onclick={() => noteEditingId === s.id ? noteEditingId = null : startNoteEdit(s)}
                      title="Session note"
                      class="p-1.5 rounded-lg transition cursor-pointer {note ? 'text-amber-600 hover:bg-amber-500/15' : 'text-[var(--text-subtle)] hover:bg-[var(--bg-inner)]'}">
                      <StickyNote class="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div class="grid sm:grid-cols-3 gap-2 text-xs">
                  <div class="flex gap-1.5 items-start">
                    {#if s.skill === 'reading'}
                      <BookOpen class="w-3.5 h-3.5 mt-0.5 shrink-0 {skillIconColor[s.skill]}" />
                    {:else if s.skill === 'listening'}
                      <Headphones class="w-3.5 h-3.5 mt-0.5 shrink-0 {skillIconColor[s.skill]}" />
                    {:else if s.skill === 'writing'}
                      <PenLine class="w-3.5 h-3.5 mt-0.5 shrink-0 {skillIconColor[s.skill]}" />
                    {:else}
                      <ClipboardCheck class="w-3.5 h-3.5 mt-0.5 shrink-0 {skillIconColor[s.skill]}" />
                    {/if}
                    <span class="text-[var(--text-muted)]"><b class="text-[var(--text-main)] font-medium">{SKILL_META[s.skill].label}:</b> {s.blockA}</span>
                  </div>
                  <div class="flex gap-1.5 items-start">
                    <Mic class="w-3.5 h-3.5 mt-0.5 shrink-0 text-rose-500" />
                    <span class="text-[var(--text-muted)]"><b class="text-[var(--text-main)] font-medium">Speaking:</b> {s.blockB}</span>
                  </div>
                  <div class="flex gap-1.5 items-start">
                    <Smartphone class="w-3.5 h-3.5 mt-0.5 shrink-0 text-[var(--text-subtle)]" />
                    {#if onNavigate && s.appView && st !== 'done'}
                      <button onclick={() => openPractice(s.appView)}
                        class="text-left text-[var(--accent-primary)] hover:underline cursor-pointer">
                        {s.appTask} →
                      </button>
                    {:else}
                      <span class="text-[var(--text-subtle)]">{s.appTask}</span>
                    {/if}
                  </div>
                </div>

                {#if note && noteEditingId !== s.id}
                  <p class="text-[11px] text-amber-800 bg-amber-500/10 border border-amber-500/20 rounded-lg px-2.5 py-1.5 flex items-start gap-1.5">
                    <StickyNote class="w-3 h-3 mt-0.5 shrink-0" /> {note}
                  </p>
                {/if}
                {#if noteEditingId === s.id}
                  <div class="flex items-center gap-2">
                    <input bind:value={noteDraft}
                      onkeydown={(e) => { if (e.key === 'Enter') saveNote(s.id); if (e.key === 'Escape') noteEditingId = null; }}
                      placeholder="Note for this session (score, errors, reminders…)"
                      class="flex-1 px-3 py-1.5 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-xs text-[var(--text-main)] focus:outline-none focus:border-[var(--accent-primary)]" />
                    <button onclick={() => saveNote(s.id)}
                      class="px-3 py-1.5 rounded-lg btn-forest text-[11px] font-semibold cursor-pointer">Save</button>
                  </div>
                {/if}
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
        <input bind:value={mockNote} placeholder="Note (e.g. Cambridge 18 Test 2)"
          class="px-3 py-1.5 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-sm text-[var(--text-main)] w-56 max-w-full" />
        <button onclick={saveMock}
          class="px-3 py-1.5 rounded-lg btn-forest text-xs font-semibold cursor-pointer">Save</button>
      </div>
    {/if}

    <!-- Latest band per skill -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-4">
      {#each Object.entries(MOCK_SKILLS) as [k, label]}
        {@const sb = skillBands[k]}
        <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
          <div class="text-[10px] font-semibold uppercase tracking-wider text-[var(--text-subtle)]">{label}</div>
          {#if sb}
            <div class="flex items-baseline gap-1.5 mt-1">
              <span class="text-xl font-bold font-serif {sb.band >= 6 ? 'text-emerald-600' : sb.band >= 5 ? 'text-amber-600' : 'text-rose-600'}">{sb.band.toFixed(1)}</span>
              {#if sb.prev !== undefined}
                {@const delta = sb.band - sb.prev}
                <span class="text-[10px] font-mono flex items-center {delta > 0 ? 'text-emerald-600' : delta < 0 ? 'text-rose-500' : 'text-[var(--text-subtle)]'}">
                  {#if delta > 0}<TrendingUp class="w-3 h-3" />+{delta.toFixed(1)}
                  {:else if delta < 0}<TrendingDown class="w-3 h-3" />{delta.toFixed(1)}
                  {:else}<Minus class="w-3 h-3" />0{/if}
                </span>
              {/if}
            </div>
          {:else}
            <div class="text-xl font-bold font-serif text-[var(--text-subtle)] mt-1">—</div>
          {/if}
        </div>
      {/each}
    </div>

    {#if mockScores.length > 0}
      <div class="mt-3 space-y-1.5">
        {#each mockScores.slice(0, 8) as m}
          <div class="flex items-center justify-between text-xs border-b border-[var(--border-main)]/50 pb-1.5 gap-2">
            <span class="font-mono text-[var(--text-muted)] shrink-0">{m.taken_at}</span>
            {#if m.note}<span class="text-[var(--text-subtle)] truncate flex-1 min-w-0">{m.note}</span>{:else}<span class="flex-1"></span>{/if}
            <span class="font-semibold text-[var(--text-main)] shrink-0">
              {m.skill} · <span class="text-[var(--accent-primary)]">{m.band.toFixed(1)}</span>
            </span>
            <button onclick={() => removeMock(m.id)} class="text-[var(--text-subtle)] hover:text-rose-500 cursor-pointer shrink-0">✕</button>
          </div>
        {/each}
      </div>
    {:else}
      <p class="text-xs text-[var(--text-subtle)] mt-3">No mock scores yet — log checkpoint results here to track band progress.</p>
    {/if}
  </section>
</div>
