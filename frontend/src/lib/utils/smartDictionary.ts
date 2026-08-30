import { GetDailyVocab, GetSavedObsidianVocab, EvaluateWriting } from '../../../wailsjs/go/main/App.js';
import { backend } from '../../../wailsjs/go/models';

export interface WordFamilyMember {
  pos: string;
  word: string;
}

export interface BilingualExample {
  en: string;
  vi: string;
}

export interface SmartWordResult {
  word: backend.Word;
  isLocal: boolean;
  synonyms?: string[];
  antonyms?: string[];
  collocations?: string[];
  word_family?: WordFamilyMember[];
  etymology?: string;
  mnemonic_hook?: string;
  examples?: BilingualExample[];
  nuance_tips?: string;
  source: 'vault' | 'app_vocab' | 'ai' | 'online_dict' | 'lexicon';
  audioUrl?: string;
}

// Built-in offline rich lexicon for popular & essential words
const OFFLINE_LEXICON: Record<string, Partial<SmartWordResult>> = {
  'serendipity': {
    word: new backend.Word({
      id: 1001,
      word: 'serendipity',
      raw_word: 'serendipity',
      pos: 'Noun',
      phonetic: '/ˌser.ənˈdɪp.ə.ti/',
      definition_en: 'The occurrence and development of events by chance in a happy or beneficial way.',
      definition_vi: 'Sự tình cờ may mắn; sự may mắn bất ngờ tìm thấy điều tốt đẹp mà không hề chủ ý tìm kiếm.',
      example_en: 'Finding my dream job while traveling abroad was pure serendipity.',
      example_vi: 'Tìm được công việc mơ ước khi đang đi du lịch nước ngoài quả là một sự tình cờ may mắn tuyệt vời.',
      level: 'C2 Proficiency',
      topic: 'mindset',
      topic_title: 'Fortunate Coincidence',
      topic_icon: '🍀',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/serendipity'
    }),
    isLocal: true,
    synonyms: ['chance', 'happy accident', 'fluke', 'providence', 'blessing', 'good fortune'],
    antonyms: ['misfortune', 'adversity', 'bad luck', 'calamity'],
    collocations: ['pure serendipity', 'stroke of serendipity', 'serendipitous encounter', 'by serendipity'],
    word_family: [
      { pos: 'Noun', word: 'serendipity' },
      { pos: 'Adjective', word: 'serendipitous' },
      { pos: 'Adverb', word: 'serendipitously' }
    ],
    etymology: 'Coined by Horace Walpole in 1754, from the Persian fairy tale "The Three Princes of Serendip" (ancient name for Sri Lanka), whose heroes were always making discoveries by accident.',
    mnemonic_hook: 'Think of "Serene" (peaceful) + "Dip" (dipping into luck) = Discovering peaceful, unexpected luck by chance!',
    examples: [
      {
        en: 'Finding my dream job while traveling abroad was pure serendipity.',
        vi: 'Tìm được công việc mơ ước khi đang du lịch nước ngoài quả là sự tình cờ may mắn tuyệt vời.'
      },
      {
        en: 'Penicillin was discovered through a famous act of scientific serendipity by Alexander Fleming.',
        vi: 'Thuốc kháng sinh Penicillin được phát hiện thông qua một sự tình cờ may mắn khoa học nổi tiếng của Alexander Fleming.'
      },
      {
        en: 'They met by sheer serendipity at an indie bookstore in Paris.',
        vi: 'Họ gặp nhau hoàn toàn do sự tình cờ duyên số tại một hiệu sách độc lập ở Paris.'
      }
    ],
    nuance_tips: 'Highly praised in IELTS Speaking & Writing for expressing serendipitous discoveries rather than plain "lucky coincidence".',
    source: 'lexicon'
  },
  'resilience': {
    word: new backend.Word({
      id: 1002,
      word: 'resilience',
      raw_word: 'resilience',
      pos: 'Noun',
      phonetic: '/rɪˈzɪl.jəns/',
      definition_en: 'The capacity to withstand or recover quickly from difficulties; toughness and adaptability.',
      definition_vi: 'Khả năng phục hồi, sự kiên cường bền bỉ vượt qua nghịch cảnh và tái tạo năng lượng.',
      example_en: 'Her emotional resilience allowed her to bounce back stronger after adversity.',
      example_vi: 'Sự kiên cường về mặt cảm xúc đã giúp cô ấy đứng dậy mạnh mẽ hơn sau nghịch cảnh.',
      level: 'C1 Advanced',
      topic: 'psychology',
      topic_title: 'Grit & Growth',
      topic_icon: '🌱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/resilience'
    }),
    isLocal: true,
    synonyms: ['toughness', 'adaptability', 'fortitude', 'grit', 'tenacity', 'hardiness'],
    antonyms: ['fragility', 'vulnerability', 'weakness', 'brittleness'],
    collocations: ['demonstrate resilience', 'build resilience', 'emotional resilience', 'economic resilience', 'remarkable resilience'],
    word_family: [
      { pos: 'Noun', word: 'resilience' },
      { pos: 'Adjective', word: 'resilient' },
      { pos: 'Adverb', word: 'resiliently' }
    ],
    etymology: 'From Latin "resilire", meaning "to rebound, leap back, spring back" (re- "back" + salire "to leap").',
    mnemonic_hook: 'Resilience sounds like "Re-silent strength" or a rubber band that always leaps back into shape after being stretched!',
    examples: [
      {
        en: 'Her emotional resilience allowed her to bounce back stronger after adversity.',
        vi: 'Sự kiên cường về mặt cảm xúc đã giúp cô ấy đứng dậy mạnh mẽ hơn sau nghịch cảnh.'
      },
      {
        en: 'The city demonstrated incredible resilience after the natural disaster.',
        vi: 'Thành phố đã thể hiện sự kiên cường đáng kinh ngạc sau thảm họa thiên nhiên.'
      },
      {
        en: 'Developing psychological resilience is crucial for modern high-pressure careers.',
        vi: 'Xây dựng khả năng phục hồi tâm lý là điều tối quan trọng đối với các nghề nghiệp áp lực cao ngày nay.'
      }
    ],
    nuance_tips: 'A staple vocabulary item in IELTS essays on psychology, education, and career development.',
    source: 'lexicon'
  },
  'ephemeral': {
    word: new backend.Word({
      id: 1003,
      word: 'ephemeral',
      raw_word: 'ephemeral',
      pos: 'Adjective',
      phonetic: '/ɪˈfem.ər.əl/',
      definition_en: 'Lasting for a very short time; fleeting, transient, and passing quickly.',
      definition_vi: 'Phù du, chóng tàn, thoáng qua, chỉ tồn tại trong một khoảng thời gian ngắn ngủi.',
      example_en: 'Social media fame is often ephemeral, fading within a few months.',
      example_vi: 'Sự nổi tiếng trên mạng xã hội thường chóng tàn, mờ nhạt dần chỉ trong vài tháng.',
      level: 'C2 Proficiency',
      topic: 'philosophy',
      topic_title: 'Time & Impermanence',
      topic_icon: '⏳',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ephemeral'
    }),
    isLocal: true,
    synonyms: ['transient', 'fleeting', 'short-lived', 'momentary', 'evanescent', 'fugitive'],
    antonyms: ['permanent', 'enduring', 'eternal', 'perpetual', 'lasting'],
    collocations: ['ephemeral beauty', 'ephemeral nature', 'ephemeral pleasure', 'ephemeral trends'],
    word_family: [
      { pos: 'Adjective', word: 'ephemeral' },
      { pos: 'Adverb', word: 'ephemerally' },
      { pos: 'Noun', word: 'ephemerality' }
    ],
    etymology: 'From Greek "ephemeros" (epi "upon" + hemera "day"), literally meaning "lasting only for a day", like mayflies.',
    mnemonic_hook: 'Ephemeral: think of "E-Females / Ephemera" blooming for just one day like cherry blossoms!',
    examples: [
      {
        en: 'Social media fame is often ephemeral, fading within a few months.',
        vi: 'Sự nổi tiếng trên mạng xã hội thường chóng tàn, mờ nhạt dần chỉ trong vài tháng.'
      },
      {
        en: 'Cherry blossoms represent the ephemeral beauty of life in Japanese philosophy.',
        vi: 'Hoa anh đào đại diện cho vẻ đẹp phù du, ngắn ngủi của cuộc sống trong triết học Nhật Bản.'
      }
    ],
    nuance_tips: 'Used in literary essays, philosophical topics, art critiques, and discussing digital trends.',
    source: 'lexicon'
  },
  'ubiquitous': {
    word: new backend.Word({
      id: 1004,
      word: 'ubiquitous',
      raw_word: 'ubiquitous',
      pos: 'Adjective',
      phonetic: '/juːˈbɪk.wə.təs/',
      definition_en: 'Present, appearing, or found everywhere at the same time; omnipresent.',
      definition_vi: 'Có mặt ở khắp mọi nơi, phổ biến rộng rãi khắp chốn cùng một lúc.',
      example_en: 'High-speed internet and smartphones have become ubiquitous worldwide.',
      example_vi: 'Internet tốc độ cao và điện thoại thông minh đã trở nên phổ biến ở khắp mọi nơi trên thế giới.',
      level: 'C1 Advanced',
      topic: 'technology',
      topic_title: 'Technology & Society',
      topic_icon: '📱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ubiquitous'
    }),
    isLocal: true,
    synonyms: ['omnipresent', 'everywhere', 'pervasive', 'universal', 'prevalent', 'widespread'],
    antonyms: ['rare', 'scarce', 'isolated', 'uncommon', 'infrequent'],
    collocations: ['become ubiquitous', 'ubiquitous presence', 'ubiquitous technology', 'almost ubiquitous'],
    word_family: [
      { pos: 'Adjective', word: 'ubiquitous' },
      { pos: 'Adverb', word: 'ubiquitously' },
      { pos: 'Noun', word: 'ubiquity' }
    ],
    etymology: 'From modern Latin "ubiquitarius", from Latin "ubique" meaning "everywhere" (ubi "where" + que "any").',
    mnemonic_hook: 'Ubiquitous: "You-Be-Everywhere-With-Us" = everywhere you look!',
    examples: [
      {
        en: 'High-speed internet and smartphones have become ubiquitous worldwide.',
        vi: 'Internet tốc độ cao và điện thoại thông minh đã trở nên phổ biến ở khắp mọi nơi trên thế giới.'
      },
      {
        en: 'Plastic waste has sadly become a ubiquitous feature of oceans worldwide.',
        vi: 'Rác thải nhựa đáng buồn đã trở thành một hiện diện có mặt khắp nơi ở các đại dương toàn cầu.'
      }
    ],
    nuance_tips: 'Top score booster in IELTS Writing Task 2 for technology, globalization, and urban life.',
    source: 'lexicon'
  },
  'eloquent': {
    word: new backend.Word({
      id: 1005,
      word: 'eloquent',
      raw_word: 'eloquent',
      pos: 'Adjective',
      phonetic: '/ˈel.ə.kwənt/',
      definition_en: 'Fluent or persuasive in speaking or writing; clearly and expressively conveying deep meaning.',
      definition_vi: 'Hùng biện, lưu loát, có khả năng diễn đạt truyền cảm và thuyết phục lòng người.',
      example_en: 'She delivered an eloquent defense of human rights at the summit.',
      example_vi: 'Cô ấy đã có bài phát biểu hùng biện đầy thuyết phục bảo vệ nhân quyền tại hội nghị thượng đỉnh.',
      level: 'B2 Upper-Intermediate',
      topic: 'communication',
      topic_title: 'Communication & Speech',
      topic_icon: '🎙️',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/eloquent'
    }),
    isLocal: true,
    synonyms: ['articulate', 'fluent', 'persuasive', 'expressive', 'silver-tongued', 'compelling'],
    antonyms: ['inarticulate', 'tongue-tied', 'hesitant', 'unconvincing'],
    collocations: ['eloquent speaker', 'eloquent testimony', 'eloquently expressed', 'eloquent plea'],
    word_family: [
      { pos: 'Adjective', word: 'eloquent' },
      { pos: 'Adverb', word: 'eloquently' },
      { pos: 'Noun', word: 'eloquence' }
    ],
    etymology: 'From Latin "eloqui" meaning "to speak out" (ex- "out" + loqui "to speak").',
    mnemonic_hook: 'Eloquent = "Elegant Speech" (Loqui = speak, like in dialogue & soliloquy).',
    examples: [
      {
        en: 'She delivered an eloquent defense of human rights at the summit.',
        vi: 'Cô ấy đã có bài phát biểu hùng biện đầy thuyết phục bảo vệ nhân quyền tại hội nghị thượng đỉnh.'
      },
      {
        en: 'His silence on the matter was an eloquent statement in itself.',
        vi: 'Sự im lặng của anh ấy về vấn đề này tự nó đã là một tuyên bố đầy ý nghĩa.'
      }
    ],
    nuance_tips: 'Can describe both spoken language, written prose, or meaningful symbolic actions.',
    source: 'lexicon'
  },
  'pragmatic': {
    word: new backend.Word({
      id: 1006,
      word: 'pragmatic',
      raw_word: 'pragmatic',
      pos: 'Adjective',
      phonetic: '/præɡˈmæt.ɪk/',
      definition_en: 'Dealing with things sensibly and realistically in a way that is based on practical rather than theoretical considerations.',
      definition_vi: 'Thực dụng, thực tế, đề cao tính ứng dụng và hiệu quả thực tế hơn là lý thuyết suông.',
      example_en: 'We need a pragmatic approach to solve this urgent engineering deadline.',
      example_vi: 'Chúng ta cần một phương pháp tiếp cận thực tế để giải quyết hạn chót kỹ thuật cấp bách này.',
      level: 'C1 Advanced',
      topic: 'strategy',
      topic_title: 'Strategy & Mindset',
      topic_icon: '🎯',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/pragmatic'
    }),
    isLocal: true,
    synonyms: ['practical', 'realistic', 'sensible', 'matter-of-fact', 'utilitarian', 'hands-on'],
    antonyms: ['idealistic', 'impractical', 'theoretical', 'visionary', 'utopian'],
    collocations: ['pragmatic approach', 'pragmatic solution', 'pragmatic decision', 'pragmatic leader'],
    word_family: [
      { pos: 'Adjective', word: 'pragmatic' },
      { pos: 'Adverb', word: 'pragmatically' },
      { pos: 'Noun', word: 'pragmatism' }
    ],
    etymology: 'From Greek "pragmatikos" meaning "fit for business or action" (pragma "deed, act").',
    mnemonic_hook: 'Pragmatic = "Practical Magic" — getting real things done in the real world!',
    examples: [
      {
        en: 'We need a pragmatic approach to solve this urgent engineering deadline.',
        vi: 'Chúng ta cần một phương pháp tiếp cận thực tế để giải quyết hạn chót kỹ thuật cấp bách này.'
      },
      {
        en: 'A pragmatic compromise was reached between both negotiating parties.',
        vi: 'Một thỏa hiệp thực tế mang tính xây dựng đã đạt được giữa cả hai bên đàm phán.'
      }
    ],
    nuance_tips: 'Often contrasted with idealistic or purely theoretical philosophies.',
    source: 'lexicon'
  },
  'procrastinate': {
    word: new backend.Word({
      id: 1007,
      word: 'procrastinate',
      raw_word: 'procrastinate',
      pos: 'Verb',
      phonetic: '/prəˈkræs.tə.neɪt/',
      definition_en: 'Delay or postpone action; habitually put off doing something that needs attention.',
      definition_vi: 'Trì hoãn, chần chừ, lần lữa không chịu bắt tay vào làm việc cần làm.',
      example_en: 'Don\'t procrastinate on your essay; starting early reduces exam anxiety.',
      example_vi: 'Đừng trì hoãn bài luận của bạn; bắt đầu sớm sẽ giúp giảm bớt lo âu trước kỳ thi.',
      level: 'B2 Upper-Intermediate',
      topic: 'habits',
      topic_title: 'Habits & Productivity',
      topic_icon: '⏰',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/procrastinate'
    }),
    isLocal: true,
    synonyms: ['delay', 'postpone', 'put off', 'dilly-dally', 'drag one\'s feet', 'defer'],
    antonyms: ['accelerate', 'expedite', 'act promptly', 'forge ahead'],
    collocations: ['tend to procrastinate', 'chronic procrastinator', 'procrastinate on tasks', 'stop procrastinating'],
    word_family: [
      { pos: 'Verb', word: 'procrastinate' },
      { pos: 'Noun', word: 'procrastination' },
      { pos: 'Noun', word: 'procrastinator' }
    ],
    etymology: 'From Latin "procrastinare" (pro- "forward, till" + crastinus "of tomorrow", from cras "tomorrow"). Literally "put off until tomorrow".',
    mnemonic_hook: 'Pro-crastinate = "Pro at putting things until cras (tomorrow)"!',
    examples: [
      {
        en: 'Don\'t procrastinate on your essay; starting early reduces exam anxiety.',
        vi: 'Đừng trì hoãn bài luận của bạn; bắt đầu sớm sẽ giúp giảm bớt lo âu trước kỳ thi.'
      },
      {
        en: 'Procrastination is often fueled by perfectionism rather than laziness.',
        vi: 'Sự trì hoãn thường bắt nguồn từ chủ nghĩa hoàn hảo hơn là do lười biếng.'
      }
    ],
    nuance_tips: 'Frequently used in discussions on time management, productivity, and study habits.',
    source: 'lexicon'
  }
};


