<script lang="ts">
  import { onMount } from 'svelte';
  import { playAudioUrl, stopAudio } from '../utils/audio';
  import { Volume2, Search, Eye, EyeOff, Headphones, ExternalLink, Play, Pause } from 'lucide-svelte';
  import { GetListeningTopics } from '../../../wailsjs/go/main/App.js';

  interface TopicItem {
    id?: number;
    topic_id?: number;
    title: string;
    icon: string;
    audio: string;
    url?: string;
    qa: { q: string; a: string }[];
  }

  // Pre-configured fallback topics
  const FALLBACK_TOPICS: TopicItem[] = [
    {
      topic_id: 1,
      title: "Family",
      icon: "👨‍👩‍👧",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-01.mp3",
      url: "https://basicenglishspeaking.com/family/",
      qa: [
        { q: "How many people are there in your family?", a: "There are four people in my family: my father, my mother, my younger sister, and me." },
        { q: "Does your family live in a house or an apartment?", a: "We live in a cozy house with a small garden in the suburbs." },
        { q: "What does your father do?", a: "My father is a civil engineer who designs infrastructure projects." }
      ]
    },
    {
      topic_id: 2,
      title: "Restaurant",
      icon: "🍽️",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-02.mp3",
      url: "https://basicenglishspeaking.com/restaurant/",
      qa: [
        { q: "How often do you eat out? Who do you go with?", a: "I often eat out on weekends with my close friends or colleagues." },
        { q: "What restaurant do you usually visit?", a: "I love visiting a local Italian restaurant known for its handmade pasta and stone-baked pizza." },
        { q: "Do you prefer eating at home or eating out?", a: "I prefer home-cooked meals for health, but dining out is great for socializing." }
      ]
    },
    {
      topic_id: 58,
      title: "Computer",
      icon: "💻",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-58.mp3",
      url: "https://basicenglishspeaking.com/computer/",
      qa: [
        { q: "Do you have your own computer?", a: "Yes, I own a personal laptop which is essential for my daily work and study." },
        { q: "What do you usually use your computer for?", a: "I use it for programming, writing documents, researching information online, and occasionally listening to music." },
        { q: "How much time do you spend on the computer each day?", a: "On average, I spend around 6 to 8 hours daily since my career involves software engineering." }
      ]
    }
  ];

  let topics = $state<TopicItem[]>(FALLBACK_TOPICS);
  let searchQuery = $state('');
  let currentTopic = $state<TopicItem>(FALLBACK_TOPICS[0]);
  let hideAnswers = $state(false);
  let isFullAudioPlaying = $state(false);
  let speed = $state(1.0);

  let filteredTopics = $derived(
    topics.filter(t => t.title.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  async function loadTopics() {
    try {
      const dbTopics = await GetListeningTopics();
      if (dbTopics && dbTopics.length > 0) {
        topics = dbTopics.map((t: any) => ({
          id: t.id,
          topic_id: t.topic_id,
          title: t.title,
          icon: t.icon || '🎧',
          audio: t.audio,
          url: t.url,
          qa: t.qa || []
        }));
        if (topics.length > 0) {
          currentTopic = topics[0];
        }
      }
    } catch (e) {
      console.warn('Could not load topics from SQLite database:', e);
    }
  }

  function playFullAudio(slow = false) {
    if (!currentTopic.audio) return;
    isFullAudioPlaying = true;
    playAudioUrl(currentTopic.audio, slow ? 0.75 : 1.0, 'full_audio').then(() => {
      isFullAudioPlaying = false;
    });
  }

  onMount(() => {
    loadTopics();
  });
</script>

<div class="grid lg:grid-cols-12 gap-6">
  <!-- Left Column: Topic List & Search (4 cols) -->
  <div class="lg:col-span-4 space-y-4">
    <!-- Search Box -->
    <div class="relative">
      <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
      <input
        type="text"
        placeholder="Search conversational topics..."
        bind:value={searchQuery}
        class="w-full bg-slate-900 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 outline-none focus:border-blue-500 transition"
      />
    </div>

    <!-- Topics Scroll Area -->
    <div class="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-2 max-h-[600px] overflow-y-auto space-y-1.5 backdrop-blur-md">
      {#each filteredTopics as t}
        <button
          onclick={() => { currentTopic = t; stopAudio(); }}
          class={`w-full p-3 rounded-xl text-left transition cursor-pointer flex items-center justify-between ${
            (currentTopic.topic_id || currentTopic.id) === (t.topic_id || t.id)
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
              : 'hover:bg-slate-800 text-slate-300'
          }`}
        >
          <div class="flex items-center gap-2.5">
            <span class="text-xl">{t.icon}</span>
            <span class="text-sm font-semibold">{t.title}</span>
          </div>
          <span class="text-xs font-mono opacity-60">#{t.topic_id || t.id}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Right Column: Interactive Player & Q&A Stream (8 cols) -->
  <div class="lg:col-span-8 space-y-6">
    <!-- Header Hero Card -->
    <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 backdrop-blur-xl shadow-2xl space-y-5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div class="flex items-center gap-3">
          <span class="text-3xl p-3 rounded-2xl bg-slate-800/80 border border-slate-700 shadow-inner">
            {currentTopic.icon}
          </span>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">
                Conversation Practice
              </span>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300">
                #{currentTopic.topic_id || currentTopic.id}
              </span>
            </div>
            <h3 class="text-2xl font-black text-slate-100 tracking-tight mt-0.5">
              {currentTopic.title}
            </h3>
          </div>
        </div>

        <!-- Controls: Hide/Reveal Answers & External Link -->
        <div class="flex items-center gap-2">
          <button
            onclick={() => hideAnswers = !hideAnswers}
            class={`px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border ${
              hideAnswers
                ? 'bg-amber-600/20 text-amber-300 border-amber-500/30'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700'
            }`}
            title="Toggle blur mode for active listening practice"
          >
            {#if hideAnswers}
              <EyeOff class="w-4 h-4" />
              <span>Answers Hidden</span>
            {:else}
              <Eye class="w-4 h-4" />
              <span>Hide Answers</span>
            {/if}
          </button>

          {#if currentTopic.url}
            <a
              href={currentTopic.url}
              target="_blank"
              class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition"
              title="Open source transcript on basicenglishspeaking.com"
            >
              <ExternalLink class="w-4 h-4" />
            </a>
          {/if}
        </div>
      </div>

      <!-- Master Audio Player Toolbar -->
      <div class="flex flex-wrap items-center justify-between gap-3 p-4 rounded-2xl bg-slate-950/80 border border-slate-800">
        <div class="flex items-center gap-2">
          <button
            onclick={() => playFullAudio(false)}
            class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-2 transition shadow-lg shadow-blue-500/25 active:scale-95 cursor-pointer"
          >
            <Play class="w-4 h-4" />
            <span>Play Full Audio (1.0x)</span>
          </button>

          <button
            onclick={() => playFullAudio(true)}
            class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border border-slate-700"
            title="Play slower for clear pronunciation listening"
          >
            <Headphones class="w-3.5 h-3.5 text-cyan-400" />
            <span>Slow (0.75x)</span>
          </button>
        </div>

        <button
          onclick={stopAudio}
          class="px-3 py-2 rounded-xl bg-slate-800/60 hover:bg-rose-950/40 text-slate-400 hover:text-rose-400 text-xs transition cursor-pointer border border-slate-700/60"
        >
          Stop Audio
        </button>
      </div>

      <!-- Q&A Conversation Stream -->
      <div class="space-y-4 pt-2">
        {#each currentTopic.qa as item, idx}
          <div class="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-2 hover:border-slate-700 transition">
            <!-- Question -->
            <div class="flex items-start justify-between gap-3">
              <div class="flex items-start gap-2.5">
                <span class="px-2 py-0.5 rounded text-xs font-bold font-mono bg-blue-600/20 text-blue-400 border border-blue-500/30 shrink-0 mt-0.5">
                  Q{idx + 1}
                </span>
                <p class="text-sm font-bold text-slate-100 leading-snug">
                  {item.q}
                </p>
              </div>

              <!-- Play Individual Question Audio via TTS -->
              <button
                onclick={() => playAudioUrl(`https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=${encodeURIComponent(item.q)}`, 1.0)}
                class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition cursor-pointer shrink-0"
                title="Listen to question"
              >
                <Volume2 class="w-3.5 h-3.5" />
              </button>
            </div>

            <!-- Answer (with blur toggle) -->
            <div class="flex items-start justify-between gap-3 pl-8">
              <p class={`text-sm leading-relaxed transition-all duration-200 ${
                hideAnswers
                  ? 'blur-sm select-none text-slate-500 hover:blur-none cursor-pointer'
                  : 'text-slate-300'
              }`}>
                {item.a}
              </p>

              <!-- Play Individual Answer Audio via TTS -->
              <button
                onclick={() => playAudioUrl(`https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=${encodeURIComponent(item.a)}`, 1.0)}
                class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition cursor-pointer shrink-0"
                title="Listen to answer"
              >
                <Volume2 class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>
