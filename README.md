# 🦄 VaultLingo

> **VaultLingo** is an elegant, lightweight, and high-performance English language mastery suite and lexicon engine with an **Editorial Journal design** and direct **Obsidian Vault 2-way synchronization**.

---

## ✨ Key Features

- 🌿 **Editorial Journal Aesthetic:** A quiet, paper-like reading and study surface designed for deep focus. Features warm parchment tones, classic typography (*Newsreader* serif & *Plus Jakarta Sans*), deep pine accents, and responsive micro-animations.
- 📚 **Vocabulary & Learn Hub:**
  - **11 Curated Topics:** Destination B1 & B2, Tech & Embedded Electronics, Workplace & Career, Daily Life, Science & AI, Travel & Culture, Health & Wellness, and Due SRS reviews.
  - **Smart Session Persistence & Lock:** Words remain securely pinned across tab navigation until you explicitly click **Refresh** (🔄) or select another topic.
  - **Optimized Topic Filter:** Smooth horizontal scrolling with desktop navigation chevrons, mouse wheel support, and zero duplicate pills.
  - **Interactive 3D Flashcards:** Flip with `Space`/`Enter` and navigate with `ArrowLeft`/`ArrowRight`.
- ⚡ **Interactive Practice Drills (`WordPracticeModal`):**
  - 5 active-recall workout modes for any word: **Meaning Recall**, **Contextual Cloze**, **Part of Speech**, **Audio Spelling**, and **Sentence Construction**.
  - Live mastery scoring, pronunciation replay, and instant 1-click sync to Obsidian.
- 📖 **Smart Oxford 6-Block Dictionary:**
  - Instant SQLite lookup (< 5ms) with live autocomplete.
  - **Deep AI Lexical Enrichment:** Generates phonetic IPA, bilingual definitions, collocations, synonyms/antonyms, word families, morphological etymology roots, vivid mnemonic memory hooks, and usage nuance traps.
  - Direct Cambridge Dictionary external browser integration.
- 🌐 **AI Paragraph Translator (Bilingual EN ⇄ VI):**
  - Translate long-form paragraphs, articles, or essays with tone styling (*Formal, Casual, Academic, Professional, Conversational*).
  - Automatically extracts key advanced vocabulary & idioms with 1-click saving directly to SQLite and Obsidian notes.
- 🎧 **Interactive Dictation Gym:**
  - Normal (1.0x) and slow (0.75x) pronunciation speeds.
  - CEFR level filtering (**A2, B1, B2, All**) and topic queues.
  - Real-time **LCS Visual Diff Engine** highlighting exact correct, incorrect, and missing words.
- 🗣️ **Conversational Listening Practice:**
  - Real-world dialogue listening streams with dual display modes: **Dialogue View** (with speaker turns & blur/reveal responses) and **Full Continuous Script View**.
  - Single-toggle Show/Hide transcript control.
- 📐 **Grammar & Question Gym:**
  - Complete cheatsheet for all **12 English Verb Tenses** (formula, QUASM question patterns, signal keywords, and audio playback).
  - **5 Question Mindsets** with practical triggers.
  - Interactive tense transformation and question formation drills.
- ✍️ **AI Writing Coach:**
  - Micro-scenario prompts across difficulty levels, live stopwatch & word counter, and structured before/after grammar correction cards.
- 🔊 **Multi-Engine Neural TTS:**
  - **Microsoft Edge TTS:** High-fidelity cloud neural voices (*Jenny, Guy, Sonia, Ryan, etc.*).
  - **Piper TTS:** 100% offline, local neural voice synthesis with zero cloud latency.
- 🗄️ **Obsidian Vault 2-Way Sync:**
  - Saves vocabulary cards, translations, and writing essays to Markdown notes with hidden SRS metadata tags (`<!-- srs: ... -->`) and updates review intervals directly in your Vault.
- ⚡ **Zero-Bloat CLI Tool (`vl`):** Standalone, ultra-fast terminal dictionary with instant embedded database lookup.

---

## 🎨 Design & Theme Palettes

VaultLingo features an editorial design language with **8 curated theme palettes** and instant **Day / Night Journal modes**:

| Palette | Aesthetic | Key Tones |
| :--- | :--- | :--- |
| 🌿 **Editorial Journal** *(Default)* | Classic journal parchment with deep pine accents | `#fcf9f4` / `#386848` |
| 🌌 **Midnight Slate** | Deep space obsidian glassmorphism | `#0f172a` / `#38bdf8` |
| ❄️ **Nord Frost** | Arctic ice & cool twilight blue | `#2e3440` / `#88c0d0` |
| 🌲 **Everforest** | Serene woodland moss & warm cedar | `#2d353b` / `#a7c080` |
| 🌸 **Catppuccin Mocha** | Soothing pastel violet & lavender | `#1e1e2e` / `#cba6f7` |
| 🌃 **Tokyo Night** | Neon cyberpunk midnight indigo | `#1a1b26` / `#7aa2f7` |
| 🪵 **Gruvbox Retro** | Warm vintage terracotta & cream | `#282828` / `#fe8019` |
| 🧛 **Dracula** | Gothic purple & electric neon pink | `#282a36` / `#bd93f9` |

