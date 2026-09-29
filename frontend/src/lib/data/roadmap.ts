// IELTS 4.5 → 6.5 Roadmap — 24 weeks, 4 sessions/week (Mon · Wed · Sat · Sun), ~60 min/session.
// Rotation: Mon = Reading, Wed = Listening, Sat = Writing, Sun = Review.
// Every session ends with a Speaking block (~20') and an app self-study task (~10').
// Progress state lives in SQLite (roadmap_progress); this file holds the static plan.

export type SessionSkill = 'reading' | 'listening' | 'writing' | 'review';

export interface SessionPlan {
  id: number;
  week: number;
  phase: 1 | 2 | 3 | 4;
  /** JS getDay() value: 1=Mon, 3=Wed, 6=Sat, 0=Sun */
  weekday: number;
  dayLabel: string;
  /** Main block skill (~30') — Speaking block (~20') is always blockB. */
  skill: SessionSkill;
  blockA: string;
  blockB: string;
  appTask: string;
  /** Practice view id for deep-linking (dictation|listening|reading|writing|vocab|…). */
  appView: string;
  milestone?: string;
  milestoneGoal?: string;
}

export interface WeekPlan {
  week: number;
  theme: string;
}

export const SKILL_META: Record<SessionSkill, { label: string; minutes: number }> = {
  reading:   { label: 'Reading',   minutes: 30 },
  listening: { label: 'Listening', minutes: 30 },
  writing:   { label: 'Writing',   minutes: 30 },
  review:    { label: 'Review',    minutes: 30 },
};

const PHASES: Record<number, { name: string; goal: string; color: string }> = {
  1: { name: 'Foundation',    goal: 'Sentence structure · structural reading · Listening Part 1 · paragraph writing · Speaking Part 1', color: 'emerald' },
  2: { name: 'Skill Building', goal: 'All reading question types · Listening Parts 2–3 · Task 2 essays · Speaking Part 2', color: 'amber' },
  3: { name: 'Test Craft',    goal: 'Timing & stamina · Listening Part 4 · Task 1 reports · Speaking Part 3 · half mock', color: 'sky' },
  4: { name: 'Mock & Polish', goal: 'Full 4-skill mocks · error patterns · test-day strategy → band 6.0+', color: 'rose' },
};
export { PHASES };

export const START_DATE = '2026-10-05'; // Monday, week 1
const WEEKDAYS = [1, 3, 6, 0] as const; // Mon, Wed, Sat, Sun
const DAY_LABELS: Record<number, string> = { 1: 'Mon', 3: 'Wed', 6: 'Sat', 0: 'Sun' };

// App self-study keyed by phase → main skill of the day.
const APP_TASKS: Record<number, Record<SessionSkill, { task: string; view: string }>> = {
  1: {
    reading:   { task: 'Vocab SRS review (Vocabulary tab)', view: 'vocab' },
    listening: { task: 'Dictation 5× A2→B1 (Dictation tab)', view: 'dictation' },
    writing:   { task: 'Writing Lab — short prompt + AI score', view: 'writing' },
    review:    { task: 'Clear SRS queue + update error log', view: 'vocab' },
  },
  2: {
    reading:   { task: 'Reading tab — 1 passage at your band', view: 'reading' },
    listening: { task: 'Dictation 5× B1–B2 + 1 listening dialogue', view: 'dictation' },
    writing:   { task: 'Writing Lab — essay prompt + AI feedback', view: 'writing' },
    review:    { task: 'Clear SRS + error-log patterns', view: 'vocab' },
  },
  3: {
    reading:   { task: 'Reading tab — 1 timed passage', view: 'reading' },
    listening: { task: 'Dictation 5× B2 + Listening dialogue', view: 'dictation' },
    writing:   { task: 'Writing Lab — timed Task 2 + AI score', view: 'writing' },
    review:    { task: 'SRS + re-do 3 hardest error-log items', view: 'vocab' },
  },
  4: {
    reading:   { task: 'Reading tab — weakest question type', view: 'reading' },
    listening: { task: 'Listening dialogue + shadowing', view: 'listening' },
    writing:   { task: 'Writing Lab — polish an old essay', view: 'writing' },
    review:    { task: 'Light SRS only — conserve energy', view: 'vocab' },
  },
};

