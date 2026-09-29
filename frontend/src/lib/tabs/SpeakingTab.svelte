<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import {
    Mic, Square, Play, Sparkles, RefreshCw, Timer,
    CheckCircle2, History, CircleAlert
  } from 'lucide-svelte';
  import {
    GetSpeakingPrompts, GetSpeakingTopics, GetRecordingStatus,
    StartSpeakingRecording, StopSpeakingRecording,
    EvaluateSpeaking, SaveSpeakingAttempt, GetSpeakingAttempts,
    PlayAudioUrl
  } from '../../../wailsjs/go/main/App.js';

  let { } = $props();

  interface Prompt {
    id: number; part: number; topic: string; question: string;
    cues: string[]; hint_vi: string; sample_ideas: string[];
  }

  let part = $state(1);
  let topic = $state('all');
  let topics = $state<string[]>([]);
  let prompts = $state<Prompt[]>([]);
  let current = $state<Prompt | null>(null);
  let seenIds = $state<number[]>([]);

  let recorderAvailable = $state(false);
  let recorderName = $state('');
  let recording = $state(false);
  let audioPath = $state('');
  let elapsed = $state(0);
  let timerId: ReturnType<typeof setInterval> | null = null;

  // Part 2 timers
  let prepLeft = $state(0);
  let talkLeft = $state(0);
  let phaseTimer: ReturnType<typeof setInterval> | null = null;

  let transcript = $state('');
  let evaluating = $state(false);
  let feedback = $state<any>(null);
  let feedbackRaw = $state('');
  let attempts = $state<any[]>([]);

  const CHECKLIST = [
    'Spoke without long pauses',
    'Answered the question directly',
    'Used a reason + example',
    'Used at least one complex sentence',
  ];
  let checks = $state<boolean[]>(CHECKLIST.map(() => false));

  async function loadPrompts() {
    prompts = (await GetSpeakingPrompts(part, topic)) as Prompt[];
    seenIds = [];
    pickNext();
  }

  function pickNext() {
    const fresh = prompts.filter(p => !seenIds.includes(p.id));
    if (fresh.length === 0) { seenIds = []; return pickNext(); }
    current = fresh[Math.floor(Math.random() * fresh.length)];
    seenIds = [...seenIds, current.id];
    resetAttempt();
    loadAttempts();
  }

  function resetAttempt() {
    audioPath = ''; transcript = ''; feedback = null; feedbackRaw = '';
    elapsed = 0; prepLeft = 0; talkLeft = 0;
    checks = CHECKLIST.map(() => false);
    stopTimers();
  }

  function stopTimers() {
    if (timerId) { clearInterval(timerId); timerId = null; }
    if (phaseTimer) { clearInterval(phaseTimer); phaseTimer = null; }
  }

  function startPrep() {
    prepLeft = 60;
    phaseTimer = setInterval(() => {
      prepLeft--;
      if (prepLeft <= 0 && phaseTimer) { clearInterval(phaseTimer); phaseTimer = null; }
    }, 1000);
  }

  async function toggleRecord() {
    try {
      if (!recording) {
        await StartSpeakingRecording();
        recording = true;
        elapsed = 0;
        if (current?.part === 2) talkLeft = 120;
        timerId = setInterval(() => {
          elapsed++;
          if (talkLeft > 0) talkLeft--;
          if (talkLeft === 1) stopRecord();
        }, 1000);
      } else {
        await stopRecord();
      }
    } catch (e) {
      console.warn(e);
      recording = false;
      stopTimers();
    }
  }

  async function stopRecord() {
    const st = await StopSpeakingRecording();
    recording = false;
    if (timerId) { clearInterval(timerId); timerId = null; }
    audioPath = st.audio_path || '';
  }

  function playRecording() {
    if (audioPath) PlayAudioUrl(audioPath, 1.0);
  }

  async function evaluate() {
    if (!current || !transcript.trim()) return;
    evaluating = true;
    feedback = null; feedbackRaw = '';
    try {
      const res = await EvaluateSpeaking(transcript, current.part, current.question, audioPath, elapsed);
      try {
        const cleaned = res.replace(/```json|```/g, '').trim();
        feedback = JSON.parse(cleaned.slice(cleaned.indexOf('{'), cleaned.lastIndexOf('}') + 1));
      } catch {
        feedbackRaw = res;
      }
      await SaveSpeakingAttempt(current.id, audioPath, elapsed, res);
      loadAttempts();
    } catch (e) {
      feedbackRaw = String(e);
    } finally {
      evaluating = false;
    }
  }

  async function loadAttempts() {
    if (!current) return;
    try { attempts = (await GetSpeakingAttempts(current.id)) || []; } catch { attempts = []; }
  }

  function fmtTime(s: number) {
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  }

  onMount(async () => {
    try {
      const [t, st] = await Promise.all([GetSpeakingTopics(), GetRecordingStatus()]);
      topics = t || [];
      recorderAvailable = st.available;
      recorderName = st.recorder;
      await loadPrompts();
    } catch (e) {
      console.warn(e);
    }
  });
  onDestroy(stopTimers);
