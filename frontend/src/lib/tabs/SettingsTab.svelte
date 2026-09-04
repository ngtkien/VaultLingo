<script lang="ts">
  import { onMount } from 'svelte';
  import { GetConfig, SaveConfig, GetSavedObsidianVocab, GetVoicesList, PlayTTS } from '../../../wailsjs/go/main/App.js';
  import { Save, Check, Folder, Key, Cpu, Volume2, ShieldCheck, Sparkles, ExternalLink, Zap, Lock, Info, Bot, Play, Radio, Mic } from 'lucide-svelte';

  let config = $state<any>({
    obsidian_vault_path: '',
    ai_provider: 'agy',
    agy_model: 'gemini-3.7-flash',
    agy_path: '',
    openrouter_api_key: '',
    openrouter_model: 'meta-llama/llama-3.3-70b-instruct:free',
    groq_api_key: '',
    groq_model: 'llama-3.3-70b-versatile',
    ollama_url: 'http://localhost:11434',
    ollama_model: 'llama3:latest',
    auto_play_audio: true,
    default_audio_speed: 1.0,
    tts_provider: 'edge',
    tts_voice: 'en-US-JennyNeural',
    piper_path: '',
    piper_model_path: ''
  });

  let voices = $state<any[]>([]);
  let savedMessage = $state(false);
  let saving = $state(false);
  let isTestingVoice = $state(false);

  const AGY_MODEL_PRESETS = [
    { id: 'gemini-3.7-flash', label: 'Gemini 3.7 Flash (Recommended)' },
    { id: 'gemini-3.0-flash', label: 'Gemini 3.0 Flash' },
    { id: 'auto', label: 'Auto (Current agy default)' },
  ];

  const OPENROUTER_FREE_MODELS = [
    { id: 'meta-llama/llama-3.3-70b-instruct:free', label: 'Llama 3.3 70B (Free)' },
    { id: 'google/gemini-2.0-flash-exp:free', label: 'Gemini 2.0 Flash (Free)' },
    { id: 'deepseek/deepseek-chat:free', label: 'DeepSeek Chat (Free)' },
    { id: 'qwen/qwen-2.5-72b-instruct:free', label: 'Qwen 2.5 72B (Free)' },
  ];

  async function loadConfig() {
    try {
      config = await GetConfig();
      if (!config.tts_provider) config.tts_provider = 'edge';
      if (!config.tts_voice) config.tts_voice = 'en-US-JennyNeural';
    } catch (e) {
      console.error(e);
    }
  }

  async function loadVoices() {
    try {
      const list = await GetVoicesList();
      if (list && list.length > 0) {
        voices = list;
      }
    } catch (e) {
      console.error('Failed to load voice list:', e);
    }
  }

  async function handleSave() {
    saving = true;
    try {
      await SaveConfig(config);
      savedMessage = true;
      setTimeout(() => {
        savedMessage = false;
      }, 3000);
    } catch (e) {
      console.error(e);
    } finally {
      saving = false;
    }
  }

  async function handleTestVoice() {
    if (isTestingVoice) return;
    isTestingVoice = true;
    try {
      await SaveConfig(config);

      let testSentence = '';
      if (config.tts_provider === 'piper') {
        testSentence = "Hello! This is local offline Piper Neural TTS running directly on your computer.";
      } else if (config.tts_provider === 'edge') {
        const currentVoice = voices.find(v => v.id === config.tts_voice);
        const voiceName = currentVoice ? currentVoice.name : 'Jenny';
        testSentence = `Hello! This is ${voiceName} powered by Microsoft Edge Neural AI.`;
      } else {
        testSentence = "Hello! This is standard Google Translate speech fallback.";
      }

      await PlayTTS(testSentence, config.default_audio_speed || 1.0);
    } catch (e) {
      console.error('Voice test error:', e);
    } finally {
      setTimeout(() => {
        isTestingVoice = false;
      }, 3500);
    }
  }

  async function handleExportBackup() {
    try {
      const items = await GetSavedObsidianVocab();
      const backupData = {
        app: 'VaultLingo',
        version: '0.1.7',
        export_date: new Date().toISOString(),
        config: {
          ai_provider: config.ai_provider,
          tts_provider: config.tts_provider,
          tts_voice: config.tts_voice,
          default_audio_speed: config.default_audio_speed
        },
        saved_vocabulary: items || []
      };
      const blob = new Blob([JSON.stringify(backupData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `vaultlingo-backup-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Backup error:', e);
    }
  }

  function handleFactoryReset() {
    if (confirm('Are you sure you want to restore all settings and cache to default values? This will not delete your Obsidian files.')) {
      localStorage.clear();
      config = {
        obsidian_vault_path: '',
        ai_provider: 'agy',
        agy_model: 'gemini-3.7-flash',
        agy_path: '',
        openrouter_api_key: '',
        openrouter_model: 'meta-llama/llama-3.3-70b-instruct:free',
        groq_api_key: '',
        groq_model: 'llama-3.3-70b-versatile',
        ollama_url: 'http://localhost:11434',
        ollama_model: 'llama3:latest',
        auto_play_audio: true,
        default_audio_speed: 1.0,
        tts_provider: 'edge',
        tts_voice: 'en-US-JennyNeural',
        piper_path: '',
        piper_model_path: ''
      };
      handleSave();
      window.location.reload();
    }
  }

  onMount(() => {
    loadConfig();
    loadVoices();
  });
</script>

<div class="w-full max-w-5xl mx-auto space-y-6 pb-12">
  <article class="journal-card p-6 sm:p-8 border border-[var(--border-main)] bg-[var(--bg-card)] space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[var(--border-main)] pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="journal-badge text-[var(--accent-primary)] bg-[var(--accent-primary-light)] px-2.5 py-0.5 rounded text-[10px]">
            Preferences
          </span>
        </div>
        <h1 class="font-serif text-2xl sm:text-3xl font-bold tracking-tight text-[var(--text-main)] mt-1">
          Settings & Preferences
        </h1>
        <p class="text-xs text-[var(--text-muted)] mt-0.5">
          Configure your Obsidian Vault path, AI provider, and Neural Speech Voices
        </p>
      </div>

      <button
        onclick={handleSave}
        disabled={saving}
        class="px-5 py-2.5 rounded-xl btn-forest text-xs font-bold flex items-center gap-2 transition cursor-pointer shadow-sm self-start sm:self-auto"
      >
        {#if savedMessage}
          <Check class="w-4 h-4 text-white" />
          <span>Saved Successfully!</span>
        {:else}
          <Save class="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Save Settings'}</span>
        {/if}
      </button>
    </div>

    <!-- Security & Privacy Disclaimer Card -->
    <div class="p-4.5 rounded-2xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-3">
      <div class="flex items-center gap-2 text-[var(--accent-primary)] font-bold text-sm">
        <ShieldCheck class="w-5 h-5" />
        <span>Security & Local Privacy</span>
      </div>

      <div class="grid sm:grid-cols-2 gap-3 text-xs text-[var(--text-muted)]">
        <div class="flex items-start gap-2 bg-[var(--bg-card)] p-3 rounded-xl border border-[var(--border-main)]">
          <Lock class="w-4 h-4 text-[var(--accent-primary)] shrink-0 mt-0.5" />
          <div>
            <strong class="text-[var(--text-main)] block">100% Local Storage</strong>
            Your configurations and keys are kept safely on your machine.
          </div>
        </div>

        <div class="flex items-start gap-2 bg-[var(--bg-card)] p-3 rounded-xl border border-[var(--border-main)]">
          <Info class="w-4 h-4 text-[var(--accent-primary)] shrink-0 mt-0.5" />
          <div>
            <strong class="text-[var(--text-main)] block">Direct Connections</strong>
            Requests run directly through your chosen provider or offline via local models.
          </div>
        </div>
      </div>
    </div>

    <!-- Speech & TTS Voice Engine -->
    <div class="space-y-4 border-t border-[var(--border-main)] pt-5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-sm font-bold text-[var(--text-main)]">
          <Volume2 class="w-4 h-4 text-[var(--accent-primary)]" />
          <span>Speech & TTS Voice Engine</span>
        </div>

        <button
          onclick={handleTestVoice}
          disabled={isTestingVoice}
          class="px-3 py-1.5 rounded-xl bg-[var(--bg-inner)] hover:bg-[var(--accent-primary-light)] text-[var(--text-muted)] hover:text-[var(--accent-primary)] border border-[var(--border-main)] text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer"
        >
          {#if isTestingVoice}
            <span class="animate-pulse flex items-center gap-1.5 text-[var(--accent-primary)]">
              <Radio class="w-3.5 h-3.5 animate-spin" />
              <span>Playing Sample...</span>
            </span>
          {:else}
            <Play class="w-3.5 h-3.5" />
            <span>Test Voice 🔊</span>
          {/if}
        </button>
      </div>

      <!-- TTS Provider Selector -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <!-- Edge Neural TTS -->
        <button
          onclick={() => config.tts_provider = 'edge'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.tts_provider === 'edge'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary-border)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">Edge Neural AI ⭐</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-[var(--accent-primary)]">Free AI</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">Ultra-natural US/UK human voices</div>
        </button>

        <!-- Piper TTS (Offline) -->
        <button
          onclick={() => config.tts_provider = 'piper'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.tts_provider === 'piper'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary-border)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">Piper TTS 🦙</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-emerald-700">Offline</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">100% on-device neural model</div>
        </button>

        <!-- Google Translate TTS (Legacy) -->
        <button
          onclick={() => config.tts_provider = 'google'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.tts_provider === 'google'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary-border)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">Google TTS 🤖</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-[var(--text-subtle)]">Basic</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">Standard fallback voice</div>
        </button>
      </div>

      <!-- Edge TTS Voice Selector Grid -->
      {#if config.tts_provider === 'edge'}
        <div class="bg-[var(--bg-inner)] p-4 rounded-xl border border-[var(--border-main)] space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="text-[var(--text-main)] font-bold flex items-center gap-1.5">
              <Mic class="w-4 h-4 text-[var(--accent-primary)]" />
              <span>Select Neural Voice:</span>
            </span>
            <span class="text-[11px] text-[var(--text-muted)]">Zero API Key Needed • Cached Locally</span>
          </div>

          <div class="grid sm:grid-cols-2 gap-2.5">
            {#each (voices.length > 0 ? voices : [
              { id: 'en-US-JennyNeural', name: 'Jenny (US)', flag: '🇺🇸', gender: 'Female', description: 'Warm, natural American female voice (Recommended)' },
              { id: 'en-US-GuyNeural', name: 'Guy (US)', flag: '🇺🇸', gender: 'Male', description: 'Deep, clear & professional American male voice' },
              { id: 'en-US-AriaNeural', name: 'Aria (US)', flag: '🇺🇸', gender: 'Female', description: 'Expressive & articulate American female voice' },
              { id: 'en-GB-SoniaNeural', name: 'Sonia (UK)', flag: '🇬🇧', gender: 'Female', description: 'Standard British RP female voice' },
              { id: 'en-GB-RyanNeural', name: 'Ryan (UK)', flag: '🇬🇧', gender: 'Male', description: 'Crisp & polite British RP male voice' },
              { id: 'en-AU-NatashaNeural', name: 'Natasha (AU)', flag: '🇦🇺', gender: 'Female', description: 'Friendly Australian English female voice' }
            ]) as v}
              <button
                onclick={() => config.tts_voice = v.id}
                class={`p-3 rounded-xl border text-left transition cursor-pointer flex items-start gap-3 ${
                  config.tts_voice === v.id
                    ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary)] text-[var(--accent-primary)]'
                    : 'bg-[var(--bg-card)] border border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
                }`}
              >
                <span class="text-2xl shrink-0 mt-0.5">{v.flag}</span>
                <div class="min-w-0 flex-1">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-[var(--text-main)]">{v.name}</span>
                    <span class="text-[10px] px-1.5 py-0.5 rounded bg-[var(--bg-inner)] text-[var(--text-subtle)] font-medium">{v.gender}</span>
                  </div>
                  <p class="text-[11px] text-[var(--text-muted)] mt-1 line-clamp-1">{v.description}</p>
                </div>
              </button>
            {/each}
          </div>
        </div>
      {/if}

      <!-- Speech Speed Selector -->
      <div class="flex items-center justify-between p-3.5 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)]">
        <div>
          <span class="text-xs font-semibold text-[var(--text-main)] block">Default Pronunciation Speed:</span>
          <span class="text-[11px] text-[var(--text-muted)]">Controls speech rate across Flashcards, Dictation & Gym</span>
        </div>
        <div class="flex items-center gap-1.5">
          {#each [0.75, 0.85, 1.0, 1.15] as spd}
            <button
              onclick={() => config.default_audio_speed = spd}
              class={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition cursor-pointer ${
                config.default_audio_speed === spd
                  ? 'bg-[var(--accent-primary)] text-white'
                  : 'bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-main)]'
              }`}
            >
              {spd}x
            </button>
          {/each}
        </div>
      </div>
    </div>

    <!-- Obsidian Vault Settings -->
    <div class="space-y-3 border-t border-[var(--border-main)] pt-5">
      <div class="flex items-center gap-2 text-sm font-bold text-[var(--text-main)]">
        <Folder class="w-4 h-4 text-[var(--accent-primary)]" />
        <span>Obsidian Vault Directory</span>
      </div>
      <p class="text-xs text-[var(--text-muted)] leading-relaxed">
        The path to your Obsidian Vault (e.g., <code class="text-[var(--text-main)] font-mono">~/Obsidian/ZederVault</code>). Vocabulary cards will be stored in <code class="text-[var(--text-main)] font-mono">English/Vocab/</code> and writing essays in <code class="text-[var(--text-main)] font-mono">English/Writing/</code>.
      </p>
      <input
        type="text"
        bind:value={config.obsidian_vault_path}
        placeholder="~/Obsidian/ZederVault"
        class="w-full bg-[var(--bg-inner)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-xl px-4 py-2.5 text-sm text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none font-mono"
      />
    </div>

    <!-- AI Evaluation Engine Settings -->
    <div class="space-y-4 border-t border-[var(--border-main)] pt-5">
      <div class="flex items-center gap-2 text-sm font-bold text-[var(--text-main)]">
        <Cpu class="w-4 h-4 text-[var(--accent-primary)]" />
        <span>AI Evaluation Provider</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
        <!-- Antigravity (agy) -->
        <button
          onclick={() => config.ai_provider = 'agy'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'agy'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">Antigravity 🛸</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-[var(--accent-primary)]">Native</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">Runs via local agy CLI</div>
        </button>

        <!-- OpenCode CLI -->
        <button
          onclick={() => config.ai_provider = 'opencode'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'opencode'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">OpenCode 🤖</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-emerald-700">Free Agent</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">Runs via opencode CLI</div>
        </button>

        <!-- OpenRouter -->
        <button
          onclick={() => config.ai_provider = 'openrouter'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'openrouter'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">OpenRouter 🌐</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-[var(--accent-primary)]">Cloud</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">Llama 3.3 & DeepSeek Free</div>
        </button>

        <!-- Groq -->
        <button
          onclick={() => config.ai_provider = 'groq'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'groq'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">Groq ⚡</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-amber-700">Fast</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">Fast inference Llama 70B</div>
        </button>

        <!-- Ollama -->
        <button
          onclick={() => config.ai_provider = 'ollama'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'ollama'
              ? 'bg-[var(--accent-primary-light)] border-[var(--accent-primary)] text-[var(--accent-primary)]'
              : 'bg-[var(--bg-inner)] border-[var(--border-main)] text-[var(--text-muted)] hover:text-[var(--text-main)]'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-[var(--text-main)]">Local Ollama 🦙</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[var(--bg-card)] text-[var(--text-subtle)]">Offline</span>
          </div>
          <div class="text-xs text-[var(--text-muted)]">100% private offline</div>
        </button>
      </div>

      <!-- Detail Form for Selected Provider -->
      {#if config.ai_provider === 'agy'}
        <div class="bg-[var(--bg-inner)] p-4 rounded-xl border border-[var(--border-main)] space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="text-[var(--accent-primary)] font-bold flex items-center gap-1.5">
              <Bot class="w-4 h-4" />
              <span>Antigravity CLI (agy) Configuration:</span>
            </span>
            <span class="text-[11px] text-[var(--text-muted)]">Authenticated Session</span>
          </div>

          <div class="space-y-1.5">
            <span class="text-xs font-semibold text-[var(--text-main)]">Supported Model:</span>
            <div class="flex flex-wrap gap-1.5">
              {#each AGY_MODEL_PRESETS as preset}
                <button
                  onclick={() => config.agy_model = preset.id}
                  class={`px-2.5 py-1 rounded-lg text-xs font-mono transition cursor-pointer ${
                    config.agy_model === preset.id
                      ? 'bg-[var(--accent-primary)] text-white font-bold'
                      : 'bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-main)]'
                  }`}
                >
                  {preset.label}
                </button>
              {/each}
            </div>
          </div>
        </div>

      {:else if config.ai_provider === 'openrouter'}
        <div class="bg-[var(--bg-inner)] p-4 rounded-xl border border-[var(--border-main)] space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-[var(--text-main)] flex items-center gap-1.5">
              <Key class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              OpenRouter API Key:
            </span>
            <a
              href="https://openrouter.ai/keys"
              target="_blank"
              class="text-[var(--accent-primary)] hover:underline flex items-center gap-1"
            >
              <span>Get Free Key at OpenRouter.ai</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>
          <input
            type="password"
            bind:value={config.openrouter_api_key}
            placeholder="sk-or-v1-..."
            class="w-full bg-[var(--bg-card)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-xl px-4 py-2 text-xs text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none font-mono"
          />
        </div>

      {:else if config.ai_provider === 'groq'}
        <div class="bg-[var(--bg-inner)] p-4 rounded-xl border border-[var(--border-main)] space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-[var(--text-main)] flex items-center gap-1.5">
              <Zap class="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              Groq API Key:
            </span>
            <a
              href="https://console.groq.com/keys"
              target="_blank"
              class="text-[var(--accent-primary)] hover:underline flex items-center gap-1"
            >
              <span>Get Free Key at Groq Console</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>
          <input
            type="password"
            bind:value={config.groq_api_key}
            placeholder="gsk_..."
            class="w-full bg-[var(--bg-card)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-xl px-4 py-2 text-xs text-[var(--text-main)] placeholder-[var(--text-subtle)] outline-none font-mono"
          />
        </div>

      {:else if config.ai_provider === 'ollama'}
        <div class="bg-[var(--bg-inner)] p-4 rounded-xl border border-[var(--border-main)] grid grid-cols-2 gap-3">
          <div class="space-y-1.5">
            <span class="text-xs font-bold text-[var(--text-main)]">Ollama Host URL:</span>
            <input
              type="text"
              bind:value={config.ollama_url}
              placeholder="http://localhost:11434"
              class="w-full bg-[var(--bg-card)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-xl px-3.5 py-2 text-xs text-[var(--text-main)] font-mono"
            />
          </div>
          <div class="space-y-1.5">
            <span class="text-xs font-bold text-[var(--text-main)]">Ollama Model Name:</span>
            <input
              type="text"
              bind:value={config.ollama_model}
              placeholder="llama3:latest"
              class="w-full bg-[var(--bg-card)] border border-[var(--border-main)] focus:border-[var(--accent-primary)] rounded-xl px-3.5 py-2 text-xs text-[var(--text-main)] font-mono"
            />
          </div>
        </div>
      {/if}
    </div>

    <!-- Data Safety & Backup -->
    <div class="space-y-4 border-t border-[var(--border-main)] pt-5">
      <div class="flex items-center gap-2 text-sm font-bold text-[var(--text-main)]">
        <ShieldCheck class="w-4 h-4 text-[var(--accent-primary)]" />
        <span>Data Safety & Backup</span>
      </div>

      <div class="grid sm:grid-cols-2 gap-3">
        <!-- Backup Export Button -->
        <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2.5">
          <div>
            <h3 class="text-xs font-bold text-[var(--text-main)] flex items-center gap-1.5">
              <span>📦</span>
              <span>Export Vocabulary Backup</span>
            </h3>
            <p class="text-[11px] text-[var(--text-muted)] mt-0.5">
              Download all saved vocabulary, configurations, and review history as a JSON backup.
            </p>
          </div>
          <button
            onclick={handleExportBackup}
            class="w-full py-2 px-3 rounded-lg bg-[var(--bg-card)] hover:bg-[var(--accent-primary-light)] text-[var(--accent-primary)] border border-[var(--border-main)] text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer"
          >
            <span>Download Backup (.json)</span>
          </button>
        </div>

        <!-- Factory Reset Button -->
        <div class="p-4 rounded-xl bg-[var(--bg-inner)] border border-[var(--border-main)] space-y-2.5">
          <div>
            <h3 class="text-xs font-bold text-red-600 flex items-center gap-1.5">
              <span>⚠️</span>
              <span>Factory Reset & Clear Cache</span>
            </h3>
            <p class="text-[11px] text-[var(--text-muted)] mt-0.5">
              Restore app configurations to factory defaults. (Keeps Obsidian notes safe).
            </p>
          </div>
          <button
            onclick={handleFactoryReset}
            class="w-full py-2 px-3 rounded-lg bg-[var(--bg-card)] hover:bg-red-500/10 text-red-600 border border-red-500/30 text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer"
          >
            <span>Restore Factory Defaults</span>
          </button>
        </div>
      </div>
    </div>
  </article>
</div>
