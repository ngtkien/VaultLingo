// IELTS 6.0 Roadmap — 16 weeks, 4 sessions/week (Mon · Wed · Sat · Sun), 60 min/session.
// Block A = Reading/Grammar (~30'), Block B = Speaking (~20'), Block C = app self-study (Dictation/Listening/WritingLab).
// Progress state lives in SQLite (roadmap_progress); this file holds the static plan.

export interface SessionPlan {
  id: number;
  week: number;
  phase: 1 | 2 | 3;
  /** JS getDay() value: 1=Mon, 3=Wed, 6=Sat, 0=Sun */
  weekday: number;
  dayLabel: string;
  blockA: string;
  blockB: string;
  appTask: string;
  milestone?: string;
  milestoneGoal?: string;
}

export interface WeekPlan {
  week: number;
  theme: string;
}

const PHASES: Record<number, { name: string; goal: string; color: string }> = {
  1: { name: 'Foundation', goal: 'Solid sentence structure · structural reading · basic speaking', color: 'emerald' },
  2: { name: 'Acceleration', goal: 'IELTS reading question types · Part 1 → Part 2 speaking', color: 'amber' },
  3: { name: 'Final Push', goal: 'Timed passages · Part 3 · mock tests → band 6.0', color: 'rose' },
};
export { PHASES };

export const START_DATE = '2026-10-05'; // Monday, week 1
const WEEKDAYS = [1, 3, 6, 0] as const; // Mon, Wed, Sat, Sun
const DAY_LABELS: Record<number, string> = { 1: 'Mon', 3: 'Wed', 6: 'Sat', 0: 'Sun' };

const APP_TASKS: Record<number, string> = {
  1: 'Dictation 5× A2→B1 (Dictation tab)',
  2: 'Dictation 5× B1–B2 + 1 listening dialogue',
  3: 'Dictation 5× B2 + Writing Lab prompt + AI score',
};

