# 🦄 VaultLingo

> **VaultLingo** is a lightweight, cross-platform desktop application designed specifically for **daily English vocabulary mastery and spaced repetition retention**, with direct **Obsidian Vault** synchronization.
>
> 🤖 **Built 100% with AI:** This entire project—from system architecture, Go backend, Svelte 5 frontend, database queries, to visual assets—was conceived, designed, and developed entirely by **AI (Google Antigravity / Gemini)**.

---

## ✨ Key Features

- 📚 **Vocabulary & Spaced Repetition (SRS SM-2):** Daily 5-word sets across curated topics (Destination B1/B2, Tech & Embedded, Workplace, Science/AI), 3D flipping flashcards with keyboard shortcuts, Cambridge Dictionary integration, Daily Idioms, and 10s Quick Quizzes.
- 🎧 **Interactive Dictation Practice:** Audio playback with normal (1.0x) and slow (0.75x) speeds, keyword hints, and a real-time **LCS Visual Diff Engine** (highlighting correct, wrong, and missing words with accuracy scores).
- 🗣️ **75 Topics Listening:** Real-world conversational Q&A streams with active listening mode (blur/reveal answers).
- ✍️ **AI Writing Coach:** Micro-scenario writing prompts, live stopwatch & word counter, and instant grammar, tone, and vocabulary evaluation powered by **Antigravity (agy CLI)**, **OpenRouter (Free Tier)**, **Groq (Free & Fast)**, or **Local Ollama**.
- 🗄️ **Obsidian Vault 2-Way Sync:** Automatically saves vocabulary cards and essays to Markdown files with hidden SRS metadata tags (`<!-- srs: ... -->`) and updates review intervals directly in your Vault.
- ☀️ / 🌙 **Day & Night Themes:** Instant reactive theme switcher between deep midnight glassmorphism and clean light mode.

---

## 🔒 Security & API Token Privacy Disclaimer

VaultLingo is built with a **Local-First, Zero-Telemetry** architecture to ensure complete control over your private API keys and study data:

- **100% Local Storage:** All API keys and configurations are stored strictly on your local computer at `~/.config/VaultLingo/config.json`.
- **Zero Intermediary Servers:** VaultLingo has **no** proprietary cloud backends or analytics services. API calls are sent *directly* from your local device to the official provider endpoint via encrypted HTTPS.
- **Antigravity Native Integration:** Uses the local system-authenticated `agy` CLI with dynamic model support without requiring external API keys.
- **Offline Mode:** If you prefer zero network exposure, you can use **Local Ollama** to run LLMs completely offline on your own hardware.
- **Revocation & Deletion:** You can modify, delete, or revoke your tokens at any time directly through the Settings interface or by removing `~/.config/VaultLingo/config.json`.

---

## 🛠️ Tech Stack

- **Backend:** Go (Wails v2) + Pure-Go SQLite (`modernc.org/sqlite`) + Native OS Audio (`mpv` / `afplay`)
- **Frontend:** Svelte 5 (Runes) + Vite 7 + TailwindCSS + `@lucide/svelte`
- **AI Integrations:**
  - 🛸 **Antigravity (agy CLI):** Native system AI integration with dynamic model support (Gemini 3.7 Flash, Gemini 3.0 Flash, auto)
  - 🌐 **OpenRouter:** Free models (`meta-llama/llama-3.3-70b-instruct:free`, `google/gemini-2.0-flash-exp:free`, `deepseek/deepseek-chat:free`)
  - ⚡ **Groq:** Ultra-fast free tier (`llama-3.3-70b-versatile`, `mixtral-8x7b-32768`)
  - 🦙 **Local Ollama:** 100% private, local and offline execution

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
