<script lang="ts">
  import { onMount } from 'svelte';
  import { GetConfig, SaveConfig, GetSavedObsidianVocab } from '../../../wailsjs/go/main/App.js';
  import { Save, Check, Folder, Key, Cpu, Volume2, ShieldCheck, Sparkles, ExternalLink, Zap, Lock, Info, Bot } from 'lucide-svelte';

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
    default_audio_speed: 1.0
  });

  let savedMessage = $state(false);
  let saving = $state(false);

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
    } catch (e) {
      console.error(e);
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

  async function handleExportBackup() {
    try {
      const items = await GetSavedObsidianVocab();
      const backupData = {
        app: 'VaultLingo',
        version: '0.1.0',
        export_date: new Date().toISOString(),
        config: {
          ai_provider: config.ai_provider,
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
        default_audio_speed: 1.0
      };
      handleSave();
      window.location.reload();
    }
  }

  onMount(() => {
    loadConfig();
  });
</script>

<div class="max-w-3xl mx-auto space-y-6">
  <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between border-b border-slate-800 pb-4">
      <div>
        <h3 class="text-xl font-bold text-slate-100">Settings & Preferences</h3>
        <p class="text-xs text-slate-400">Configure your Obsidian Vault path, AI provider, and audio options</p>
      </div>

      <button
        onclick={handleSave}
        disabled={saving}
        class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-blue-500/25 transition cursor-pointer active:scale-95"
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
    <div class="p-4 rounded-2xl bg-gradient-to-br from-cyan-950/40 via-slate-900 to-indigo-950/40 border border-cyan-500/30 space-y-3 shadow-lg">
      <div class="flex items-center gap-2 text-cyan-400 font-bold text-sm">
        <ShieldCheck class="w-5 h-5 text-cyan-400" />
        <span>Security & API Token Privacy Disclaimer</span>
      </div>

      <div class="grid sm:grid-cols-2 gap-3 text-xs text-slate-300">
        <div class="flex items-start gap-2 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/80">
          <Lock class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <strong class="text-slate-100 block">100% Local Storage</strong>
            Your API keys are stored strictly in your local configuration at <code class="text-cyan-300 font-mono text-[11px]">~/.config/VaultLingo/config.json</code>.
          </div>
        </div>

        <div class="flex items-start gap-2 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/80">
          <Info class="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <div>
            <strong class="text-slate-100 block">Zero Intermediary Servers</strong>
            Requests are sent directly and encrypted over HTTPS to your chosen provider or executed locally via <code class="text-slate-200 font-mono">agy</code>.
          </div>
        </div>
      </div>
    </div>

    <!-- Obsidian Vault Settings -->
    <div class="space-y-3">
      <div class="flex items-center gap-2 text-sm font-bold text-purple-400">
        <Folder class="w-4 h-4" />
        <span>Obsidian Vault Directory</span>
      </div>
      <p class="text-xs text-slate-400 leading-relaxed">
        The absolute or home-relative path to your Obsidian Vault (e.g., <code class="text-slate-300">~/Obsidian/ZederVault</code>). Vocabulary cards will be automatically organized into <code class="text-slate-300">English/Vocab/</code> and writing essays into <code class="text-slate-300">English/Writing/</code>.
      </p>
      <input
        type="text"
        bind:value={config.obsidian_vault_path}
        placeholder="~/Obsidian/ZederVault"
        class="w-full bg-slate-950 border border-slate-700/80 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 outline-none font-mono"
      />
    </div>

    <!-- AI Evaluation Engine Settings -->
    <div class="space-y-4 border-t border-slate-800 pt-5">
      <div class="flex items-center gap-2 text-sm font-bold text-cyan-400">
        <Cpu class="w-4 h-4" />
        <span>AI Evaluation Provider</span>
      </div>

      <!-- 4 Provider Selector Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <!-- Antigravity (agy) -->
        <button
          onclick={() => config.ai_provider = 'agy'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'agy'
              ? 'bg-violet-600/20 border-violet-500 text-violet-300 ring-1 ring-violet-500/40'
              : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold">Antigravity (agy) 🛸</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-violet-500/20 text-violet-300">Zero-Key</span>
          </div>
          <div class="text-xs opacity-75">Runs via local agy CLI with dynamic model support</div>
        </button>

        <!-- OpenRouter -->
        <button
          onclick={() => config.ai_provider = 'openrouter'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'openrouter'
              ? 'bg-cyan-600/20 border-cyan-500 text-cyan-300 ring-1 ring-cyan-500/40'
              : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold">OpenRouter 🌐</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-cyan-500/20 text-cyan-300">Free Tier</span>
          </div>
          <div class="text-xs opacity-75">Llama 3.3, Gemini 2.0 & DeepSeek Free</div>
        </button>

        <!-- Groq -->
        <button
          onclick={() => config.ai_provider = 'groq'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'groq'
              ? 'bg-amber-600/20 border-amber-500 text-amber-300 ring-1 ring-amber-500/40'
              : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold">Groq ⚡</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-500/20 text-amber-300">Fast</span>
          </div>
          <div class="text-xs opacity-75">Ultra-fast inference on Llama 3.3 70B</div>
        </button>

        <!-- Ollama -->
        <button
          onclick={() => config.ai_provider = 'ollama'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'ollama'
              ? 'bg-emerald-600/20 border-emerald-500 text-emerald-300 ring-1 ring-emerald-500/40'
              : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
          }`}
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold">Local Ollama 🦙</span>
            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300">Offline</span>
          </div>
          <div class="text-xs opacity-75">100% private and offline on your computer</div>
        </button>
      </div>

      <!-- Detail Form for Selected Provider -->
      {#if config.ai_provider === 'agy'}
        <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="text-violet-300 font-bold flex items-center gap-1.5">
              <Bot class="w-4 h-4 text-violet-400" />
              <span>Antigravity CLI (agy) Configuration:</span>
            </span>
            <span class="text-[11px] text-slate-400">Authenticated Session (No API Key Required)</span>
          </div>

          <!-- Model Selector & Presets -->
          <div class="space-y-1.5">
            <span class="text-xs font-semibold text-slate-300">Supported Model:</span>
            <div class="flex flex-wrap gap-1.5">
              {#each AGY_MODEL_PRESETS as preset}
                <button
                  onclick={() => config.agy_model = preset.id}
                  class={`px-2.5 py-1 rounded-lg text-xs font-mono transition cursor-pointer ${
                    config.agy_model === preset.id
                      ? 'bg-violet-600 text-white font-bold'
                      : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
                  }`}
                >
                  {preset.label}
                </button>
              {/each}
            </div>
          </div>

          <!-- Custom Model Input -->
          <div class="space-y-1">
            <span class="text-[11px] text-slate-400">Custom Model Identifier (dynamically updates with agy CLI versions):</span>
            <input
              type="text"
              bind:value={config.agy_model}
              placeholder="gemini-3.7-flash"
              class="w-full bg-slate-900 border border-slate-700/80 focus:border-violet-500 rounded-xl px-3.5 py-2 text-xs text-slate-100 font-mono"
            />
          </div>
        </div>

      {:else if config.ai_provider === 'openrouter'}
        <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-slate-300 flex items-center gap-1.5">
              <Key class="w-3.5 h-3.5 text-cyan-400" />
              OpenRouter API Key:
            </span>
            <a
              href="https://openrouter.ai/keys"
              target="_blank"
              class="text-cyan-400 hover:underline flex items-center gap-1"
            >
              <span>Get Free Key at OpenRouter.ai</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>
          <input
            type="password"
            bind:value={config.openrouter_api_key}
            placeholder="sk-or-v1-..."
            class="w-full bg-slate-900 border border-slate-700/80 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 rounded-xl px-4 py-2 text-xs text-slate-100 placeholder-slate-500 outline-none font-mono"
          />

          <!-- Free Model Presets -->
          <div class="space-y-1.5 pt-1">
            <span class="text-xs font-semibold text-slate-400">Free Model Selection:</span>
            <div class="flex flex-wrap gap-1.5">
              {#each OPENROUTER_FREE_MODELS as m}
                <button
                  onclick={() => config.openrouter_model = m.id}
                  class={`px-2.5 py-1 rounded-lg text-xs font-mono transition cursor-pointer ${
                    config.openrouter_model === m.id
                      ? 'bg-cyan-500 text-slate-950 font-bold'
                      : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
                  }`}
                >
                  {m.label}
                </button>
              {/each}
            </div>
          </div>
        </div>

      {:else if config.ai_provider === 'groq'}
        <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-slate-300 flex items-center gap-1.5">
              <Zap class="w-3.5 h-3.5 text-amber-400" />
              Groq API Key:
            </span>
            <a
              href="https://console.groq.com/keys"
              target="_blank"
              class="text-amber-400 hover:underline flex items-center gap-1"
            >
              <span>Get Free Key at Groq Console</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>
          <input
            type="password"
            bind:value={config.groq_api_key}
            placeholder="gsk_..."
            class="w-full bg-slate-900 border border-slate-700/80 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 rounded-xl px-4 py-2 text-xs text-slate-100 placeholder-slate-500 outline-none font-mono"
          />

          <div class="space-y-1.5 pt-1">
            <span class="text-xs font-semibold text-slate-400">Groq Model:</span>
            <div class="flex gap-2">
              {#each ['llama-3.3-70b-versatile', 'mixtral-8x7b-32768'] as gm}
                <button
                  onclick={() => config.groq_model = gm}
                  class={`px-3 py-1 rounded-lg text-xs font-mono transition cursor-pointer ${
                    config.groq_model === gm
                      ? 'bg-amber-500 text-slate-950 font-bold'
                      : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
                  }`}
                >
                  {gm}
                </button>
              {/each}
            </div>
          </div>
        </div>

      {:else if config.ai_provider === 'ollama'}
        <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 grid grid-cols-2 gap-3">
          <div class="space-y-1.5">
            <span class="text-xs font-bold text-slate-300">Ollama Host URL:</span>
            <input
              type="text"
              bind:value={config.ollama_url}
              placeholder="http://localhost:11434"
              class="w-full bg-slate-900 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3.5 py-2 text-xs text-slate-100 font-mono"
            />
          </div>
          <div class="space-y-1.5">
            <span class="text-xs font-bold text-slate-300">Ollama Model Name:</span>
            <input
              type="text"
              bind:value={config.ollama_model}
              placeholder="llama3:latest"
              class="w-full bg-slate-900 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3.5 py-2 text-xs text-slate-100 font-mono"
            />
          </div>
        </div>
      {/if}
    </div>

    <!-- Audio Playback Settings -->
    <div class="space-y-3 border-t border-slate-800 pt-5">
      <div class="flex items-center gap-2 text-sm font-bold text-amber-400">
        <Volume2 class="w-4 h-4" />
        <span>Audio Playback Settings</span>
      </div>

      <div class="flex items-center justify-between p-3.5 rounded-xl bg-slate-950 border border-slate-800">
        <span class="text-xs text-slate-300">Default Pronunciation Speed:</span>
        <div class="flex items-center gap-1.5">
          {#each [0.75, 0.85, 1.0] as spd}
            <button
              onclick={() => config.default_audio_speed = spd}
              class={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition cursor-pointer ${
                config.default_audio_speed === spd
                  ? 'bg-amber-500 text-slate-950'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {spd}x
            </button>
          {/each}
        </div>
      </div>
    </div>

    <!-- Data Safety, Backup & Factory Reset -->
    <div class="space-y-4 border-t border-slate-800 pt-5">
      <div class="flex items-center gap-2 text-sm font-bold text-emerald-400">
        <ShieldCheck class="w-4 h-4" />
        <span>Data Safety & Backup Management</span>
      </div>

      <div class="grid sm:grid-cols-2 gap-3">
        <!-- Backup Export Button -->
        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2.5">
          <div>
            <h4 class="text-xs font-bold text-slate-100 flex items-center gap-1.5">
              <span>📦</span>
              <span>Export Vocabulary Backup</span>
            </h4>
            <p class="text-[11px] text-slate-400 mt-0.5">
              Download all saved vocabulary, configurations, and review history as a JSON backup.
            </p>
          </div>
          <button
            onclick={handleExportBackup}
            class="w-full py-2 px-3 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white border border-emerald-500/30 text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer active:scale-95"
          >
            <span>Download Backup (.json)</span>
          </button>
        </div>

        <!-- Factory Reset Button -->
        <div class="p-4 rounded-xl bg-slate-950 border border-red-500/30 space-y-2.5">
          <div>
            <h4 class="text-xs font-bold text-red-400 flex items-center gap-1.5">
              <span>⚠️</span>
              <span>Factory Reset & Clear Cache</span>
            </h4>
            <p class="text-[11px] text-slate-400 mt-0.5">
              Restore app configurations and search cache to factory defaults. (Keeps Obsidian notes safe).
            </p>
          </div>
          <button
            onclick={handleFactoryReset}
            class="w-full py-2 px-3 rounded-lg bg-red-500/15 hover:bg-red-600 text-red-300 hover:text-white border border-red-500/30 text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer active:scale-95"
          >
            <span>Restore Factory Defaults</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
