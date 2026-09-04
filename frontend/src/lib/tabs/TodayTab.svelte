<script lang="ts">
  import { 
    Clock, 
    Flame, 
    Award, 
    Target, 
    Sparkles, 
    ArrowRight, 
    BookOpen, 
    Headphones, 
    PenTool, 
    CheckCircle2, 
    FileText, 
    ChevronRight,
    Volume2
  } from 'lucide-svelte';

  let { 
    dueCount = 18, 
    idiom = null,
    onNavigate,
    onOpenWord
  } = $props<{ 
    dueCount?: number; 
    idiom?: any;
    onNavigate: (area: string, view?: string) => void;
    onOpenWord?: (word: string) => void;
  }>();

  // Progress state
  const streakDays = 7;
  const bestStreak = 42;
  const userXP = 1250;
  const userLevel = 12;
  const weeklyDays = 4;
  const weeklyTarget = 7;
  const minutesToday = 94;
  const dailyTargetMinutes = 120;

  const quote = {
    word: "architecture",
    pos: "noun",
    phonetic: "/ˈɑːr.kə.tek.tʃɚ/",
    definition: "The structure, design, or intentional framework of a complex system.",
    quoteText: "Language is the architecture of thought.",
    author: "Joseph Joubert"
  };

  const recentNotes = [
    { title: "System Design Best Practices", tag: "Tech", time: "2h ago" },
    { title: "Rosy Logic - Database Indexes", tag: "Backend", time: "Yesterday" }
  ];
</script>

