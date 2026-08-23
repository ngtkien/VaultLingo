<script lang="ts">
  import { onMount } from 'svelte';
  import { GetConfig, SaveConfig } from '../../../wailsjs/go/main/App.js';
  import { Save, Check, Folder, Key, Cpu, Volume2, ShieldCheck, Sparkles, ExternalLink } from 'lucide-svelte';

  let config = $state<any>({
    obsidian_vault_path: '',
    gemini_api_key: '',
    ai_provider: 'gemini',
    ollama_url: 'http://localhost:11434',
    ollama_model: 'llama3:latest',
    auto_play_audio: true,
    default_audio_speed: 1.0
  });

  let savedMessage = $state(false);
  let saving = $state(false);

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
      <div class="flex items-center gap-2 text-sm font-bold text-blue-400">
        <Cpu class="w-4 h-4" />
        <span>AI Evaluation Provider</span>
      </div>

      <!-- Provider Selector -->
      <div class="grid grid-cols-2 gap-3">
        <button
          onclick={() => config.ai_provider = 'gemini'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'gemini'
              ? 'bg-blue-600/20 border-blue-500 text-blue-300'
              : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
          }`}
        >
          <div class="text-sm font-bold">Google Gemini API 🌟</div>
          <div class="text-xs opacity-75">Fast, highly accurate evaluation powered by Gemini 2.5 Flash</div>
        </button>

        <button
          onclick={() => config.ai_provider = 'ollama'}
          class={`p-3.5 rounded-xl border text-left transition cursor-pointer space-y-1 ${
            config.ai_provider === 'ollama'
              ? 'bg-emerald-600/20 border-emerald-500 text-emerald-300'
              : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
          }`}
        >
          <div class="text-sm font-bold">Local Ollama (Offline) 🦙</div>
          <div class="text-xs opacity-75">Run locally hosted open models on your machine (Llama 3, Qwen 2.5)</div>
        </button>
      </div>

      {#if config.ai_provider === 'gemini'}
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-slate-300 flex items-center gap-1">
              <Key class="w-3.5 h-3.5 text-blue-400" />
              Gemini API Key:
            </span>
            <a
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              class="text-blue-400 hover:underline flex items-center gap-1"
            >
              <span>Get Free API Key from Google AI Studio</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>
          <input
            type="password"
            bind:value={config.gemini_api_key}
            placeholder="AIzaSy..."
            class="w-full bg-slate-950 border border-slate-700/80 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 outline-none font-mono"
          />
        </div>
      {:else}
        <div class="grid grid-cols-2 gap-3">
          <div class="space-y-1.5">
            <span class="text-xs font-bold text-slate-300">Ollama Host URL:</span>
            <input
              type="text"
              bind:value={config.ollama_url}
              placeholder="http://localhost:11434"
              class="w-full bg-slate-950 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3.5 py-2 text-xs text-slate-100 font-mono"
            />
          </div>
          <div class="space-y-1.5">
            <span class="text-xs font-bold text-slate-300">Ollama Model Name:</span>
            <input
              type="text"
              bind:value={config.ollama_model}
              placeholder="llama3:latest"
              class="w-full bg-slate-950 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3.5 py-2 text-xs text-slate-100 font-mono"
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
  </div>
</div>
