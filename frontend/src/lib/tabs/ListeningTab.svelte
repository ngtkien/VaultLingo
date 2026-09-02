<script lang="ts">
  import { onMount } from 'svelte';
  import { playAudioUrl, stopAudio } from '../utils/audio';
  import { 
    Volume2, 
    Search, 
    Eye, 
    EyeOff, 
    Headphones, 
    ExternalLink, 
    Play, 
    Pause, 
    FileText, 
    MessageSquareQuote,
    Copy,
    Check,
    AlignLeft,
    ListFilter
  } from 'lucide-svelte';
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

  // Pre-configured fallback topics matching exact audio recordings
  const FALLBACK_TOPICS: TopicItem[] = [
    {
      topic_id: 1,
      title: "Family",
      icon: "👨‍👩‍👧",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-01.mp3",
      url: "https://basicenglishspeaking.com/family/",
      qa: [
        { q: "How many people are there in your family?", a: "There are 5 people in my family: my father, mother, brother, sister, and me." },
        { q: "Does your family live in a house or an apartment?", a: "We live in a house in the countryside." },
        { q: "What does your father do?", a: "My father is a doctor. He works at the local hospital." },
        { q: "How old is your mother?", a: "She is 40 years old, 1 year younger than my father." },
        { q: "Do you have any siblings? What’s his/her name?", a: "Yes, I do. I have 1 elder brother, David, and 1 younger sister, Mary." },
        { q: "Are you the oldest amongst your brothers and sisters?", a: "No, I’m not. I’m the second child in my family." },
        { q: "What does your mother/father like?", a: "My father likes playing football and my mother likes cooking." },
        { q: "Do your parents let you stay out late?", a: "Of course not. They always ask me to get home before 10 pm each night." },
        { q: "Do you stay with your parents?", a: "Right now, no, but I used to." },
        { q: "Does your family usually have dinner together?", a: "Yes, we do. My mom always prepares delicious meals for us." }
      ]
    },
    {
      topic_id: 2,
      title: "Restaurant",
      icon: "🍽️",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-02.mp3",
      url: "https://basicenglishspeaking.com/restaurant/",
      qa: [
        { q: "How often do you eat out? Who do you go with?", a: "I often eat out on weekends, when I hang out with my friends." },
        { q: "What restaurant do you usually visit?", a: "Well, there are not many restaurants in my neighborhood, so my best choice is the deli in convenient stores like the Circle K, Mini-Stop, B-smart." },
        { q: "What type of food do you enjoy to eat? Western or Asian?", a: "I’m interested in Asian food, Western food is not my thing." },
        { q: "How much do you usually pay when you eat out?", a: "It’s not very expensive, just around $5 for each meal." },
        { q: "Do you enjoy spicy food?", a: "Yes, I do, especially on cold days." },
        { q: "Are the servers there friendly to you?", a: "Yes, they are. Most of them are really helpful." },
        { q: "Have you ever tried Italian food?", a: "Yes, at least once, when I was in my friend’s wedding party." },
        { q: "Are you concerned about calories when eating out?", a: "Yes, I am. I’m on diet now, so this really matters to me." },
        { q: "Are fast food restaurants like KFC or McDonald’s famous in your country?", a: "Yes, they are. The youth in my country are big fans of fast food." },
        { q: "Do you often drink alcohol when eating out?", a: "No, not often. Just when I have parties with my friends." }
      ]
    },
    {
      topic_id: 58,
      title: "Computer",
      icon: "💻",
      audio: "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-58.mp3",
      url: "https://basicenglishspeaking.com/computer/",
      qa: [
        { q: "Do you have your own computer?", a: "Yes, I owned a personal laptop when I was in university." },
        { q: "How often do you use the computer?", a: "Almost every day. I can’t work without a computer." },
        { q: "Have you ever joined any computer class?", a: "Yes, years ago. I learned about Microsoft Word and Excel." },
        { q: "What do you use the computer for?", a: "You know, I’m an accountant, so managing business records would be much easier for me using a computer." },
        { q: "What are some advantages of using the computer?", a: "With a computer connected to the Internet, we can shop, pay bills or do bank transactions online. Listening to music, watching movies are even more convenient." },
        { q: "Do you use other high-tech devices besides computers?", a: "Yes, apart from a computer, I also use a smartphone." },
        { q: "Should children learn how to use the computer?", a: "Yes, I think so. Children should be given chances to approach the computer but under the control of their parents." }
      ]
    }
  ];

  let topics = $state<TopicItem[]>(FALLBACK_TOPICS);
  let searchQuery = $state('');
  let currentTopic = $state<TopicItem>(FALLBACK_TOPICS[0]);
  let showTranscript = $state(false);
  let transcriptFormat = $state<'dialogue' | 'text'>('dialogue');
  let hideAnswers = $state(false);
  let isFullAudioPlaying = $state(false);
  let copied = $state(false);

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

  function copyTranscript() {
    if (!currentTopic?.qa) return;
    const text = currentTopic.qa.map(item => `Q: ${item.q}\nA: ${item.a}`).join('\n\n');
    navigator.clipboard.writeText(text);
    copied = true;
    setTimeout(() => { copied = false; }, 2000);
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

  <!-- Right Column: Interactive Player & Audio Transcript (8 cols) -->
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
                Audio Listening Practice
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

        <!-- Header Controls: Show/Hide Audio Transcript & External Link -->
        <div class="flex items-center flex-wrap gap-2">
          <button
            onclick={() => showTranscript = !showTranscript}
            class={`px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer border ${
              showTranscript
                ? 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700'
                : 'bg-blue-600 hover:bg-blue-500 text-white border-blue-500 shadow-lg shadow-blue-500/25'
            }`}
            title={showTranscript ? "Hide audio transcript" : "Show full audio transcript"}
          >
            {#if showTranscript}
              <EyeOff class="w-4 h-4" />
              <span>Hide Audio Transcript</span>
            {:else}
              <FileText class="w-4 h-4 text-white" />
              <span>Show Audio Transcript</span>
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
            <span>Play Audio (1.0x)</span>
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

        <div class="flex items-center gap-2">
          <button
            onclick={() => showTranscript = !showTranscript}
            class="px-3 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-blue-400 text-xs font-medium flex items-center gap-1.5 transition cursor-pointer border border-slate-700/80"
          >
            <FileText class="w-3.5 h-3.5" />
            <span>{showTranscript ? 'Hide Transcript' : 'Show Transcript'}</span>
          </button>

          <button
            onclick={stopAudio}
            class="px-3 py-2 rounded-xl bg-slate-800/60 hover:bg-rose-950/40 text-slate-400 hover:text-rose-400 text-xs transition cursor-pointer border border-slate-700/60"
          >
            Stop
          </button>
        </div>
      </div>

      <!-- Main Content Area: Audio Transcript or Listening Comprehension Mode -->
      {#if showTranscript}
        <!-- Audio Transcript Container -->
        <div class="space-y-4 pt-2">
          <!-- Transcript Top Toolbar -->
          <div class="flex flex-wrap items-center justify-between gap-2 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <div class="flex items-center gap-2">
              <span class="flex items-center gap-1.5 text-xs font-bold text-slate-200">
                <MessageSquareQuote class="w-4 h-4 text-blue-400" />
                Audio Transcript
              </span>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-slate-800 text-slate-400">
                {currentTopic.qa.length} dialogue turns
              </span>
            </div>

            <div class="flex items-center gap-2">
              <!-- Switch Format: Dialogue vs Continuous Text -->
              <div class="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5">
                <button
                  onclick={() => transcriptFormat = 'dialogue'}
                  class={`px-2.5 py-1 rounded-md text-[11px] font-medium transition cursor-pointer flex items-center gap-1 ${
                    transcriptFormat === 'dialogue'
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Dialogue exchanges view"
                >
                  <ListFilter class="w-3 h-3" />
                  <span>Dialogue</span>
                </button>
                <button
                  onclick={() => transcriptFormat = 'text'}
                  class={`px-2.5 py-1 rounded-md text-[11px] font-medium transition cursor-pointer flex items-center gap-1 ${
                    transcriptFormat === 'text'
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Continuous script text view"
                >
                  <AlignLeft class="w-3 h-3" />
                  <span>Full Text</span>
                </button>
              </div>

              <!-- Blur Answers Toggle in Dialogue View -->
              {#if transcriptFormat === 'dialogue'}
                <button
                  onclick={() => hideAnswers = !hideAnswers}
                  class={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition cursor-pointer border flex items-center gap-1 ${
                    hideAnswers
                      ? 'bg-amber-600/20 text-amber-300 border-amber-500/30'
                      : 'bg-slate-900 hover:bg-slate-800 text-slate-400 border-slate-800'
                  }`}
                  title="Blur responses for active recall"
                >
                  {#if hideAnswers}
                    <EyeOff class="w-3 h-3" />
                    <span>Responses Hidden</span>
                  {:else}
                    <Eye class="w-3 h-3" />
                    <span>Hide Responses</span>
                  {/if}
                </button>
              {/if}

              <!-- Copy Transcript Button -->
              <button
                onclick={copyTranscript}
                class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 text-[11px] font-medium transition cursor-pointer border border-slate-800 flex items-center gap-1"
                title="Copy entire audio transcript"
              >
                {#if copied}
                  <Check class="w-3 h-3 text-emerald-400" />
                  <span class="text-emerald-400">Copied</span>
                {:else}
                  <Copy class="w-3 h-3" />
                  <span>Copy</span>
                {/if}
              </button>
            </div>
          </div>

          <!-- Transcript Body -->
          {#if transcriptFormat === 'dialogue'}
            <div class="space-y-3">
              {#each currentTopic.qa as item, idx}
                <div class="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-2.5 hover:border-slate-700 transition shadow-sm">
                  <!-- Speaker A (Question / Prompt in Audio) -->
                  <div class="flex items-start gap-3">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold font-mono bg-blue-600/20 text-blue-400 border border-blue-500/30 shrink-0 mt-0.5">
                      Speaker 1
                    </span>
                    <p class="text-sm font-semibold text-slate-200 leading-relaxed">
                      {item.q}
                    </p>
                  </div>

                  <!-- Speaker B (Response / Spoken in Audio) -->
                  <div class="flex items-start gap-3 pl-2 sm:pl-4 border-l-2 border-slate-800 ml-3">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold font-mono bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 shrink-0 mt-0.5">
                      Speaker 2
                    </span>
                    <p class={`text-sm leading-relaxed transition-all duration-200 ${
                      hideAnswers
                        ? 'blur-sm select-none text-slate-500 hover:blur-none cursor-pointer'
                        : 'text-slate-300'
                    }`}>
                      {item.a}
                    </p>
                  </div>
                </div>
              {/each}
            </div>
          {:else}
            <!-- Full Continuous Script View -->
            <div class="p-6 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-4">
              <div class="text-xs uppercase tracking-wider text-slate-500 font-bold">
                Spoken Audio Script: {currentTopic.title}
              </div>
              <div class="space-y-4 text-sm leading-relaxed text-slate-200 divide-y divide-slate-800/60">
                {#each currentTopic.qa as item}
                  <div class="pt-3 first:pt-0 space-y-1">
                    <p class="font-medium text-blue-300">
                      — {item.q}
                    </p>
                    <p class="text-slate-300 pl-4">
                      {item.a}
                    </p>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      {:else}
        <!-- Active Listening Comprehension Mode Banner -->
        <div class="py-12 px-6 rounded-2xl bg-slate-950/40 border border-slate-800/80 border-dashed text-center space-y-4 flex flex-col items-center justify-center">
          <div class="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shadow-inner">
            <Headphones class="w-7 h-7" />
          </div>
          <div class="max-w-md space-y-1.5">
            <h4 class="text-base font-bold text-slate-200">Active Audio Listening Mode</h4>
            <p class="text-xs text-slate-400 leading-relaxed">
              Listen to the complete audio recording above to train your ear. When you are ready to review what was spoken, click below to reveal the audio transcript.
            </p>
          </div>
          <button
            onclick={() => showTranscript = true}
            class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-2 transition shadow-lg shadow-blue-500/25 cursor-pointer active:scale-95"
          >
            <FileText class="w-4 h-4" />
            <span>Show Audio Transcript</span>
          </button>
        </div>
      {/if}
    </div>
  </div>
</div>