// [week, theme, [blockA, blockB] × 4 sessions (Mon, Wed, Sat, Sun)]
const WEEKS: [number, string, [string, string][]][] = [
  // ── Phase 1 · Foundation ──────────────────────────────────────────
  [1, 'Word forms & patterns', [
    ['Nature of English + 4 word forms (N/V/Adj/Adv)', 'Read 5 sample sentences aloud, identify word forms'],
    ['Word-form position in sentences — mark 20 sentences', 'Make 5 sentences and speak them aloud'],
    ['5 word patterns (SV, SVO, SV+Adj…)', 'Speak 5 sentences about today using each pattern'],
    ['Nouns + determiners (a/an/the/some)', 'Self-introduction 2 min — record baseline'],
  ]],
  [2, 'Simple sentences & structural reading', [
    ['Steps to write a correct simple sentence + verb patterns', 'Read your 10 written sentences aloud'],
    ['Structural reading — stop translating; simplify 10 long sentences', 'Retell sentence content in 1 min'],
    ['3 core tenses + Grammar tab drills', 'Part 1: 5 questions on Work/Study'],
    ['Read a 200-word paragraph structurally', 'Speak a 5-sentence chain about yesterday'],
  ]],
  [3, 'Complex sentences & whole-paragraph reading', [
    ['Relative clauses — analyse 10 sentences in a passage', 'Part 1 answers with reason + example'],
    ['Adverbial clauses — read a 250-word paragraph without a dictionary', 'Summarise the paragraph orally in 3 sentences'],
    ['Structural read of one short passage — mark 5 useful structures', 'Retell the passage in 2 min'],
    ['Paraphrase 10 sentence pairs', 'Part 1 — 6 questions, record'],
  ]],
  [4, 'Checkpoint — foundation', [
    ['Review: 20 mixed word-form/pattern sentences', 'Read aloud + Part 1 drill'],
    ['Mini reading: 1 passage, timed 15 min', 'Part 1 — 8 questions, record'],
    ['Structural read of 1 passage + summarise each paragraph', 'Mini mock Part 1 — 3 min continuous'],
    ['Checkpoint review + error log', 'Milestone check'],
  ]],
  // ── Phase 2 · Acceleration ────────────────────────────────────────
  [5, 'True/False/Not Given + Part 1', [
    ['T/F/NG — False vs Not Given', 'Part 1 structure: statement → reason → example'],
    ['T/F/NG — 1 passage + review', 'Part 1 — 6 questions, 30–45 s each, record'],
    ['Paraphrase in questions ↔ passage — 10 pairs', 'Part 1: Home/Hobbies'],
    ['Passage timed 20 min + error log', 'Replay recording — self-assess fluency'],
  ]],
  [6, 'Matching headings + Part 1 fluency', [
    ['Matching headings — paragraph-summary strategy', 'Write + speak your own Part 1 script (5 questions)'],
    ['Matching headings — 1 passage', 'Part 1 — answer without the script'],
    ['Timed passage + analyse hard sentences', 'Shadow a model Part 1 answer for 15 min'],
    ['Weekly review + error log', 'Part 1 drill — 8 mixed-topic questions'],
  ]],
  [7, 'Gap fill & summary + Part 2', [
    ['Gap fill + summary completion', 'Part 2 structure: intro → 4 cues → ending'],
    ['1 gap-fill passage, timed', '1 cue card — record'],
    ['Sentence completion + hard structures', 'Outline 3 cue cards (person/place/event)'],
    ['Mini test: half a Reading test, 30 min', 'Speak 1 full cue card, 1 min 30 s'],
  ]],
  [8, 'Reading speed + Part 2', [
    ['Timed passage 20 min — all errors to log', 'Part 2 — 2 cue cards, record'],
    ['Matching features', 'Part 2 + Part 1 mix'],
    ['2 consecutive passages in 40 min (stamina)', 'Part 3-style: 5 simple opinion questions'],
    ['Weekly review + topic vocabulary', 'Compare recording with session 4'],
  ]],
  [9, 'Checkpoint 5.0', [
    ['Mock Reading — 2 passages, 40 min', 'Score + analyse every error'],
    ['Mock Reading — passage 3 + weakest type', 'Part 1 + Part 2, record'],
    ['Review all mock reading errors', 'Mock Speaking full P1–P3, record'],
    ['Checkpoint review', 'Milestone check'],
  ]],
  // ── Phase 3 · Final push ──────────────────────────────────────────
  [10, 'Reading strategy & timing', [
    ['Full-passage structural reading + 20 min/passage pacing', 'Part 2 — open answers with statements'],
    ['Passage 1 timed + deep review', 'Part 2 — 2 cue cards'],
    ['Timed passage + weakest question type', 'Part 3: opinion + reason + example'],
    ['Error log + advanced paraphrase', 'Part 1 mix to keep rhythm'],
  ]],
  [11, 'First full reading test', [
    ['Reading full test 60 min — attempt 1', 'Score the band'],
    ['Analyse the mock: every error → its cause', 'Part 3 — 6 questions, record'],
    ['Redo the hardest passage', 'Part 2 — 2 unfamiliar cues'],
    ['Weekly review', 'Part 3: Education/Society'],
  ]],
  [12, 'Hard question types + Part 3', [
    ['Advanced T/F/NG — most-confused items', 'Part 3 — add a concession'],
    ['Passage 3 (hardest), timed', 'Part 3 — 6 abstract questions, record'],
    ['Reading full test — attempt 2', 'Compare with attempt 1'],
    ['Weekly review + error log', 'Mock Part 2 + Part 3, record'],
  ]],
  [13, 'Reading stamina', [
    ['2 consecutive passages, timed 40 min', 'Part 2 — 2 cue cards'],
    ['Passage + your personal weakest type', 'Part 3 drill'],
    ['Reading full test — attempt 3', 'Part 1–2 mix'],
    ['Analyse all 3 tests → error pattern', 'Part 3 — 5 questions'],
  ]],
  [14, 'Full speaking mock', [
    ['Timed passage + score', 'Mock Speaking full — record'],
    ['Weak-type drill', 'Self-score 4 criteria → pick 3 weaknesses'],
    ['2 passages timed', 'Work on weakness #1'],
    ['Full error-log review', 'Work on weakness #2'],
  ]],
  [15, 'Mock test 1', [
    ['Mock 1 — Reading full test 60 min', 'Score the band'],
    ['Analyse the reading mock', 'Mock 1 — Speaking full'],
    ['Re-drill the most-missed type', 'Self-score the speaking mock'],
    ['Mock 1 summary', 'Milestone check'],
  ]],
  [16, 'Mock 2 & test-ready', [
    ['Mock 2 — Reading full test', 'Fix remaining speaking weakness'],
    ['Last passage + strategy review', 'Mock 2 — Speaking full'],
    ['Review entire Reading error log', 'Compare with the session-4 recording'],
    ['Test-day checklist + room strategy', 'Milestone check'],
  ]],
];

