// Daily Pull tracker — 100% local, honest, no fake stats.
// Stores one entry per day in localStorage:
//   vaultlingo_day_YYYY-MM-DD = { visited, review, dictation, listening }
export interface DayRecord {
  visited: boolean;
  review: boolean;
  dictation: boolean;
  listening: boolean;
}

const DAY_PREFIX = 'vaultlingo_day_';

export function todayKey(d = new Date()): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${DAY_PREFIX}${y}-${m}-${day}`;
}

function dateKeyFromOffset(offsetDays: number): string {
  const d = new Date();
  d.setDate(d.getDate() - offsetDays);
  return todayKey(d);
}

export function getDayRecord(key?: string): DayRecord {
  const k = key || todayKey();
  try {
    const raw = localStorage.getItem(k);
    if (raw) {
      const p = JSON.parse(raw);
      return {
        visited: !!p.visited,
        review: !!p.review,
        dictation: !!p.dictation,
        listening: !!p.listening,
      };
    }
  } catch {}
  return { visited: false, review: false, dictation: false, listening: false };
}

export function markToday(task?: keyof DayRecord): DayRecord {
  const k = todayKey();
  const rec = getDayRecord(k);
  rec.visited = true;
  if (task) rec[task] = true;
  try {
    localStorage.setItem(k, JSON.stringify(rec));
  } catch {}
  return rec;
}

/** Consecutive days with visited=true, counting today (or yesterday if today not yet visited). */
export function getStreak(): number {
  let streak = 0;
  // If today not visited yet, streak can still continue from yesterday.
  const today = getDayRecord();
  let offset = today.visited ? 0 : 1;
  while (true) {
    const rec = getDayRecord(dateKeyFromOffset(offset));
    if (rec.visited) {
      streak++;
      offset++;
    } else {
      break;
    }
    if (streak > 3650) break;
  }
  return streak;
}

export function getTodayProgress(): { done: number; total: number; pct: number; rec: DayRecord } {
  const rec = getDayRecord();
  const tasks = [rec.review, rec.dictation, rec.listening];
  const done = tasks.filter(Boolean).length;
  return { done, total: 3, pct: Math.round((done / 3) * 100), rec };
}
