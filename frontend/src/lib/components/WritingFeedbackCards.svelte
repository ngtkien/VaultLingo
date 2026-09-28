<script lang="ts">
  import {
    Sparkles,
    AlertCircle,
    CheckCircle2,
    ArrowRight,
    Copy,
    Check,
    Briefcase,
    MessageSquare,
    BookOpen
  } from 'lucide-svelte';
  import type { AiFeedbackData } from '../utils/writingFeedbackParser';

  let {
    feedback,
    onApplyAlternative,
    applyLabel = "Use in Editor"
  } = $props<{
    feedback: AiFeedbackData;
    onApplyAlternative?: (text: string) => void;
    applyLabel?: string;
  }>();

  let copiedIndex = $state<number | null>(null);

  async function copyText(text: string, index: number) {
    try {
      await navigator.clipboard.writeText(text);
      copiedIndex = index;
      setTimeout(() => {
        if (copiedIndex === index) copiedIndex = null;
      }, 2000);
    } catch (e) {
      console.error(e);
    }
  }
</script>

<div class="space-y-4">
  <!-- Score & Overall Banner -->
  <div class="p-5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="px-4 py-3 rounded-2xl border border-[var(--border-main)] bg-[var(--bg-card)] flex flex-col items-center justify-center shrink-0">
        <span class="text-2xl font-black text-[var(--accent-primary)] font-mono">{feedback.score}</span>
        <span class="text-[10px] font-bold uppercase text-[var(--text-subtle)]">/ 10</span>
      </div>

      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span class="journal-badge text-[var(--text-subtle)]">Assessment</span>
          <span class="text-xs font-bold text-[var(--accent-primary)]">
            {feedback.scoreLabel}
          </span>
        </div>
        <p class="text-sm text-[var(--text-main)] font-serif italic leading-relaxed">
          {feedback.overallFeedback}
        </p>
      </div>
    </div>

    {#if feedback.promptAlignment}
      <div class="px-3 py-2 rounded-xl bg-[var(--bg-card)] border border-[var(--border-main)] text-[11px] text-[var(--text-muted)] shrink-0 self-start sm:self-center">
        <span class="font-bold text-[var(--accent-primary)] block">🎯 Prompt Adherence:</span>
        <span>{feedback.promptAlignment}</span>
      </div>
    {/if}
  </div>

  <!-- Grammar & Spelling Corrections -->
  <div class="space-y-2.5">
    <div class="flex items-center justify-between text-xs font-bold text-[var(--text-main)]">
      <span class="flex items-center gap-1.5 text-red-600">
        <AlertCircle class="w-4 h-4" />
        <span>Grammar & Spelling Corrections ({feedback.corrections.length})</span>
      </span>
    </div>

    {#if feedback.corrections.length === 0}
      <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 text-xs flex items-center gap-2">
        <CheckCircle2 class="w-4 h-4 text-emerald-600 shrink-0" />
        <span>Excellent work! No significant grammatical errors detected in your response.</span>
      </div>
    {:else}
      <div class="grid gap-2.5">
        {#each feedback.corrections as item}
          <div class="p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2">
            <div class="flex flex-col sm:flex-row sm:items-center gap-2 text-xs">
              <div class="flex items-center gap-1.5 flex-1 bg-[var(--bg-card)] text-red-700 px-3 py-1.5 rounded-lg border border-red-500/30 font-medium">
                <span class="text-red-600 font-bold">❌ Original:</span>
                <span class="line-through">{item.original}</span>
              </div>

              <ArrowRight class="w-3.5 h-3.5 text-[var(--text-subtle)] shrink-0 hidden sm:block" />

              <div class="flex items-center gap-1.5 flex-1 bg-[var(--bg-card)] text-emerald-700 px-3 py-1.5 rounded-lg border border-emerald-500/30 font-semibold">
                <span class="text-emerald-600 font-bold">✅ Fix:</span>
                <span>{item.correction}</span>
              </div>
            </div>

            {#if item.reason || item.category}
              <div class="text-[11px] text-[var(--text-muted)] pl-1 flex items-start gap-1">
                <span>💡</span>
                <span>
                  {#if item.category}
                    <span class="px-1.5 py-0.5 rounded bg-[var(--bg-card)] border border-[var(--border-main)] font-mono uppercase text-[9px] text-[var(--text-subtle)] mr-1">{item.category}</span>
                  {/if}
                  {item.reason}
                </span>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    {/if}
  </div>

  <!-- Native Phrasing Alternatives -->
  {#if feedback.alternatives.length > 0}
    <div class="space-y-2.5 pt-1">
      <span class="flex items-center gap-1.5 text-xs font-bold text-[var(--text-main)]">
        <Sparkles class="w-4 h-4 text-[var(--accent-primary)]" />
        <span>Native Phrasing Alternatives</span>
      </span>

      <div class="grid gap-3">
        {#each feedback.alternatives as alt, idx}
          <div class="p-4 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-[var(--accent-primary)] flex items-center gap-1.5 bg-[var(--bg-card)] px-2.5 py-1 rounded-lg border border-[var(--border-main)]">
                {#if alt.style.toLowerCase().includes('prof') || alt.style.toLowerCase().includes('form')}
                  <Briefcase class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                {:else}
                  <MessageSquare class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                {/if}
                <span>{alt.style}</span>
              </span>

              <div class="flex items-center gap-1.5">
                <button
                  onclick={() => copyText(alt.text, idx)}
                  class="px-2.5 py-1 rounded-lg bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] text-[11px] font-medium flex items-center gap-1 transition cursor-pointer border border-[var(--border-main)]"
                  title="Copy sentence"
                >
                  {#if copiedIndex === idx}
                    <Check class="w-3 h-3 text-emerald-600" />
                    <span class="text-emerald-600">Copied</span>
                  {:else}
                    <Copy class="w-3 h-3" />
                    <span>Copy</span>
                  {/if}
                </button>

                {#if onApplyAlternative}
                  <button
                    onclick={() => onApplyAlternative(alt.text)}
                    class="px-2.5 py-1 rounded-lg bg-[var(--accent-primary-light)] text-[var(--accent-primary)] border border-[var(--accent-primary-border)] text-[11px] font-semibold flex items-center gap-1 transition cursor-pointer"
                  >
                    <span>{applyLabel}</span>
                  </button>
                {/if}
              </div>
            </div>

            <p class="text-sm font-serif italic text-[var(--text-main)] leading-relaxed pl-1">
              “{alt.text}”
            </p>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Vocabulary Highlights -->
  {#if feedback.vocabularyHighlights.length > 0}
    <div class="space-y-2 pt-1">
      <span class="text-xs font-bold text-[var(--text-main)] flex items-center gap-1.5">
        <BookOpen class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
        <span>Vocabulary & Collocation Highlights:</span>
      </span>

      <div class="grid sm:grid-cols-2 gap-2">
        {#each feedback.vocabularyHighlights as v}
          <div class="p-3 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] flex items-start gap-2 text-xs">
            <span class="font-bold text-[var(--accent-primary)] font-mono shrink-0 bg-[var(--bg-card)] px-2 py-0.5 rounded border border-[var(--border-main)]">
              {v.term}
            </span>
            <span class="text-[var(--text-muted)] text-[11px] leading-relaxed mt-0.5">
              {v.meaning}
            </span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>
