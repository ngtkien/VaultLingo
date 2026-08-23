# 🦄 VaultLingo

> **VaultLingo** is a lightweight, cross-platform desktop application designed specifically for **daily English vocabulary mastery and spaced repetition retention**, with direct **Obsidian Vault** synchronization.
>
> 🤖 **Built with AI:** This entire project was conceived, designed, and developed entirely by **AI (Google Antigravity / Gemini)**.

---

## ✨ Key Features

- 📚 **Vocabulary & Spaced Repetition (SRS SM-2):** Daily 5-word sets across curated topics (Destination B1/B2, Tech & Embedded, Workplace, Science/AI), 3D flipping flashcards with keyboard shortcuts, Cambridge Dictionary integration, Daily Idioms, and 10s Quick Quizzes.
- 🎧 **Interactive Dictation Practice:** Audio playback with normal (1.0x) and slow (0.75x) speeds, keyword hints, and a real-time **LCS Visual Diff Engine** (highlighting correct, wrong, and missing words with accuracy scores).
- 🗣️ **75 Topics Listening:** Real-world conversational Q&A streams with active listening mode (blur/reveal answers).
- ✍️ **AI Writing Coach:** Micro-scenario writing prompts, live stopwatch & word counter, and instant grammar, tone, and vocabulary evaluation powered by **Google Gemini 2.5 Flash** or **Local Ollama**.
- 🗄️ **Obsidian Vault 2-Way Sync:** Automatically saves vocabulary cards and essays to Markdown files with hidden SRS metadata tags (`<!-- srs: ... -->`) and updates review intervals directly in your Vault.
- ☀️ / 🌙 **Day & Night Themes:** Instant reactive theme switcher between deep midnight glassmorphism and clean light mode.

---

## 🛠️ Tech Stack

- **Backend:** Go (Wails v2) + Pure-Go SQLite (`modernc.org/sqlite`) + Native OS Audio (`mpv` / `afplay`)
- **Frontend:** Svelte 5 (Runes) + Vite 7 + TailwindCSS + `@lucide/svelte`
- **AI Integrations:** Google Gemini 2.5 Flash / Local Ollama (Offline)

---

## 🚀 Quick Start

### Prerequisites
- [Go](https://go.dev/) (>= 1.20)
- [Node.js](https://nodejs.org/) (>= 18)
- [Wails CLI v2](https://wails.io/): `go install github.com/wailsapp/wails/v2/cmd/wails@latest`
- `mpv` (for native audio streaming on Linux)

### Run in Development (Live Reload)
```bash
wails dev
```

### Build Production Binary
```bash
# Linux:
wails build

# macOS (Universal Binary):
wails build -platform darwin/universal
```

Binary output will be generated at: `build/bin/VaultLingo`

---

## 📐 Architecture & Engineering

Detailed ASCII system design diagrams and annotated source tree are available in the [architecture/](./architecture/) directory:
- [SYSTEM_DESIGN.md](./architecture/SYSTEM_DESIGN.md)
- [SOURCE_TREE.md](./architecture/SOURCE_TREE.md)

---

## 📄 License
MIT License. Created by Zeder.