</script>

<div class="w-full max-w-4xl mx-auto space-y-6 pb-12">
  <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] border border-[var(--border-main)]">
    <span class="journal-badge text-rose-600 bg-rose-500/10 px-2.5 py-1 rounded-md inline-flex items-center gap-1.5">
      <Mic class="w-3.5 h-3.5" /> Speaking Lab
    </span>
    <h1 class="font-serif text-3xl font-bold tracking-tight text-[var(--text-main)] mt-2.5">
      Speak first, polish later.
    </h1>
    <p class="text-sm text-[var(--text-muted)] font-sans mt-1">
      IELTS Part 1–3 practice · record, replay, get AI band feedback · {recorderAvailable ? `recorder: ${recorderName}` : 'self-check mode (no recorder found)'}
    </p>
  </section>

  <!-- Controls -->
  <section class="journal-card p-4 border border-[var(--border-main)] flex flex-wrap items-center gap-2.5">
    <div class="flex gap-1.5">
      {#each [1, 2, 3] as p}
        <button onclick={() => { part = p; loadPrompts(); }}
          class="px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer
            {part === p ? 'bg-[var(--accent-primary)] text-white' : 'text-[var(--text-muted)] hover:bg-[var(--accent-primary-light)]'}">
          Part {p}
        </button>
      {/each}
    </div>
    <select bind:value={topic} onchange={loadPrompts}
      class="px-3 py-1.5 rounded-lg border border-[var(--border-main)] bg-[var(--bg-inner)] text-xs text-[var(--text-main)]">
      <option value="all">All topics</option>
      {#each topics as t}<option value={t}>{t}</option>{/each}
    </select>
    <button onclick={pickNext} title="Next prompt"
      class="ml-auto p-2 rounded-lg text-[var(--text-muted)] hover:bg-[var(--accent-primary-light)] transition cursor-pointer">
      <RefreshCw class="w-4 h-4" />
    </button>
  </section>

  {#if current}
    <!-- Prompt card -->
    <section class="journal-card p-6 border border-[var(--border-main)] space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-[10px] font-mono font-bold text-[var(--accent-primary)] uppercase tracking-wider">
          Part {current.part} · {current.topic}
        </span>
        {#if current.part === 2}
          <button onclick={startPrep} disabled={prepLeft > 0}
            class="text-xs px-3 py-1.5 rounded-lg border border-[var(--border-main)] flex items-center gap-1.5 cursor-pointer disabled:opacity-40">
            <Timer class="w-3.5 h-3.5" />
            {prepLeft > 0 ? `Prep ${fmtTime(prepLeft)}` : 'Start 1 min prep'}
          </button>
        {/if}
      </div>

      <h2 class="font-serif text-xl sm:text-2xl font-bold text-[var(--text-main)] leading-snug">
        {current.question}
      </h2>

      {#if current.cues?.length}
        <ul class="space-y-1.5 text-sm text-[var(--text-muted)]">
          <li class="text-[11px] font-semibold uppercase tracking-wider text-[var(--text-subtle)]">You should say:</li>
          {#each current.cues as cue}<li class="pl-4 border-l-2 border-[var(--accent-primary)]/30">· {cue}</li>{/each}
        </ul>
      {/if}
      {#if current.hint_vi}
        <p class="text-xs italic text-[var(--text-subtle)]">💡 {current.hint_vi}</p>
      {/if}
    </section>

    <!-- Record + evaluate -->
    <section class="journal-card p-5 border border-[var(--border-main)] space-y-4">
      <div class="flex items-center gap-3 flex-wrap">
        {#if recorderAvailable}
          <button onclick={toggleRecord}
            class="px-5 py-2.5 rounded-xl font-semibold text-xs flex items-center gap-2 cursor-pointer transition
              {recording ? 'bg-rose-600 text-white animate-pulse' : 'btn-forest'}">
            {#if recording}<Square class="w-4 h-4" /> Stop · {fmtTime(elapsed)}{:else}<Mic class="w-4 h-4" /> Record{/if}
          </button>
          {#if talkLeft > 0 && recording}
            <span class="text-xs font-mono text-rose-600 font-bold">Talk left: {fmtTime(talkLeft)}</span>
          {/if}
          {#if audioPath && !recording}
            <button onclick={playRecording}
              class="px-4 py-2.5 rounded-xl border border-[var(--border-main)] text-xs font-semibold flex items-center gap-1.5 cursor-pointer hover:border-[var(--accent-primary)]">
              <Play class="w-3.5 h-3.5" /> Replay
            </button>
          {/if}
        {:else}
          <span class="text-xs text-amber-700 bg-amber-500/10 border border-amber-500/30 px-3 py-2 rounded-lg inline-flex items-center gap-1.5">
            <CircleAlert class="w-3.5 h-3.5" /> No mic recorder — use the checklist + transcript mode below
          </span>
        {/if}
      </div>

      <!-- Self-check while AI off -->
      <div class="grid sm:grid-cols-2 gap-2">
        {#each CHECKLIST as c, i}
          <button onclick={() => checks[i] = !checks[i]}
            class="flex items-center gap-2 text-left text-xs px-3 py-2 rounded-lg border transition cursor-pointer
              {checks[i] ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-700' : 'border-[var(--border-main)] text-[var(--text-muted)]'}">
            <CheckCircle2 class="w-3.5 h-3.5 shrink-0 {checks[i] ? 'text-emerald-600' : 'text-[var(--text-subtle)]'}" />
            {c}
          </button>
        {/each}
      </div>

      <!-- Transcript → AI band feedback -->
      <div class="space-y-2">
        <label for="speaking-transcript" class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">
          Transcript of what you said — for AI band evaluation
        </label>
        <textarea id="speaking-transcript" bind:value={transcript} rows="3"
          placeholder="Type (or paste) roughly what you just said — the AI scores this against IELTS band descriptors…"
          class="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-main)] bg-[var(--bg-inner)] text-sm text-[var(--text-main)] focus:border-[var(--accent-primary)] outline-none resize-y"></textarea>
        <button onclick={evaluate} disabled={evaluating || !transcript.trim()}
          class="px-4 py-2.5 rounded-xl btn-forest text-xs font-semibold flex items-center gap-1.5 cursor-pointer disabled:opacity-50">
          <Sparkles class="w-3.5 h-3.5" /> {evaluating ? 'Evaluating…' : 'Evaluate band'}
        </button>
      </div>

      <!-- AI feedback -->
      {#if feedback}
        <div class="rounded-xl border border-[var(--accent-primary)]/30 bg-[var(--accent-primary-light)]/40 p-4 space-y-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl font-serif font-bold text-[var(--accent-primary)]">{feedback.band_estimate ?? '—'}</span>
            <span class="text-[11px] font-mono text-[var(--text-muted)] uppercase">estimated band</span>
          </div>
          {#each [['Fluency', feedback.fluency], ['Vocabulary', feedback.lexical], ['Grammar', feedback.grammar]] as [label, txt]}
            {#if txt}<p class="text-xs text-[var(--text-muted)]"><b class="text-[var(--text-main)]">{label}:</b> {txt}</p>{/if}
          {/each}
          {#if feedback.improvements?.length}
            <div>
              <p class="text-[11px] font-semibold text-amber-700 uppercase">Fix next time</p>
              <ul class="text-xs text-[var(--text-muted)] list-disc pl-4 space-y-0.5">
                {#each feedback.improvements as imp}<li>{imp}</li>{/each}
              </ul>
            </div>
          {/if}
          {#if feedback.better_answer}
            <div class="pt-2 border-t border-[var(--border-main)]/50">
              <p class="text-[11px] font-semibold text-[var(--accent-primary)] uppercase">Band-7 sample</p>
              <p class="text-xs text-[var(--text-main)] italic mt-1">{feedback.better_answer}</p>
            </div>
          {/if}
        </div>
      {:else if feedbackRaw}
        <div class="rounded-xl border border-[var(--border-main)] p-4 text-xs text-[var(--text-muted)] whitespace-pre-wrap">{feedbackRaw}</div>
      {/if}
    </section>

    <!-- Attempts history -->
    {#if attempts.length}
      <section class="journal-card p-5 border border-[var(--border-main)]">
        <h3 class="text-sm font-semibold text-[var(--text-main)] flex items-center gap-2">
          <History class="w-4 h-4" /> Recent attempts on this prompt
        </h3>
        <div class="mt-2 space-y-1.5">
          {#each attempts.slice(0, 5) as a}
            <div class="text-xs text-[var(--text-muted)] flex items-center gap-2">
              <span class="font-mono">{a.created_at}</span>
              <span>· {a.duration}s</span>
              {#if a.audio_path}
                <button onclick={() => PlayAudioUrl(a.audio_path, 1.0)} class="text-[var(--accent-primary)] hover:underline cursor-pointer">▶ audio</button>
              {/if}
            </div>
          {/each}
        </div>
      </section>
    {/if}
  {/if}
</div>