const MILESTONES: Record<number, { name: string; goal: string }> = {
  16: { name: 'Checkpoint · Foundation', goal: 'Read one short passage structurally + Part 1 for 3 min → Phase 2' },
  36: { name: 'Checkpoint · 5.0', goal: 'Mock Reading ~5.0 + fluent P1–P3 speaking → Phase 3' },
  60: { name: 'Mock 1 complete', goal: 'R/S ≥ 5.5 — pick the 3 weakest points' },
  64: { name: 'Test ready', goal: 'Mock ≥ 6.0 stable → book the IELTS test' },
};

function buildSessions(): SessionPlan[] {
  const out: SessionPlan[] = [];
  let id = 0;
  for (const [week, , blocks] of WEEKS) {
    const phase = week <= 4 ? 1 : week <= 9 ? 2 : 3;
    blocks.forEach(([a, b], i) => {
      id++;
      const weekday = WEEKDAYS[i];
      out.push({
        id, week, phase, weekday,
        dayLabel: DAY_LABELS[weekday],
        blockA: a, blockB: b,
        appTask: APP_TASKS[phase],
        milestone: MILESTONES[id]?.name,
        milestoneGoal: MILESTONES[id]?.goal,
      });
    });
  }
  return out;
}

export const SESSIONS: SessionPlan[] = buildSessions();
export const TOTAL_SESSIONS = SESSIONS.length;

export const WEEK_META: WeekPlan[] = WEEKS.map(([week, theme]) => ({ week, theme }));

// ---------- date helpers ----------

const DAY_MS = 86400000;

export function baseDate(s: SessionPlan): Date {
  const d = new Date(START_DATE + 'T00:00:00');
  d.setDate(d.getDate() + (s.week - 1) * 7 + WEEKDAYS.indexOf(s.weekday as 1 | 3 | 6 | 0));
  return d;
}

function isStudyDay(d: Date): boolean {
  return (WEEKDAYS as readonly number[]).includes(d.getDay());
}

function nextStudyDay(from: Date): Date {
  const d = new Date(from);
  while (!isStudyDay(d)) d.setDate(d.getDate() + 1);
  return d;
}

function addStudyDays(from: Date, n: number): Date {
  const d = new Date(from);
  for (let i = 0; i < n; i++) {
    d.setDate(d.getDate() + 1);
    while (!isStudyDay(d)) d.setDate(d.getDate() + 1);
  }
  return d;
}

/**
 * Projected date of each pending session: remaining sessions are packed onto
 * upcoming study days starting from today — so missed work shifts the plan
 * forward automatically.
 */
export function projectedDates(doneIds: Set<number>, today = new Date()): Map<number, Date> {
  const map = new Map<number, Date>();
  const pending = SESSIONS.filter(s => !doneIds.has(s.id));
  let cursor = nextStudyDay(today);
  for (const s of pending) {
    map.set(s.id, new Date(cursor));
    cursor = addStudyDays(cursor, 1);
  }
  return map;
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' });
}
