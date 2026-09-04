<script lang="ts">
  import { 
    Headphones, 
    Ear, 
    Dumbbell, 
    PenTool, 
    Clock, 
    Flame, 
    Award, 
    Target, 
    ArrowRight, 
    Sparkles, 
    CheckCircle2, 
    History,
    ShieldCheck
  } from 'lucide-svelte';

  let { onSelectPracticeTab } = $props<{
    onSelectPracticeTab: (tabId: 'dictation' | 'listening' | 'grammar' | 'writing') => void;
  }>();

  const minutesPracticed = 78;
  const targetMinutes = 120;
  const dailyPercentage = 68;
  const streakDays = 7;
  const userXP = 1250;
  const userLevel = 12;

  const practiceModules = [
    {
      id: 'dictation' as const,
      title: 'Dictation',
      desc: 'Train your ear and refine your spelling with real-world audio dictation.',
      duration: '10-20 min',
      icon: Headphones,
      cta: 'Start Dictation'
    },
    {
      id: 'listening' as const,
      title: 'Listening',
      desc: 'Improve comprehension with conversational topics, transcripts, and targeted listening practice.',
      duration: '10-25 min',
      icon: Ear,
      cta: 'Start Listening'
    },
    {
      id: 'grammar' as const,
      title: 'Grammar Gym',
      desc: 'Strengthen grammar and usage through focused exercises and questions.',
      duration: '10-20 min',
      icon: Dumbbell,
      cta: 'Start Grammar Gym'
    },
    {
      id: 'writing' as const,
      title: 'Writing Lab',
      desc: 'Build clarity and structure with guided scenarios and AI feedback.',
      duration: '15-30 min',
      icon: PenTool,
      cta: 'Start Writing Lab'
    }
  ];

  const recentPractice = [
    { type: 'Dictation', topic: 'Workplace Communication', level: 'B1', time: '5 min ago', tab: 'dictation' as const },
    { type: 'Listening', topic: 'Family Dialogue', level: 'B1', time: '1 hour ago', tab: 'listening' as const },
    { type: 'Grammar Gym', topic: 'Present Perfect & QUASM', level: 'B1', time: '1 day ago', tab: 'grammar' as const },
    { type: 'Writing Lab', topic: 'Clarifying Requirements', level: 'B1', time: '2 days ago', tab: 'writing' as const }
  ];
</script>

<div class="w-full max-w-6xl mx-auto space-y-6 pb-12">
  <!-- Hero Banner -->
  <section class="journal-card p-6 sm:p-8 bg-[var(--bg-card)] border border-[var(--border-main)]">
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
      <div class="max-w-2xl space-y-2.5">
        <div class="flex items-center gap-2">
          <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-1 rounded-md">
            Welcome to Practice
          </span>
          <span class="text-xs text-[var(--text-muted)] font-serif italic">
            Small steps. Strong foundations. Lasting mastery.
          </span>
        </div>

        <h1 class="font-serif text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-main)]">
          Sharpen your English through intentional practice.
        </h1>

        <p class="text-sm text-[var(--text-muted)] leading-relaxed font-sans">
          Practice across listening, grammar, writing, and dictation—designed for clarity, confidence, and real-world communication.
        </p>
      </div>

      <!-- Quick stats overview -->
      <div class="p-5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] min-w-[280px] space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">
            Today's Progress
          </span>
          <span class="text-xs font-mono font-bold text-[var(--accent-primary)]">
            {dailyPercentage}%
          </span>
        </div>

        <!-- Progress bar -->
        <div class="w-full h-2 rounded-full bg-[var(--border-main)] overflow-hidden">
          <div 
            class="h-full bg-[var(--accent-primary)] rounded-full transition-all duration-500"
            style="width: {dailyPercentage}%"
          ></div>
        </div>

        <div class="grid grid-cols-2 gap-2 text-xs pt-1">
          <div>
            <span class="text-[var(--text-subtle)] block">Practiced</span>
            <span class="font-bold text-[var(--text-main)] font-mono">{minutesPracticed} / {targetMinutes} min</span>
          </div>
          <div>
            <span class="text-[var(--text-subtle)] block">Streak</span>
            <span class="font-bold text-amber-600 font-mono">{streakDays} days active</span>
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
              <span class="px-2 py-0.5 rounded text-[10px] font-mono text-[var(--text-subtle)] bg-[var(--bg-inner)] border border-[var(--border-main)]">
                {mod.duration}
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

  <!-- Highlighted Focus Session -->
  <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)] bg-[var(--bg-card)]">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div class="space-y-1.5">
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-[var(--accent-primary-light)] text-[var(--accent-primary)]">
            #5: Workplace Communication
          </span>
          <span class="text-xs text-[var(--text-muted)] font-serif italic">Recommended focus</span>
        </div>
        <h3 class="text-base font-bold font-serif text-[var(--text-main)]">
          Enhance clarity and professionalism in workplace conversations.
        </h3>
        <p class="text-xs text-[var(--text-muted)]">
          Practice phrasing requests, giving feedback, and structuring technical summaries.
        </p>
      </div>

      <button
        onclick={() => onSelectPracticeTab('writing')}
        class="px-4 py-2.5 rounded-xl btn-forest font-semibold text-xs flex items-center justify-center gap-1.5 shrink-0 shadow-sm"
      >
        <span>Continue Focus Session</span>
        <ArrowRight class="w-3.5 h-3.5" />
      </button>
    </div>
  </section>

  <!-- Recent Practice History -->
  <section class="journal-card p-5 sm:p-6 border border-[var(--border-main)]">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <History class="w-4 h-4 text-[var(--accent-primary)]" />
        <h2 class="text-base font-semibold text-[var(--text-main)]">Recent Practice</h2>
      </div>
      <span class="text-xs text-[var(--text-muted)] font-mono">View All History &rarr;</span>
    </div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {#each recentPractice as item}
        <button
          onclick={() => onSelectPracticeTab(item.tab)}
          class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] hover:border-[var(--accent-primary)] text-left transition cursor-pointer group"
        >
          <div class="flex items-center justify-between text-[11px]">
            <span class="font-bold text-[var(--accent-primary)]">{item.type}</span>
            <span class="font-mono text-[var(--text-subtle)]">{item.time}</span>
          </div>
          <p class="text-xs font-semibold text-[var(--text-main)] mt-2 line-clamp-1 group-hover:text-[var(--accent-primary)] transition">
            {item.topic}
          </p>
          <div class="mt-2 flex items-center gap-1 text-[10px] text-[var(--text-muted)]">
            <span class="px-1.5 py-0.5 rounded bg-[var(--bg-card)] border border-[var(--border-main)]">{item.level}</span>
            <span>Completed</span>
          </div>
        </button>
      {/each}
    </div>
  </section>

  <!-- Vault Connected Footer Info -->
  <footer class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[var(--text-muted)]">
    <div class="flex items-center gap-2">
      <ShieldCheck class="w-4 h-4 text-emerald-600" />
      <span>Vault connected</span>
      <span class="text-[var(--text-subtle)] font-mono">Last sync: Today, 10:24 AM</span>
    </div>

    <div class="font-serif italic text-center sm:text-right">
      “Language is the architecture of thought.” — Joseph Joubert
    </div>
  </footer>
</div>