// [week, theme, [skill, main block, speaking block] × 4 sessions (Mon, Wed, Sat, Sun)]
const WEEKS: [number, string, [SessionSkill, string, string][]][] = [
  // ── Phase 1 · Foundation (weeks 1–5) ──────────────────────────────
  [1, 'Word forms & IELTS orientation', [
    ['reading',   'Nature of English + 4 word forms (N/V/Adj/Adv) — mark 20 sentences', 'Read 5 sample sentences aloud, name each word form'],
    ['listening', 'IELTS Listening format — 4 parts / 40 questions · Part 1: form completion', 'Spell names & read numbers/dates aloud'],
    ['writing',   'Write 10 correct simple sentences — SV / SVO / SV+Adj patterns', 'Read your 10 sentences aloud, fix what sounds wrong'],
    ['review',    'Word-form quiz (20 items) + open your error log', 'Self-introduction 2 min — record baseline'],
  ]],
  [2, 'Simple sentences & Part 1 details', [
    ['reading',   'Steps to a correct simple sentence + 5 core verb patterns', 'Speak 5 sentences about today using each pattern'],
    ['listening', 'Listening Part 1 — complete a form while listening (2 attempts)', 'Shadow the Part 1 transcript for 10 min'],
    ['writing',   'Paragraph building — topic sentence + 2 supporting sentences', 'Part 1: 5 questions on Work/Study'],
    ['review',    'Structural reading — simplify 10 long sentences, stop translating', 'Retell a 200-word paragraph in 1 min'],
  ]],
  [3, 'Complex sentences & listening distractors', [
    ['reading',   'Relative clauses — analyse 10 sentences inside a passage', 'Part 1 answers: statement + reason + example'],
    ['listening', 'Listening Part 1 — distractors: corrected numbers & changed answers', 'Record yourself reading the transcript'],
    ['writing',   'Combine sentences — relative + adverbial clauses into a paragraph', 'Describe your home in 6 sentences (record)'],
    ['review',    'Structural read of one short passage — mark 5 reusable structures', 'Part 1 — 6 questions, record'],
  ]],
  [4, 'Paragraph power & spelling accuracy', [
    ['reading',   'Adverbial clauses — read a 250-word paragraph without a dictionary', 'Summarise the paragraph orally in 3 sentences'],
    ['listening', 'Listening Part 1 — spelling drill: names, emails, postcodes at speed', 'Dictate your own details to yourself'],
    ['writing',   'Write a 120-word paragraph — my job / my studies', 'Read it aloud — record & self-check'],
    ['review',    'Paraphrase drill — 10 sentence pairs', 'Part 1 — 6 questions, record'],
  ]],
  [5, 'Checkpoint — foundation', [
    ['reading',   'Mini reading — 1 passage timed 15 min + review', 'Part 1 — 8 questions, record'],
    ['listening', 'Listening Part 1 mini-test (10 items) — target ≥7/10', 'Shadow the hardest section'],
    ['writing',   'Rewrite your week-4 paragraph cleaner — 150 words', 'Read it aloud — record'],
    ['review',    'Checkpoint review + full error-log pass', 'Milestone check'],
  ]],
  // ── Phase 2 · Skill building (weeks 6–12) ─────────────────────────
  [6, 'T/F/NG + Listening Part 2 + essay skeleton', [
    ['reading',   'T/F/NG — False vs Not Given, then 1 passage', 'Part 1 structure: statement → reason → example'],
    ['listening', 'Listening Part 2 — MCQ & matching strategies, 1 section timed', 'Part 1 — 6 questions, record'],
    ['writing',   'Task 2 skeleton — 4-paragraph opinion essay: intro + outline', 'Explain your opinion aloud in 1 min'],
    ['review',    'Paraphrase in questions ↔ passage — 10 pairs', 'Replay recording — self-assess fluency'],
  ]],
  [7, 'Matching headings + maps + full opinion essay', [
    ['reading',   'Matching headings — paragraph-summary strategy + 1 passage', 'Part 2 structure: intro → 4 cues → ending'],
    ['listening', 'Listening Part 2 — map / plan labelling drill', 'Outline 2 cue cards (person, place)'],
    ['writing',   'Write a full opinion essay — 250 words in 40 min', 'Speak your essay arguments in 2 min'],
    ['review',    'Weekly review + error log', 'Part 2 — 1 cue card, record'],
  ]],
  [8, 'Gap fill & summary + Listening Part 3', [
    ['reading',   'Gap fill + summary completion — 1 passage timed', 'Part 2 — 1 cue card, record'],
    ['listening', 'Listening Part 3 — multi-speaker talk: opinions & attitudes', 'Part 3-style: 3 simple opinion questions'],
    ['writing',   'Discussion essay (both views + opinion) — write 2 body paragraphs', 'Argue both sides aloud, 90 s each'],
    ['review',    'Mini test — 2 passages in 30 min', 'Speak 1 full cue card, 1 min 30 s'],
  ]],
  [9, 'Matching features + Part 3 speed', [
    ['reading',   'Matching features & statements — 1 timed passage', 'Part 2 — 2 cue cards, record'],
    ['listening', 'Listening Part 3 — full section timed + transcript review', 'Part 3: Education — 4 questions'],
    ['writing',   'Advantage/disadvantage essay — full essay in 40 min', 'Part 2 + Part 1 mix'],
    ['review',    'Weekly review + topic vocabulary', 'Compare recording with week-7'],
  ]],
  [10, 'Sentence completion + Part 3 distractors', [
    ['reading',   'Sentence completion & short answers — hard structures', 'Part 2 — event cue card, record'],
    ['listening', 'Listening Part 3 — distractors & speaker switches', 'Part 3: Technology — 4 questions'],
    ['writing',   'Problem/solution essay — outline + full essay in 40 min', 'Explain your solutions aloud, 2 min'],
    ['review',    '2 consecutive passages in 40 min (stamina)', 'Part 1–2 mixed drill'],
  ]],
  [11, 'Mixed types + flow charts & tables', [
    ['reading',   'Mixed question types — drill your weakest first', 'Part 2 — object cue card, record'],
    ['listening', 'Listening — flow-chart, table & note completion', 'Part 3: Environment — 4 questions'],
    ['writing',   'Two-part question essay — plan + full essay', 'Summarise your essay in 90 s'],
    ['review',    'Mock Reading — 2 passages, 40 min + error log', 'Part 2 + Part 3 mix'],
  ]],
  [12, 'Checkpoint 5.0', [
    ['reading',   'Mock Reading — passage 3 + weakest type, timed', 'Part 1 + Part 2, record'],
    ['listening', 'Mock Listening — Parts 1–2 (20 items) — target ≥15/20', 'Retell what you heard in 1 min'],
    ['writing',   'Timed Task 2 — self-check with band descriptors', 'Speak your essay as a 2-min answer'],
    ['review',    'Checkpoint review', 'Milestone check'],
  ]],
  // ── Phase 3 · Test craft (weeks 13–19) ────────────────────────────
  [13, 'Pacing + Listening Part 4 + Task 1', [
    ['reading',   'Full-passage structural reading + 20-min pacing', 'Part 3 — opinion + reason + example'],
    ['listening', 'Listening Part 4 — lecture note completion, 1 section', 'Summarise the lecture aloud in 3 sentences'],
    ['writing',   'Task 1 intro — report structure: intro + overview + 2 detail paragraphs', 'Describe a chart orally in 2 min'],
    ['review',    'Error log + advanced paraphrase', 'Part 1 mix to keep rhythm'],
  ]],
  [14, 'First full reading test + P4 strategies', [
    ['reading',   'Reading full test 60 min — attempt 1 → band score', 'Part 3 — 6 questions, record'],
    ['listening', 'Listening Part 4 — prediction & signpost language', 'Shadow a Part 4 lecture'],
    ['writing',   'Task 1 — line graph & bar chart: write 1 report in 20 min', 'Describe the trend orally in 2 min'],
    ['review',    'Analyse the reading mock — every error → its cause', 'Part 3: Education/Society'],
  ]],
  [15, 'Hardest types + full listening test', [
    ['reading',   'Passage 3 (hardest) timed + Yes/No/Not Given', 'Part 3 — add a concession'],
    ['listening', 'Listening full test — attempt 1 → score', 'Part 3 — 6 abstract questions, record'],
    ['writing',   'Task 1 — pie chart & table: write 1 report', 'Compare two charts aloud'],
    ['review',    'Redo hardest reading passage + weakest listening part', 'Mock Part 2 + Part 3, record'],
  ]],
  [16, 'Stamina + process & mixed charts', [
    ['reading',   '2 consecutive passages timed 40 min', 'Part 2 — 2 cue cards'],
    ['listening', 'Listening — Parts 3+4 back-to-back', 'Part 3 drill — Society questions'],
    ['writing',   'Task 1 — process & mixed charts: write 1 report', 'Describe a process aloud, 2 min'],
    ['review',    'Reading full test — attempt 2 → compare with attempt 1', 'Part 1–2 mix'],
  ]],
  [17, 'Speed & accuracy sprint', [
    ['reading',   'Speed drill — 2 passages × 15 min', 'Part 3 — 5 questions'],
    ['listening', 'Listening full test — attempt 2', 'Retell Part 4'],
    ['writing',   'Full writing — Task 1 + Task 2 in 60 min', 'Speak your Task 2 argument, 2 min'],
    ['review',    'Analyse all errors → your personal error pattern', 'Part 3 — 5 questions'],
  ]],
  [18, 'Full speaking mock + weakest links', [
    ['reading',   'Timed passage + score', 'Mock Speaking full (P1–P3) — record'],
    ['listening', 'Listening weakest part — targeted drill', 'Self-score 4 criteria → pick 3 weaknesses'],
    ['writing',   'Rewrite your worst essay — improve one band criterion', 'Work on weakness #1'],
    ['review',    'Full error-log review', 'Work on weakness #2'],
  ]],
  [19, 'Checkpoint 5.5 — half mock', [
    ['reading',   'Mock — Reading full test 60 min → score', 'Part 2 — 2 unfamiliar cues'],
    ['listening', 'Mock — Listening full test → score', 'Shadow weakest section'],
    ['writing',   'Mock — Writing Task 1 + Task 2, timed', 'Mock Speaking full — record'],
    ['review',    'Checkpoint review', 'Milestone check'],
  ]],
  // ── Phase 4 · Mock & polish (weeks 20–24) ─────────────────────────
  [20, 'Mock 1 week', [
    ['reading',   'Mock 1 — Reading full test 60 min', 'Part 3 — 6 questions'],
    ['listening', 'Mock 1 — Listening full test', 'Retell Part 4'],
    ['writing',   'Mock 1 — Writing T1 + T2 timed', 'Mock 1 — Speaking full, record'],
    ['review',    'Mock 1 debrief — log 4 band scores + error pattern', 'Light review — favourite topic'],
  ]],
  [21, 'Targeted fixes', [
    ['reading',   'Reading weakest question type — drill + 1 passage', 'Part 3 — add contrast markers'],
    ['listening', 'Listening weakest part — targeted drill', 'Part 2 — 2 cue cards'],
    ['writing',   'Rewrite Mock 1 essay — target +0.5 band', 'Speak revised essay aloud'],
    ['review',    'Error log — top 10 recurring errors', 'Part 1–3 mix'],
  ]],
  [22, 'Mock 2 week', [
    ['reading',   'Mock 2 — Reading full test', 'Part 3 — 6 questions'],
    ['listening', 'Mock 2 — Listening full test', 'Retell Part 4'],
    ['writing',   'Mock 2 — Writing T1 + T2 timed', 'Mock 2 — Speaking full, record'],
    ['review',    'Mock 2 debrief — compare with Mock 1', 'Light review + SRS'],
  ]],
  [23, 'Final polish', [
    ['reading',   'Last hardest passage + personal strategy card', 'Part 3 — abstract questions'],
    ['listening', 'Listening full test — attempt 3', 'Shadow review'],
    ['writing',   'Final timed writing — your weakest essay type', 'Mock Speaking full — record'],
    ['review',    'Review entire error log + saved vocab', 'Compare with week-1 baseline recording'],
  ]],
  [24, 'Test-ready', [
    ['reading',   'Light review — reading strategy checklist', 'Part 1 warm-up — 6 questions'],
    ['listening', "Light review — listening dos & don'ts", 'Part 2 — favourite cue card'],
    ['writing',   'Light review — writing templates & phrases', 'Part 3 — stay fluent, nothing new'],
    ['review',    'Test-day checklist + room strategy', 'Milestone check'],
  ]],
];

