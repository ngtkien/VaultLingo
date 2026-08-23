# VaultLingo Source Code Layout & Module Reference

This document outlines the directory structure, file-by-file responsibilities, and coding conventions across the VaultLingo repository.

---

## 1. Annotated Repository Tree (ASCII)

```
VaultLingo/
├── architecture/                         # Architecture diagrams & technical design
│   ├── SYSTEM_DESIGN.md                  # High-level architecture, sub-systems & flows
│   └── SOURCE_TREE.md                    # Detailed directory layout & file references
│
├── app.go                                # Wails application struct & IPC binding handlers
├── main.go                               # Desktop entrypoint, WebKit options, window config
├── go.mod / go.sum                       # Go dependencies (modernc.org/sqlite, wails v2)
├── wails.json                            # Wails build configuration & platform tags
│
├── backend/                              # Go Core Engine
│   ├── models.go                         # Data structures (Word, Dictation, Quiz, Config, etc.)
│   ├── db.go                             # Pure-Go SQLite connection & table initializers
│   ├── vocab_service.go                  # Vocab queries, SM-2 SRS math, Idioms, Quizzes
│   ├── dictation_service.go              # Sentence fetching & LCS-based diff calculation
│   ├── writing_service.go                # Gemini 2.5 Flash / Ollama writing evaluation client
│   ├── obsidian_service.go               # Obsidian markdown parser, SRS tag injector & URI open
│   ├── config_service.go                 # Local settings store (~/.config/VaultLingo/config.json)
│   └── audio_service.go                  # Native OS audio streaming via mpv / afplay
│
├── data/
│   └── vocab.db                          # Embedded SQLite database (B1, B2, Tech, Dictations)
│
├── build/                                # Application icons & packaging assets
│   ├── appicon.png                       # Cute Anime Pegasus mascot app icon
│   ├── darwin/                           # macOS plist templates
│   └── windows/                          # Windows icon & NSIS installer scripts
│
└── frontend/                             # Svelte 5 + Vite 7 Frontend Presentation
    ├── package.json                      # Frontend dependencies (@lucide/svelte, tailwindcss)
    ├── vite.config.ts                    # Vite build configuration with Tailwind plugin
    ├── svelte.config.js                  # Svelte 5 compiler preprocessors
    ├── tsconfig.json                     # TypeScript strict configuration
    ├── index.html                        # Application HTML shell
    │
    ├── src/
    │   ├── main.ts                       # Svelte 5 mount(App, { target }) entrypoint
    │   ├── App.svelte                    # Root container, layout & active tab state
    │   ├── style.css                     # TailwindCSS imports & Dark/Light CSS variables
    │   │
    │   ├── assets/
    │   │   └── images/
    │   │       └── pegasus-logo.png      # High-res Anime Pegasus mascot artwork
    │   │
    │   ├── lib/
    │   │   ├── components/
    │   │   │   └── Navbar.svelte         # Header, brand mascot, tabs, Day/Night toggle
    │   │   │
    │   │   ├── tabs/
    │   │   │   ├── VocabTab.svelte       # 5 Daily Words, 3D Flashcard, SRS, Quiz & Idiom
    │   │   │   ├── DictationTab.svelte   # Audio player, keyword hints, LCS Diff visualizer
    │   │   │   ├── ListeningTab.svelte   # 75 Topics Q&A, active listening blur mode
    │   │   │   ├── WritingTab.svelte     # Scenario writing, stopwatch, AI coach & lock overlay
    │   │   │   ├── ObsidianTab.svelte    # Vault scanner, due word filter, 2-way SRS review
    │   │   │   └── SettingsTab.svelte    # Vault path, Gemini API Key, Ollama, audio speed
    │   │   │
    │   │   └── utils/
    │   │       ├── audio.ts              # Frontend bridge to Go native audio engine
    │   │       └── theme.ts              # Day / Night mode local storage & DOM class manager
    │   │
    │   └── wailsjs/                      # Auto-generated TypeScript Wails IPC bindings
    │       ├── go/main/App.d.ts          # Strongly typed Go method signatures
    │       └── go/models.ts              # Strongly typed backend struct interfaces
```

---

## 2. Component Responsibility Matrix

| Layer | File | Core Responsibility |
| :--- | :--- | :--- |
| **App Lifecycle** | `main.go` | Sets up Wayland/NVIDIA flags, window dimensions (1024x768), and launches Wails. |
| **IPC Bridge** | `app.go` | Maps Go backend services to frontend callable asynchronous Promise methods. |
| **Database** | `backend/db.go` | Pure-Go SQLite engine. Copies bundled `vocab.db` to user local share on first run. |
| **Vocab & SRS** | `backend/vocab_service.go` | Queries words by topic, runs SuperMemo-2 (SM-2) algorithm calculation. |
| **Dictation** | `backend/dictation_service.go` | Calculates Longest Common Subsequence (LCS) word differences and accuracy %. |
| **AI Coach** | `backend/writing_service.go` | Connects to Google Gemini 2.5 Flash API or local Ollama REST endpoints. |
| **Obsidian** | `backend/obsidian_service.go` | Formats Markdown with YAML header and `<!-- srs: ... -->` hidden comment tags. |
| **Audio Engine**| `backend/audio_service.go` | Controls system native audio player (`mpv` on Linux / `afplay` on macOS). |
| **UI Components**| `frontend/src/lib/tabs/*` | Svelte 5 components with fine-grained `$state`, `$derived`, and reactive signals. |

---

## 3. Build & Packaging Commands

```bash
# Live development with hot-reloading:
wails dev

# Build standalone production executable on Linux:
wails build

# Build standalone macOS Universal Binary (.app / .dmg):
wails build -platform darwin/universal
```
