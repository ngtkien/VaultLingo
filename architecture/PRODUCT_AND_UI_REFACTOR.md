# Product & UI Refactor Blueprint

## Product decision

VaultLingo is an **offline-first daily English practice workspace**. Its value
is not a large collection of disconnected AI features; it is a dependable,
private learning loop that works without an account or cloud dependency.

The default experience should answer one question: **what is the most useful
thing to practise in the next 15–25 minutes?**

## Product principles

1. **Offline is the baseline.** SQLite data, SRS, dictation checking,
   packaged lessons, and local TTS must remain usable without a network.
2. **Cloud is opt-in enhancement.** Online dictionary lookup, Edge TTS, and
   AI enrichment must never block core study.
3. **Content quality before feature count.** Audio/transcript pairs must be
   exact; quizzes must not reveal answer-position patterns; each vocabulary
   entry needs a minimum quality contract.
4. **One clear daily loop.** Review -> learn -> practise -> finish.
5. **Calm and legible over decorative.** The interface should support focused
   study, not compete with the lesson for attention.

## Information architecture

Replace the dense eight-item primary navigation with four study-oriented
destinations:

```
Today       Learn              Practice                  Library
-----       -----              --------                  -------
Daily plan  Vocabulary          Dictation                 Saved words
Due reviews Dictionary          Listening                 Lesson packs
Streak      Idioms              Grammar                   Obsidian sync
            Quick quiz          Writing Lab (optional)    Search/history
```

Settings, appearance, audio providers, and AI providers belong in a secondary
menu. Obsidian is a Library capability, not a primary study destination.

## UI direction: “calm learning instrument”

The existing dark glassmorphism, gradients, badges, rounded cards and broad
theme palette are individually reasonable, but together create visual noise.
The current drawing mode is especially inconsistent: handwritten typography
and dotted paper imply informal note-taking, while the rest of the UI is a
precise, dense developer dashboard. It should be removed from the primary UI
and not receive further feature investment.

### Keep

- Dark and light modes; retain one well-tuned neutral palette as default.
- A single restrained accent color per learning state: blue for action, green
  for success, amber for attention, red only for errors.
- Clear typography, predictable spacing, keyboard operation, and small
  meaningful icons.
- One primary action per card: `Start review`, `Play`, `Check`, or `Continue`.

### Change

- Remove the drawing-mode toggle from the header. If preserved at all, move it
  to an experimental setting and do not let it change the UI font globally.
- Reduce palette choices from seven to one default plus optional system light/
  dark. Themes are customization, not a learning feature.
- Replace nested glass cards and repeated borders with one page surface and
  one card level. Avoid gradients except for a sparse progress/status cue.
- Remove decorative version badges and implementation labels from the study
  flow (for example “0ms”, “AI”, or provider names). Show those only in debug
  or Settings.
- On large screens use a content grid with a readable maximum line length;
  fullscreen should add useful columns or breathing room, never merely scale
  the same compact dashboard.
- On small screens use a compact header and horizontal navigation or a menu;
  do not squeeze all destinations and controls into one bar.

## Page templates

### Today (default route)

```
Good evening, Zeder                         18 min plan
-------------------------------------------------------
[ Continue: 5 reviews ]  [ 3 new words ]  [ 1 listening ]

Progress this week: 4 / 7 days       Streak: 4 days
```

Only one prominent CTA should appear: `Continue learning`.

### Practice session

```
< Back to Today              Dictation  2 of 8

                  [ large lesson surface ]
                 Play / Slow / Hint / Check

              Previous                 Next lesson
```

Practice should be distraction-free: hide global customization, unnecessary
statistics, and unrelated widgets while the learner is answering.

### Library

Use a utilitarian, searchable list. Counts, filters, CEFR tags, source, and
offline availability are valuable here; they are not needed in the practice
flow.

## Content and data requirements

- Vocabulary: target 5k–8k curated entries before broadening scope. Require
  POS, IPA/phonetic, English definition, Vietnamese meaning, and an example.
- Idioms: 100+ curated entries, deterministic daily rotation, and no duplicate
  local fallback bank that diverges from SQLite.
- Quiz: 250–400 questions; shuffle options server-side and validate that the
  correct-answer distribution is balanced over repeated deliveries.
- Dictation: 800–1,200 sentences across A2/B1/B2 and balanced categories.
- Listening: distinguish `TTS Practice` (packaged transcript is the audio
  source) from `Authentic Recording` (verified transcript + source/license).

## Engineering preparation before redesign

1. Add content versioning/migrations for existing installed SQLite databases.
   New embedded data must update a user's old database safely and idempotently.
2. Separate `content`, `study state`, `integrations`, and `appearance` from
   component UI code.
3. Create a small design-token layer: spacing, surface, border, text, accent,
   success, warning, error. Stop placing arbitrary color/shadow classes in
   every component.
4. Make UI components composable: `PageHeader`, `StudyCard`, `PrimaryButton`,
   `ProgressBar`, `EmptyState`, `LessonPlayer`, and `SessionShell`.
5. Add content integrity tests: no duplicate prompts, valid JSON, required
   fields, valid CEFR/category, and matching TTS transcript/audio mode.
6. Keep Wails bindings thin. Backend services own persistence and migrations;
   Svelte owns session state and rendering.

## Delivery order

**Phase 1 — reliability:** SQLite content migrations, content checks, audio /
transcript integrity, stable daily selection, SRS tests.

**Phase 2 — simplify navigation:** introduce Today, Learn, Practice, Library
without removing current capabilities. Keep old pages behind the new grouping.

**Phase 3 — visual system:** remove drawing mode from the primary interface,
reduce theme noise, implement tokens and shared page/session components.

**Phase 4 — guided habit:** daily plan, continue state, weekly progress,
goal-based content selection, and focus sessions.