const MILESTONES: Record<number, { name: string; goal: string }> = {
  20: { name: 'Checkpoint · Foundation', goal: 'Structural reading + Part 1 listening ≥7/10 + 3-min Part 1 → Phase 2' },
  48: { name: 'Checkpoint · 5.0', goal: 'Mock R ~5.0 · L Parts 1–2 ≥15/20 · timed Task 2 → Phase 3' },
  76: { name: 'Checkpoint · 5.5', goal: 'Half mock R/L ≥5.5 · W/S coherent under time → Phase 4' },
  80: { name: 'Mock 1 complete', goal: 'First full 4-skill mock — log all 4 band scores' },
  88: { name: 'Mock 2 complete', goal: 'R/L ≥6.0 · pick the final weak points' },
  96: { name: 'Test ready', goal: 'Mocks ≥6.0 stable across 4 skills → book the IELTS test' },
};

function buildSessions(): SessionPlan[] {
  const out: SessionPlan[] = [];
  let id = 0;
  for (const [week, , blocks] of WEEKS) {
    const phase = week <= 5 ? 1 : week <= 12 ? 2 : week <= 19 ? 3 : 4;
    blocks.forEach(([skill, a, b], i) => {
      id++;
      const weekday = WEEKDAYS[i];
      const app = APP_TASKS[phase][skill];
      out.push({
        id, week, phase, weekday, skill,
        dayLabel: DAY_LABELS[weekday],
        blockA: a, blockB: b,
        appTask: app.task, appView: app.view,
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