<div class="w-full max-w-6xl mx-auto space-y-6 pb-12">
  <!-- Top Editorial Hero: Daily Practice & Plan -->
  <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] relative overflow-hidden border border-[var(--border-main)]">
    <div class="max-w-3xl space-y-3">
      <div class="flex items-center gap-2">
        <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-1 rounded-md">
          Your Daily Practice
        </span>
        <span class="text-xs text-[var(--text-muted)] font-serif italic">
          20 minutes to fluency
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
          <p class="text-xs text-[var(--text-muted)]">Stay consistent, build fluency.</p>
        </div>
        <span class="text-xs font-serif italic text-[var(--accent-primary)]">
          Plan your day, make it count.
        </span>
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
            <BookOpen class="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] transition" />
          </div>
          <div class="mt-4">
            <h3 class="text-sm font-bold text-[var(--text-main)] group-hover:text-[var(--accent-primary)] transition">
              Review due words
            </h3>
            <p class="text-xs text-[var(--text-muted)] mt-0.5">
              {dueCount || 18} words due
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
            <Headphones class="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] transition" />
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
            <Sparkles class="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] transition" />
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

  <!-- Middle Grid: Your Progress & Focus Session & Review Queue -->
  <div class="grid lg:grid-cols-3 gap-6">
    <!-- Column 1 & 2: Your Progress & Focus Session -->
    <div class="lg:col-span-2 space-y-6">
      <!-- Your Progress Box -->
      <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)]">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-semibold text-[var(--text-main)]">Your Progress</h2>
          <span class="text-xs text-[var(--text-muted)] font-mono">Updated today</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <!-- Streak -->
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Day streak</span>
              <Flame class="w-4 h-4 text-amber-500" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {streakDays}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              Best: {bestStreak} days
            </p>
          </div>

          <!-- Level & XP -->
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Level</span>
              <Award class="w-4 h-4 text-emerald-600" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {userLevel}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              {userXP.toLocaleString()} XP
            </p>
          </div>

          <!-- Weekly Goal -->
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Weekly goal</span>
              <Target class="w-4 h-4 text-blue-500" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {weeklyDays}/{weeklyTarget}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              Days on track
            </p>
          </div>

          <!-- Minutes Today -->
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
            <div class="flex items-center justify-between">
              <span class="text-xs text-[var(--text-muted)]">Min today</span>
              <Clock class="w-4 h-4 text-[var(--accent-primary)]" />
            </div>
            <div class="mt-2 text-2xl font-bold font-serif text-[var(--text-main)]">
              {minutesToday}
            </div>
            <p class="text-[11px] text-[var(--text-subtle)] mt-0.5">
              Goal: {dailyTargetMinutes} min
            </p>
          </div>
        </div>
      </section>

      <!-- Focus Session Banner -->
      <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] bg-gradient-to-r from-[var(--bg-card)] to-[var(--bg-inner)]">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="space-y-1.5">
            <div class="flex items-center gap-2">
              <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2 py-0.5 rounded text-[10px]">
                Focus Session
              </span>
              <span class="text-xs text-[var(--text-muted)]">A focused block to keep your momentum</span>
            </div>
            <h3 class="text-lg font-bold font-serif text-[var(--text-main)]">
              Workplace Communication & Clarity
            </h3>
            <p class="text-xs text-[var(--text-muted)] max-w-md">
              Refine your professional tone and phrasing for real-world engineering syncs.
            </p>
          </div>

          <button
            onclick={() => onNavigate('practice', 'writing')}
            class="px-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center justify-center gap-1.5 shrink-0 shadow-sm"
          >
            <span>Continue Session</span>
            <ArrowRight class="w-3.5 h-3.5" />
          </button>
        </div>
      </section>
    </div>

    <!-- Column 3: Review Queue -->
    <div class="space-y-6">
      <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] h-full flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border-main)]">
            <div>
              <h2 class="text-base font-semibold text-[var(--text-main)]">Review Queue</h2>
              <p class="text-xs text-[var(--text-muted)]">Keep your knowledge fresh.</p>
            </div>
            <span class="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
              {dueCount || 18} due
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
                {dueCount || 18} due <ChevronRight class="w-3.5 h-3.5" />
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
                1 due <ChevronRight class="w-3.5 h-3.5" />
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
                2 due <ChevronRight class="w-3.5 h-3.5" />
              </span>
            </button>
          </div>
        </div>

        <button
          onclick={() => onNavigate('learn', 'vocab')}
          class="w-full mt-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center justify-center gap-1.5 shadow-sm"
        >
          <span>Go to review</span>
          <ArrowRight class="w-3.5 h-3.5" />
        </button>
      </section>
    </div>
  </div>

  <!-- Bottom Row: Recently Opened & Word Journal -->
  <div class="grid md:grid-cols-2 gap-6">
    <!-- Recently Opened Notes -->
    <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)]">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-base font-semibold text-[var(--text-main)]">Recently Opened</h2>
        <button onclick={() => onNavigate('library')} class="text-xs text-[var(--accent-primary)] hover:underline cursor-pointer">
          View all
        </button>
      </div>

      <div class="space-y-2.5">
        {#each recentNotes as note}
          <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex items-center justify-between">
            <div class="flex items-center gap-3">
              <FileText class="w-4 h-4 text-[var(--accent-primary)]" />
              <div>
                <h3 class="text-xs font-semibold text-[var(--text-main)]">{note.title}</h3>
                <span class="text-[10px] text-[var(--text-subtle)] font-mono">{note.time}</span>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] bg-[var(--bg-card)] border border-[var(--border-main)] text-[var(--text-muted)]">
              {note.tag}
            </span>
          </div>
        {/each}
      </div>
    </section>

    <!-- Word Journal Quote -->
    <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] flex flex-col justify-between">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-base font-semibold text-[var(--text-main)]">Word Journal</h2>
        <button onclick={() => onOpenWord?.(quote.word)} class="text-xs text-[var(--accent-primary)] hover:underline cursor-pointer">
          View in Dictionary
        </button>
      </div>

      <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
        <div class="flex items-center justify-between">
          <div>
            <span class="font-serif font-bold text-base text-[var(--text-main)]">{quote.word}</span>
            <span class="text-xs text-[var(--text-muted)] font-mono ml-2">{quote.phonetic}</span>
          </div>
          <span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
            {quote.pos}
          </span>
        </div>

        <p class="text-xs text-[var(--text-muted)]">
          {quote.definition}
        </p>

        <blockquote class="pt-2 border-t border-[var(--border-main)] mt-2">
          <p class="font-serif italic text-sm text-[var(--text-main)] leading-snug">
            “{quote.quoteText}”
          </p>
          <cite class="text-[11px] text-[var(--text-subtle)] block mt-1">
            — {quote.author}
          </cite>
        </blockquote>
      </div>

      <div class="mt-4 pt-3 flex items-center justify-between border-t border-[var(--border-main)]">
        <button
          onclick={() => onOpenWord?.(quote.word)}
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