/**
 * Searches for a word across:
 * 1. Built-in Lexicon (Instant 0ms)
 * 2. App Preloaded Vocab (<10ms)
 * 3. Online Free Dictionary API (~150ms ultra fast, e.g. for "work", "play")
 * 4. AI Structured Definition (On-demand or fallback)
 * 5. Synthesized Fallback (Zero crash guarantee)
 */
export async function lookupSmartDictionary(rawQuery: string, forceAI = false): Promise<SmartWordResult> {
  const query = rawQuery.trim().toLowerCase();
  if (!query) {
    throw new Error('Please enter a word to search');
  }

  // If forceAI is requested, jump directly to AI engine
  if (forceAI) {
    try {
      const aiResult = await lookupViaAI(query);
      if (aiResult) {
        return aiResult;
      }
    } catch (err) {
      console.warn('Force AI lookup failed, falling back:', err);
    }
  }

  // 1. Built-in Offline Lexicon Check
  if (OFFLINE_LEXICON[query]) {
    const item = OFFLINE_LEXICON[query];
    return {
      word: item.word!,
      isLocal: true,
      synonyms: item.synonyms || [],
      antonyms: item.antonyms || [],
      collocations: item.collocations || [],
      word_family: item.word_family || [],
      etymology: item.etymology || '',
      mnemonic_hook: item.mnemonic_hook || '',
      examples: item.examples || [],
      nuance_tips: item.nuance_tips || '',
      source: 'lexicon'
    };
  }

  // 2. Check App Preloaded Daily Vocab
  try {
    const dailyVocab = await GetDailyVocab('all', 100);
    if (dailyVocab && dailyVocab.length > 0) {
      const match = dailyVocab.find(
        (w) => w.word.toLowerCase() === query
      );
      if (match) {
        return {
          word: match,
          isLocal: true,
          source: 'app_vocab'
        };
      }
    }
  } catch (err) {
    console.warn('App vocab check skipped:', err);
  }

  // 3. Online Free Dictionary API (Ultra fast ~150ms for words like "work", "study", etc.)
  try {
    const onlineResult = await lookupViaOnlineAPI(query);
    if (onlineResult) {
      return onlineResult;
    }
  } catch (apiErr) {
    console.warn('Online dictionary API skipped or failed:', apiErr);
  }

  // 4. AI Smart Lookup & Structure Generation (Fallback for rare/slang/academic words)
  try {
    const aiResult = await lookupViaAI(query);
    if (aiResult) {
      return aiResult;
    }
  } catch (err) {
    console.warn('AI lookup encountered error, proceeding to synthesized fallback:', err);
  }

  // 5. Synthesized Fallback Entry (Never crash with Load Failed)
  return createSynthesizedEntry(query);
}