> 💡 Toggle between **Light Journal** and **Dark Journal** at any time via the Moon/Sun icon in the navigation bar.

---

## ⚡ VaultLingo CLI (`vl`)

VaultLingo includes a standalone command-line dictionary tool `vl` that runs in **0ms** using the embedded SQLite database:

```bash
# Instant dictionary lookup with full 6-block Oxford linguistic data
vl compare
vl collaborate
vl resilience

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
2. 🛸 **Antigravity CLI (`agy`):** Native system-authenticated Google Deepmind agent CLI with dynamic model support (e.g., `gemini-2.5-flash`).
3. 🌐 **OpenRouter:** Free and open-source models (`meta-llama/llama-3.3-70b-instruct:free`, `deepseek/deepseek-chat:free`).
4. ⚡ **Groq:** Ultra-fast cloud tier (`llama-3.3-70b-versatile`, `mixtral-8x7b-32768`).
5. 🦙 **Local Ollama:** 100% private, offline LLM execution on your own hardware (`http://localhost:11434`).

---

## 🛠️ Wails Setup & Development Prerequisites

VaultLingo is built with **Go + Svelte 5 + Tailwind CSS v4** powered by **Wails v2**.

### 1. System Dependencies

#### 🐧 Ubuntu / Debian / Linux Mint:
```bash
sudo apt update
sudo apt install -y build-essential pkg-config libgtk-3-dev libwebkit2gtk-4.1-dev \
                    golang nodejs npm
# If libwebkit2gtk-4.1-dev is unavailable on older Ubuntu versions, use:
# sudo apt install -y libwebkit2gtk-4.0-dev
```

#### 🏹 Arch Linux / Manjaro:
```bash
sudo pacman -S --needed base-devel gtk3 webkit2gtk-4.1 pkgconf go nodejs npm
```

#### 🎩 Fedora:
```bash
sudo dnf install gtk3-devel webkit2gtk4.1-devel pkg-config golang nodejs npm
```

#### 🍏 macOS:
```bash
xcode-select --install
brew install go node
```

---

### 2. Install Wails v2 CLI

Install the official Wails CLI using Go:

```bash
go install github.com/wailsapp/wails/v2/cmd/wails@latest
```

Ensure your Go bin directory is in your shell `$PATH`:
```bash
# Add to ~/.bashrc or ~/.zshrc if not already present:
export PATH="$HOME/go/bin:$PATH"

# Apply changes:
source ~/.bashrc  # or source ~/.zshrc
```

Verify your Wails setup:
```bash
wails doctor
```

---

### 3. Run in Development (Live Reload)

```bash
# Clone the repository
git clone https://github.com/ngtkien/VaultLingo.git
cd VaultLingo

# Install frontend dependencies
cd frontend && npm install && cd ..

# Start desktop app with hot reload
wails dev
```

### 4. Running Automated Tests

```bash
# Run Backend Go Unit Tests
go test -v ./backend/...

# Run Frontend Vitest & Diagnostics
cd frontend
npm test
npm run check
npm run build
cd ..
```

---

## 📦 Installation & Packaging

### 1. Arch Linux / Manjaro (AUR / yay)

```bash
# Recommended: Pre-compiled binary package
yay -S vaultlingo-bin

# Or build from source via AUR:
yay -S vaultlingo
```

---

### 2. Debian / Ubuntu / Linux Mint (`.deb`)

Download the latest `.deb` package from [GitHub Releases](https://github.com/ngtkien/VaultLingo/releases):

```bash
# Install with apt (automatically handles dependencies):
sudo apt install ./vaultlingo_0.1.8_amd64.deb

# Or with dpkg:
sudo dpkg -i vaultlingo_0.1.8_amd64.deb
sudo apt-get install -f
```

---

### 3. Universal Linux Release Bundle (`.tar.gz`)

Download the release archive from [GitHub Releases](https://github.com/ngtkien/VaultLingo/releases):

```bash
tar -xzvf vaultlingo-v0.1.8-linux-x86_64.tar.gz
cd vaultlingo-v0.1.8-linux-x86_64
sudo ./install.sh
```

---

### 4. Build All Packages Locally

```bash
# Build desktop app, CLI, .deb, and release bundles:
bash scripts/package_release.sh

# Or build Debian package only:
bash scripts/package_deb.sh

# Or update AUR PKGBUILD and .SRCINFO:
bash scripts/package_aur.sh
```

---

## 🔒 Security & Privacy

- **100% Local Storage:** All user configurations are stored locally at `~/.config/VaultLingo/config.json`.
- **Zero Intermediary Servers:** All requests connect directly to your configured AI/TTS providers.
- **Embedded Database (`//go:embed`):** 2,700+ vocabulary words, dictations, idioms, and topics work 100% offline out-of-the-box.

---

## 📄 License

MIT License. Created by [Zeder](https://github.com/ngtkien).
