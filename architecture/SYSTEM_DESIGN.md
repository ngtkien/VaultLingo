# VaultLingo System Architecture & Technical Design

VaultLingo is a lightweight, cross-platform desktop application built with **Wails v2 (Go backend)** and **Svelte 5 (Frontend)**. It provides offline-capable vocabulary learning with Spaced Repetition (SM-2), interactive dictation with word-by-word diff checking, AI-assisted writing evaluation, and direct bi-directional synchronization with Obsidian Markdown Vaults.

---

## 1. High-Level Architecture (ASCII Overview)

```
===================================================================================
                               VAULTLINGO APPLICATION
===================================================================================

+----------------------------------------------------------------------------------+
|                        PRESENTATION LAYER (SVELTE 5 + TS)                        |
|                                                                                  |
|  [Navbar: Tabs & Day/Night Toggle]                                               |
|  +--------------------+---------------------+--------------------+-------------+ |
|  |   Vocabulary       |   Dictation         |   75 Topics        |   Writing   | |
|  |  - List / 3D Card  |  - Audio 1x / 0.75x |  - Q&A Stream      |  - AI Coach | |
|  |  - SRS SM-2 Rating |  - Visual Diff LCS  |  - Active Listen   |  - Lock     | |
|  +--------------------+---------------------+--------------------+-------------+ |
|  |   Obsidian Vault Explorer & SRS Sync   |   Settings (Vault, AI, Audio)  | |
|  +------------------------------------------+----------------------------------+ |
+--------------------------------------------------------------------------------- +
                                      |
                      [Wails v2 IPC Bridge / Bindings]
                      - TypeScript Promise RPC Callbacks
                      - Binary Message Passing (JSON / Memory)
                                      |
                                      v
+---------------------------------------------------------------------------------+
|                        CORE APPLICATION BACKEND (GO)                            |
|                                                                                 |
|  [app.go: Service Coordinator & Lifecycle Handler]                              |
|  +---------------------+---------------------+--------------------------------+ |
|  | vocab_service.go    | dictation_service.go| writing_service.go             | |
|  | - SM-2 SRS Algorithm| - LCS Diff Algorithm| - Gemini 2.5 Flash Client      | |
|  | - Quiz & Idiom Store| - Sentence Matcher  | - Ollama HTTP Rest Client      | |
|  +---------------------+---------------------+--------------------------------+ |
|  | obsidian_service.go | audio_service.go    | config_service.go              | |
|  | - Markdown Parser   | - mpv / Native Pipe | - JSON Config Store            | |
|  | - SRS Tag Injector  | - Speed controller  | - ~/.config/VaultLingo/        | |
|  +---------------------+---------------------+--------------------------------+ |
+---------------------------------------------------------------------------------+
         |                          |                           |
         v                          v                           v
+-------------------+      +-------------------+      +-------------------+
|  DATABASE STORAGE |      | OBSIDIAN VAULT MD |      |  AI LLM SERVICES  |
|                   |      |                   |      |                   |
| - Pure Go SQLite  |      | - English/Vocab/  |      | - Google Gemini   |
|   (modernc.org)   |      | - English/Writing |      | - Local Ollama    |
| - vocab.db        |      | - <!-- srs: ...-->|      | - Offline Fallback|
+-------------------+      +-------------------+      +-------------------+
```

---

## 2. Core Subsystems & Interaction Flows

### A. Vocabulary & Spaced Repetition (SM-2 Algorithm)
```
[User Rates Card] ───> [Wails: RecordSrsReview]
                              │
                              ▼
                 +--------------------------+
                 | SuperMemo-2 Engine       |
                 | - Grade: Again/Hard/Good |
                 | - Calc: Interval & EF    |
                 | - NextReview = Today + I |
                 +--------------------------+
                              │
               +──────────────┴──────────────+
               ▼                             ▼
       [Update SQLite]             [Update Obsidian MD]
       Table: srs_reviews          <!-- srs: {"next_review": ...} -->
```

### B. Dictation & Real-Time Diff Matching
```
[Target Sentence] ───+
                     │
                     v
       +----------------------------+
       | Tokenizer & Sanitizer      |
       | (Lowercase, Strip Punct)   |
       +----------------------------+
                     │
                     v
       +----------------------------+
       | Longest Common Subsequence |
       | (LCS Dynamic Programming)  |
       +----------------------------+
                     │
                     v
       +----------------------------+
       | Diff Token Generator       |
       | - Correct (🟩)             |
       | - Wrong / Extra (🟥)       |
       | - Missing (🟧)             |
       | - Accuracy % Score         |
       +----------------------------+
```

### C. Obsidian Vault Bi-Directional Synchronization
```
+---------------------------------------------------------------+
|                       VAULT SYNCHRONIZER                      |
+---------------------------------------------------------------+
                             |
         +-------------------+-------------------+
         |                                       |
         v                                       v
[Save Word / Essay]                     [Scan Vault on Startup]
 - Read configured Vault path            - Walk <Vault>/English/Vocab/
 - Ensure topic directory exists         - Parse Markdown frontmatter
 - Append / Write Markdown               - Extract <!-- srs: {...} -->
 - Inject hidden SRS comment             - Calculate "Due Today" count
 - Available for Obsidian Graph          - List in Obsidian Tab
```

### D. Native Audio Pipeline (Zero WebKit GStreamer Dependency)
```
[UI Trigger: Play Audio] ───> [audio.ts]
                                  │
                                  ▼
                      [Go: backend.PlayTTS / PlayAudioUrl]
                                  │
                                  ▼
               +-------------------------------------+
               | OS Native Player Process Controller |
               | - Linux: mpv --no-video --speed=... |
               | - macOS: afplay / mpv               |
               | - Direct ALSA / Pulse / PipeWire    |
               +-------------------------------------+
                                  │
                                  ▼
                     [Earphones / Desktop Speakers]
```

---

## 3. Security & Privacy Model
- **Local-First Storage:** All vocabulary data and study history remain 100% on your machine (`~/.local/share/VaultLingo/vocab.db` and your local Obsidian Vault).
- **API Token Safety:** Gemini API keys and Ollama endpoint configurations are stored strictly in local user configuration (`~/.config/VaultLingo/config.json`) and never transmitted to third-party telemetry servers.
- **Offline Capable:** Full vocabulary browsing, 3D flashcards, dictation diff checking, and local Ollama evaluations work completely offline.