/**
 * Uses backend AI engine to generate rich, structured JSON for the word
 */
async function lookupViaAI(word: string): Promise<SmartWordResult | null> {
  const prompt = `You are an expert linguistic scholar and English-Vietnamese lexicographer. Provide an in-depth, structured dictionary entry for the English word "${word}".

Return ONLY a valid JSON object (no markdown formatting, no backticks, no outer text) with the following exact schema:
{
  "word": "${word}",
  "raw_word": "${word}",
  "pos": "Noun | Verb | Adjective | Adverb | Idiom | Phrasal Verb",
  "phonetic": "/IPA phonetic transcription/",
  "definition_en": "Clear, precise English definition",
  "definition_vi": "Nghĩa tiếng Việt chuẩn xác, giải thích rõ sắc thái",
  "example_en": "Natural primary example sentence showcasing the word in context",
  "example_vi": "Dịch câu ví dụ chính sang tiếng Việt tự nhiên",
  "level": "A1 | A2 | B1 | B2 | C1 | C2",
  "topic": "topic_slug",
  "topic_title": "Topic Name",
  "topic_icon": "relevant emoji",
  "dict_link": "https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}",
  "synonyms": ["synonym1", "synonym2", "synonym3", "synonym4", "synonym5"],
  "antonyms": ["antonym1", "antonym2", "antonym3"],
  "collocations": ["common collocation 1", "common collocation 2", "common collocation 3"],
  "word_family": [
    { "pos": "Noun", "word": "noun_form" },
    { "pos": "Verb", "word": "verb_form" },
    { "pos": "Adjective", "word": "adj_form" },
    { "pos": "Adverb", "word": "adv_form" }
  ],
  "etymology": "Concise origin and root explanation (e.g. Latin/Greek roots)",
  "mnemonic_hook": "A memorable association or memory hook to remember this word easily",
  "examples": [
    { "en": "Example sentence 1 in daily or academic context.", "vi": "Dịch ví dụ 1 sang tiếng Việt." },
    { "en": "Example sentence 2 in workplace or IELTS context.", "vi": "Dịch ví dụ 2 sang tiếng Việt." }
  ],
  "nuance_tips": "Key usage tips, register notes, or common pitfalls in IELTS Speaking/Writing"
}`;

  try {
    const rawResponse = await EvaluateWriting(
      `Dictionary Entry for: ${word}`,
      `Please parse and define the word: ${word}`,
      prompt
    );

    if (!rawResponse || typeof rawResponse !== 'string') {
      return null;
    }

    let cleanJson = rawResponse.trim();
    if (cleanJson.startsWith('```')) {
      cleanJson = cleanJson.replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '').trim();
    }

    const firstBrace = cleanJson.indexOf('{');
    const lastBrace = cleanJson.lastIndexOf('}');
    if (firstBrace !== -1 && lastBrace !== -1) {
      cleanJson = cleanJson.substring(firstBrace, lastBrace + 1);
    }

    const data = JSON.parse(cleanJson);
    if (!data.word || !data.definition_en) {
      return null;
    }

    const wordObj = new backend.Word({
      id: Date.now(),
      word: data.word || word,
      raw_word: data.raw_word || word,
      pos: data.pos || 'Word',
      phonetic: data.phonetic || '',
      definition_en: data.definition_en || '',
      definition_vi: data.definition_vi || '',
      example_en: data.example_en || '',
      example_vi: data.example_vi || '',
      level: data.level || 'B2 Upper-Intermediate',
      topic: data.topic || 'vocabulary',
      topic_title: data.topic_title || 'Smart Dictionary',
      topic_icon: data.topic_icon || '📖',
      dict_link: data.dict_link || `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
    });

    return {
      word: wordObj,
      isLocal: false,
      synonyms: Array.isArray(data.synonyms) ? data.synonyms : [],
      antonyms: Array.isArray(data.antonyms) ? data.antonyms : [],
      collocations: Array.isArray(data.collocations) ? data.collocations : [],
      word_family: Array.isArray(data.word_family) ? data.word_family : [],
      etymology: data.etymology || '',
      mnemonic_hook: data.mnemonic_hook || '',
      examples: Array.isArray(data.examples) && data.examples.length > 0 ? data.examples : [
        { en: data.example_en || '', vi: data.example_vi || '' }
      ],
      nuance_tips: data.nuance_tips || '',
      source: 'ai'
    };
  } catch (parseErr) {
    console.warn('AI lookup skipped:', parseErr);
    return null;
  }
}

/**
 * Free Dictionary API
 */
async function lookupViaOnlineAPI(word: string): Promise<SmartWordResult> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 4000);

  const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`;
  const resp = await fetch(url, { signal: controller.signal });
  clearTimeout(timeoutId);

  if (!resp.ok) {
    throw new Error(`Word "${word}" was not found in online dictionary.`);
  }

  const entries = await resp.json();
  if (!entries || !entries.length) {
    throw new Error(`No definition found for "${word}".`);
  }

  const entry = entries[0];
  const firstMeaning = entry.meanings?.[0];
  const firstDef = firstMeaning?.definitions?.[0];

  let phonetic = entry.phonetic || '';
  let audioUrl = '';
  if (entry.phonetics && entry.phonetics.length > 0) {
    for (const p of entry.phonetics) {
      if (p.text && !phonetic) phonetic = p.text;
      if (p.audio && !audioUrl) audioUrl = p.audio;
    }
  }

  const synonyms: string[] = [];
  const antonyms: string[] = [];

  for (const m of entry.meanings || []) {
    if (m.synonyms) synonyms.push(...m.synonyms);
    if (m.antonyms) antonyms.push(...m.antonyms);
    for (const d of m.definitions || []) {
      if (d.synonyms) synonyms.push(...d.synonyms);
      if (d.antonyms) antonyms.push(...d.antonyms);
    }
  }

  const wordObj = new backend.Word({
    id: Date.now(),
    word: entry.word || word,
    raw_word: entry.word || word,
    pos: firstMeaning?.partOfSpeech ? (firstMeaning.partOfSpeech.charAt(0).toUpperCase() + firstMeaning.partOfSpeech.slice(1)) : 'Word',
    phonetic: phonetic || '',
    definition_en: firstDef?.definition || 'Definition retrieved from online dictionary.',
    definition_vi: '',
    example_en: firstDef?.example || `Example sentence demonstrating the use of "${entry.word || word}".`,
    example_vi: '',
    level: 'B2 Intermediate',
    topic: 'vocabulary',
    topic_title: 'Online Dictionary',
    topic_icon: '🌐',
    dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
  });

  return {
    word: wordObj,
    isLocal: false,
    synonyms: [...new Set(synonyms)].slice(0, 6),
    antonyms: [...new Set(antonyms)].slice(0, 4),
    collocations: [],
    nuance_tips: '',
    source: 'online_dict',
    audioUrl
  };
}

/**
 * Creates a clean synthesized dictionary entry when offline
 */
function createSynthesizedEntry(word: string): SmartWordResult {
  const capitalized = word.charAt(0).toUpperCase() + word.slice(1);
  const wordObj = new backend.Word({
    id: Date.now(),
    word: word,
    raw_word: word,
    pos: 'Word',
    phonetic: `/${word}/`,
    definition_en: `Search query for "${capitalized}". Click external dictionaries below for comprehensive entries.`,
    definition_vi: `Từ khóa tra cứu "${capitalized}".`,
    example_en: `The word "${word}" is frequently used in academic and conversational English.`,
    example_vi: `Từ "${word}" thường được sử dụng trong tiếng Anh học thuật và giao tiếp.`,
    level: 'B2 Intermediate',
    topic: 'vocabulary',
    topic_title: 'Vocabulary Search',
    topic_icon: '📖',
    dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
  });

  return {
    word: wordObj,
    isLocal: false,
    synonyms: [],
    antonyms: [],
    collocations: [],
    nuance_tips: 'Open external dictionary links below to view in-depth phonetics, idioms, and grammar notes.',
    source: 'lexicon'
  };
}
