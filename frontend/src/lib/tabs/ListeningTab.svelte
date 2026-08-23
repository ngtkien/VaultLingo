<script lang="ts">
  import { onMount } from 'svelte';
  import { playAudioUrl, stopAudio } from '../utils/audio';
  import { Volume2, Search, Eye, EyeOff, Headphones, ExternalLink, Play, Pause } from 'lucide-svelte';

  interface TopicItem {
    id: number;
    title: string;
    icon: string;
    audio: string;
    url: string;
    qa: { q: string; a: string }[];
  }

  // Pre-configured 75 Listening Topics
  const TOPICS_75: TopicItem[] = [
    {
      id: 58,
      title: "Computer",
      icon: "💻",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-58.mp3",
      url: "https://basicenglishspeaking.com/computer/",
      qa: [
        { q: "Do you have your own computer?", a: "Yes, I own a personal laptop which is essential for my daily work and study." },
        { q: "What do you usually use your computer for?", a: "I use it for programming, writing documents, researching information online, and occasionally listening to music." },
        { q: "How much time do you spend on the computer each day?", a: "On average, I spend around 6 to 8 hours daily since my career involves software engineering." }
      ]
    },
    {
      id: 1,
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
      id: 2,
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
      id: 3,
      title: "Books & Reading",
      icon: "📖",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-03.mp3",
      url: "https://basicenglishspeaking.com/books/",
      qa: [
        { q: "How often do you read books?", a: "I try to read at least 30 minutes every evening before going to bed." },
        { q: "What kind of book do you like reading?", a: "I enjoy reading technology books, personal growth, and science fiction." }
      ]
    },
    {
      id: 4,
      title: "Travel & Vacation",
      icon: "✈️",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-04.mp3",
      url: "https://basicenglishspeaking.com/travel/",
      qa: [
        { q: "How many places have you traveled to?", a: "I have visited over ten cities across my country and two international destinations." },
        { q: "Who do you usually go with?", a: "I usually travel with my close friends or family during summer holidays." }
      ]
    },
    {
      id: 5,
      title: "Hobbies & Leisure",
      icon: "🎨",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-05.mp3",
      url: "https://basicenglishspeaking.com/hobbies/",
      qa: [
        { q: "What is your favorite hobby?", a: "My favorite hobby is exploring open-source projects, tinkering with electronics, and jogging." },
        { q: "When did you start that hobby?", a: "I started developing interest in computers when I was in high school." }
      ]
    }
  ];

  let searchQuery = $state('');
  let currentTopic = $state<TopicItem>(TOPICS_75[0]);
  let hideAnswers = $state(false);
  let isFullAudioPlaying = $state(false);
  let speed = $state(1.0);

  let filteredTopics = $derived(
    TOPICS_75.filter(t => t.title.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  function playFullAudio(slow = false) {
    if (!currentTopic.audio) return;
    isFullAudioPlaying = true;
    playAudioUrl(currentTopic.audio, slow ? 0.75 : 1.0, 'full_audio').then(() => {
      isFullAudioPlaying = false;
    });
  }
</script>

<div class="grid lg:grid-cols-12 gap-6">
  <!-- Left Column: Topic List & Search (4 cols) -->
  <div class="lg:col-span-4 space-y-4">
    <!-- Search Box -->
    <div class="relative">
      <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
      <input
        type="text"
        placeholder="Search 75 topics..."
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
            currentTopic.id === t.id
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
              : 'hover:bg-slate-800 text-slate-300'
          }`}
        >
          <div class="flex items-center gap-2.5">
            <span class="text-xl">{t.icon}</span>
            <span class="text-sm font-semibold">{t.title}</span>
          </div>
          <span class="text-xs font-mono opacity-60">#{t.id}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Right Column: Active Topic Player & Q&A (8 cols) -->
  <div class="lg:col-span-8 space-y-6">
    <!-- Topic Header & Audio Player -->
    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-5">
      <div class="flex items-start justify-between">
        <div class="flex items-center gap-3">
          <span class="text-3xl">{currentTopic.icon}</span>
          <div>
            <h3 class="text-2xl font-bold text-slate-100">{currentTopic.title}</h3>
            <a
              href={currentTopic.url}
              target="_blank"
              class="text-xs text-blue-400 hover:underline flex items-center gap-1 mt-0.5"
            >
              <span>BasicEnglishSpeaking.com Source</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>
        </div>

        <button
          onclick={() => hideAnswers = !hideAnswers}
          class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border border-slate-700"
        >
          {#if hideAnswers}
            <Eye class="w-3.5 h-3.5" />
            <span>Show Answers</span>
          {:else}
            <EyeOff class="w-3.5 h-3.5" />
            <span>Hide Answers (Active Listening)</span>
          {/if}
        </button>
      </div>

      <!-- Main Audio Playback Bar -->
      <div class="p-4 rounded-xl bg-slate-950/70 border border-slate-800 flex items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <button
            onclick={() => playFullAudio(false)}
            class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-blue-500/25 transition cursor-pointer"
          >
            <Headphones class="w-4 h-4" />
            <span>Play Full Topic Audio</span>
          </button>
          <button
            onclick={() => playFullAudio(true)}
            class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition cursor-pointer border border-slate-700"
          >
            0.75x Slow
          </button>
        </div>

        <span class="text-xs text-slate-400 italic">Topic #{currentTopic.id} Audio Stream</span>
      </div>

      <!-- Q&A Conversation Breakdown -->
      <div class="space-y-4 pt-2">
        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Questions & Sample Answers</h4>
        <div class="space-y-3">
          {#each currentTopic.qa as item, idx}
            <div class="p-4 rounded-xl bg-slate-950/50 border border-slate-800/80 space-y-2">
              <!-- Question -->
              <div class="flex items-start justify-between gap-3">
                <div class="flex items-start gap-2">
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-500/20 text-blue-300">
                    Q{idx + 1}
                  </span>
                  <p class="text-sm font-semibold text-slate-100">{item.q}</p>
                </div>
              </div>

              <!-- Answer -->
              <div class="flex items-start justify-between gap-3 pt-1 border-t border-slate-800/40">
                <div class="flex items-start gap-2">
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-300">
                    A
                  </span>
                  <p class={`text-sm text-slate-300 transition-all ${hideAnswers ? 'blur-sm select-none' : ''}`}>
                    {item.a}
                  </p>
                </div>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</div>
