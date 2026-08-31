# 🦄 VaultLingo

> **VaultLingo** is a lightweight, high-performance, cross-platform English language mastery suite and lexicon engine with direct **Obsidian Vault** synchronization.

---

## ✨ Key Features

- 📚 **Vocabulary & Spaced Repetition (SRS SM-2):** Daily 5-word sets across curated topics (Destination B1/B2, Tech & Embedded, Workplace, Science/AI), 3D flipping flashcards with keyboard shortcuts, Cambridge Dictionary integration, Daily Idioms, and Quick Quizzes.
- ⚡ **Zero-Bloat CLI Tool (`vl`):** Standalone, ultra-fast (< 5ms) terminal dictionary with 6-block Oxford linguistic analysis and automatic AI synthesis fallback.
- 🎧 **Interactive Dictation Practice:** Audio playback with normal (1.0x) and slow (0.75x) speeds, keyword hints, and a real-time **LCS Visual Diff Engine** (highlighting correct, wrong, and missing words).
- 🗣️ **Conversational Listening Practice:** Real-world Q&A streams loaded dynamically from SQLite with active listening mode (blur/reveal answers).
- ✍️ **AI Writing Coach (v0.1.3 Visual Feedback):** Micro-scenario writing prompts, live stopwatch & word counter, and structured before/after grammar correction cards powered by **OpenCode**, **Antigravity (agy CLI)**, **OpenRouter**, **Groq**, or **Local Ollama**.
- 🗄️ **Obsidian Vault 2-Way Sync:** Automatically saves vocabulary cards and essays to Markdown files with hidden SRS metadata tags (`<!-- srs: ... -->`) and updates review intervals directly in your Vault.
- ☀️ / 🌙 **Day & Night Themes:** Instant reactive theme switcher between deep midnight glassmorphism and clean light mode.

---

## ⚡ VaultLingo CLI (`vl`)

VaultLingo includes a standalone command-line dictionary tool `vl` that runs in **0ms** using the embedded SQLite database:

```bash
# Instant 0ms dictionary lookup with full 6-block Oxford linguistic data
vl compare
vl collaborate
vl serendipity

# Autocomplete & search word suggestions
vl -s arch
vl -s comp

# Output structured data as raw JSON (ideal for scripts & jq)
vl compare --json

# Lookup word and automatically sync flashcard note to Obsidian Vault
vl compare -o
```

---

## 🤖 Supported AI Providers

VaultLingo supports a wide range of local and cloud AI providers with zero lock-in:

1. 🤖 **OpenCode CLI:** Local, free CLI-based AI agent (`/usr/bin/opencode`).
2. 🛸 **Antigravity CLI (`agy`):** Native system-authenticated Google Deepmind agent CLI with dynamic model support (e.g., `gemini-3.7-flash`).
3. 🌐 **OpenRouter:** Free and open-source models (`meta-llama/llama-3.3-70b-instruct:free`, `deepseek/deepseek-chat:free`).
4. ⚡ **Groq:** Ultra-fast free cloud tier (`llama-3.3-70b-versatile`, `mixtral-8x7b-32768`).
5. 🦙 **Local Ollama:** 100% private, offline LLM execution on your own hardware (`http://localhost:11434`).

---

## 🔒 Security & Privacy

- **100% Local Storage:** All configurations are stored locally at `~/.config/VaultLingo/config.json`.
- **Zero Intermediary Servers:** No telemetry or third-party tracking servers.
- **Embedded Database (`//go:embed`):** Fully functional offline out-of-the-box.

---

## 🛠️ Installation & Building

### Quick Install (Linux / macOS Release Bundle)
Download the latest `vaultlingo-linux-amd64.tar.gz` from GitHub Releases:
```bash
tar -xzvf vaultlingo-linux-amd64.tar.gz
cd vaultlingo-linux-amd64
sudo ./install.sh
```

### Run in Development (Live Reload)
```bash
# Start desktop app in dev mode:
wails dev

# Run Backend Go Unit Tests:
go test -v ./backend/...

# Run Frontend Vitest Suite & Diagnostics:
cd frontend
npm test
npm run check
```

### Build Production Binaries
```bash
# Build desktop app + CLI binary:
bash scripts/package_release.sh
```

---

## 📄 License
MIT License. Created by Zeder.
