import { GetDailyVocab, GetSavedObsidianVocab, EvaluateWriting } from '../../../wailsjs/go/main/App.js';
import { backend } from '../../../wailsjs/go/models';

export interface SmartWordResult {
  word: backend.Word;
  isLocal: boolean;
  synonyms?: string[];
  antonyms?: string[];
  collocations?: string[];
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
      definition_vi: 'Sự tình cờ may mắn, sự may mắn bất ngờ tìm thấy điều tốt đẹp mà không cần chủ định.',
      example_en: 'Finding my dream job while on vacation was pure serendipity.',
      example_vi: 'Tìm được công việc mơ ước khi đang đi nghỉ quả là sự tình cờ may mắn tuyệt vời.',
      level: 'C2 Proficiency',
      topic: 'mindset',
      topic_title: 'Fortunate Coincidence',
      topic_icon: '🍀',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/serendipity'
    }),
    isLocal: true,
    synonyms: ['chance', 'fluke', 'happy accident', 'providence', 'blessing'],
    antonyms: ['misfortune', 'adversity', 'bad luck'],
    collocations: ['pure serendipity', 'stroke of serendipity', 'serendipity and luck'],
    nuance_tips: 'Often used to describe poetic, delightful discoveries made purely by coincidence.',
    source: 'lexicon'
  },
  'resilience': {
    word: new backend.Word({
      id: 1002,
      word: 'resilience',
      raw_word: 'resilience',
      pos: 'Noun',
      phonetic: '/rɪˈzɪl.jəns/',
      definition_en: 'The capacity to withstand or recover quickly from difficulties; toughness.',
      definition_vi: 'Khả năng phục hồi, sự kiên cường vượt qua nghịch cảnh hoặc thử thách.',
      example_en: 'Her resilience in overcoming obstacles inspired the entire team.',
      example_vi: 'Sự kiên cường vượt qua các trở ngại của cô ấy đã truyền cảm hứng cho cả đội ngũ.',
      level: 'C1 Advanced',
      topic: 'psychology',
      topic_title: 'Grit & Growth',
      topic_icon: '🌱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/resilience'
    }),
    isLocal: true,
    synonyms: ['toughness', 'adaptability', 'fortitude', 'grit', 'tenacity'],
    antonyms: ['fragility', 'vulnerability', 'weakness'],
    collocations: ['demonstrate resilience', 'emotional resilience', 'economic resilience'],
    nuance_tips: 'Key word for IELTS Speaking & Writing when discussing mental health and perseverance.',
    source: 'lexicon'
  },
  'ephemeral': {
    word: new backend.Word({
      id: 1003,
      word: 'ephemeral',
      raw_word: 'ephemeral',
      pos: 'Adjective',
      phonetic: '/ɪˈfem.ər.əl/',
      definition_en: 'Lasting for a very short time; fleeting or transient.',
      definition_vi: 'Phù du, chóng tàn, chỉ tồn tại trong một khoảng thời gian rất ngắn.',
      example_en: 'Fame in the internet age can be surprisingly ephemeral.',
      example_vi: 'Sự nổi tiếng trong thời đại internet có thể chóng tàn một cách đáng ngạc nhiên.',
      level: 'C2 Proficiency',
      topic: 'philosophy',
      topic_title: 'Time & Impermanence',
      topic_icon: '⏳',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ephemeral'
    }),
    isLocal: true,
    synonyms: ['transient', 'fleeting', 'short-lived', 'momentary', 'evanescent'],
    antonyms: ['permanent', 'enduring', 'eternal', 'perpetual'],
    collocations: ['ephemeral beauty', 'ephemeral nature', 'ephemeral pleasure'],
    nuance_tips: 'High-level academic word to describe beauty, trends, or moments that vanish quickly.',
    source: 'lexicon'
  },
  'ubiquitous': {
    word: new backend.Word({
      id: 1004,
      word: 'ubiquitous',
      raw_word: 'ubiquitous',
      pos: 'Adjective',
      phonetic: '/juːˈbɪk.wə.təs/',
      definition_en: 'Present, appearing, or found everywhere; omnipresent.',
      definition_vi: 'Có mặt ở khắp mọi nơi, phổ biến rộng rãi cùng lúc.',
      example_en: 'Smartphones have become ubiquitous in modern society.',
      example_vi: 'Điện thoại thông minh đã trở nên phổ biến ở khắp mọi nơi trong xã hội hiện đại.',
      level: 'C1 Advanced',
      topic: 'technology',
      topic_title: 'Technology & Society',
      topic_icon: '📱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ubiquitous'
    }),
    isLocal: true,
    synonyms: ['omnipresent', 'everywhere', 'pervasive', 'universal', 'prevalent'],
    antonyms: ['rare', 'scarce', 'isolated', 'uncommon'],
    collocations: ['become ubiquitous', 'ubiquitous presence', 'ubiquitous technology'],
    nuance_tips: 'Frequently used in IELTS essays about technology, AI, and digital media.',
    source: 'lexicon'
  },
  'eloquent': {
    word: new backend.Word({
      id: 1005,
      word: 'eloquent',
      raw_word: 'eloquent',
      pos: 'Adjective',
      phonetic: '/ˈel.ə.kwənt/',
      definition_en: 'Fluent or persuasive in speaking or writing; clearly expressing ideas.',
      definition_vi: 'Hùng biện, lưu loát, có khả năng diễn đạt thuyết phục và truyền cảm.',
      example_en: 'She gave an eloquent speech advocating for environmental protection.',
      example_vi: 'Cô ấy đã có bài phát biểu hùng biện đầy thuyết phục ủng hộ bảo vệ môi trường.',
      level: 'B2 Upper-Intermediate',
      topic: 'communication',
      topic_title: 'Communication & Speech',
      topic_icon: '🎙️',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/eloquent'
    }),
    isLocal: true,
    synonyms: ['articulate', 'fluent', 'persuasive', 'expressive', 'silver-tongued'],
    antonyms: ['inarticulate', 'tongue-tied', 'hesitant'],
    collocations: ['eloquent speaker', 'eloquent testimony', 'eloquently expressed'],
    nuance_tips: 'Describes communication that moves emotions and demonstrates exceptional eloquence.',
    source: 'lexicon'
  },
  'pragmatic': {
    word: new backend.Word({
      id: 1006,
      word: 'pragmatic',
      raw_word: 'pragmatic',
      pos: 'Adjective',
      phonetic: '/præɡˈmæt.ɪk/',
      definition_en: 'Dealing with things sensibly and realistically based on practical considerations.',
      definition_vi: 'Thực dụng, thực tế, dựa trên kinh nghiệm và hiệu quả thực tế hơn là lý thuyết.',
      example_en: 'We need a pragmatic approach to solve this complex logistical problem.',
      example_vi: 'Chúng ta cần một cách tiếp cận thực tế để giải quyết vấn đề hậu cần phức tạp này.',
      level: 'C1 Advanced',
      topic: 'strategy',
      topic_title: 'Strategy & Mindset',
      topic_icon: '🎯',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/pragmatic'
    }),
    isLocal: true,
    synonyms: ['practical', 'realistic', 'sensible', 'matter-of-fact', 'utilitarian'],
    antonyms: ['idealistic', 'impractical', 'theoretical', 'visionary'],
    collocations: ['pragmatic approach', 'pragmatic solution', 'pragmatic decision'],
    nuance_tips: 'Valuable word when discussing leadership, management, and problem solving.',
    source: 'lexicon'
  },
  'procrastinate': {
    word: new backend.Word({
      id: 1007,
      word: 'procrastinate',
      raw_word: 'procrastinate',
      pos: 'Verb',
      phonetic: '/prəˈkræs.tə.neɪt/',
      definition_en: 'Delay or postpone action; put off doing something that needs to be done.',
      definition_vi: 'Trì hoãn, chần chừ không chịu làm ngay việc cần làm.',
      example_en: 'Most students tend to procrastinate until the night before the final exam.',
      example_vi: 'Hầu hết sinh viên có xu hướng trì hoãn cho đến tận đêm trước ngày thi cuối kỳ.',
      level: 'B2 Upper-Intermediate',
      topic: 'habits',
      topic_title: 'Habits & Productivity',
      topic_icon: '⏰',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/procrastinate'
    }),
    isLocal: true,
    synonyms: ['delay', 'postpone', 'put off', 'dilly-dally', 'drag one\'s feet'],
    antonyms: ['accelerate', 'expedite', 'act promptly'],
    collocations: ['tend to procrastinate', 'chronic procrastinator', 'procrastinate on tasks'],
    nuance_tips: 'Commonly discussed in topics regarding time management and personal growth.',
    source: 'lexicon'
  }
};

/**
 * Searches for a word across:
 * 1. Built-in Lexicon
 * 2. Obsidian Vault
 * 3. Daily Vocab
 * 4. AI Structured Definition
 * 5. Online Free Dictionary API
 * 6. Synthesized Lexical Fallback
 */
export async function lookupSmartDictionary(rawQuery: string): Promise<SmartWordResult> {
  const query = rawQuery.trim().toLowerCase();
  if (!query) {
    throw new Error('Please enter a word to search');
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
      nuance_tips: item.nuance_tips || '',
      source: 'lexicon'
    };
  }

  // 2. Check Obsidian Vault
  try {
    const obsidianItems = await GetSavedObsidianVocab();
    if (obsidianItems && obsidianItems.length > 0) {
      const match = obsidianItems.find(
        (item) => item.word.toLowerCase() === query
      );
      if (match) {
        const wordObj = new backend.Word({
          id: Date.now(),
          word: match.word,
          raw_word: match.word,
          pos: match.pos || 'Word',
          phonetic: match.phonetic || '',
          definition_en: match.definition || '',
          definition_vi: '',
          example_en: match.example || '',
          example_vi: '',
          level: 'Vault Synced',
          topic: match.topic_key || 'vault',
          topic_title: match.topic_title || 'Saved in Vault',
          topic_icon: '📁',
          dict_link: match.dict_link || `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(match.word)}`
        });
        return {
          word: wordObj,
          isLocal: true,
          source: 'vault'
        };
      }
    }
  } catch (err) {
    console.warn('Obsidian lookup check skipped:', err);
  }

  // 3. Check App Preloaded Daily Vocab
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

  // 4. AI Smart Lookup & Structure Generation
  try {
    const aiResult = await lookupViaAI(query);
    if (aiResult) {
      return aiResult;
    }
  } catch (err) {
    console.warn('AI lookup encountered error, proceeding to online API:', err);
  }

  // 5. Online Dictionary API
  try {
    return await lookupViaOnlineAPI(query);
  } catch (apiErr) {
    console.warn('Online dictionary API unreachable:', apiErr);
  }

  // 6. Synthesized Fallback Entry (Never crash with Load Failed)
  return createSynthesizedEntry(query);
}

/**
 * Uses backend AI engine to generate rich, structured JSON for the word
 */
async function lookupViaAI(word: string): Promise<SmartWordResult | null> {
  const prompt = `You are a linguistic expert and English-Vietnamese lexicographer. Provide a detailed dictionary entry for the English word "${word}".

Return ONLY a valid JSON object (no markdown, no backticks, no wrapping text) with the following exact keys:
{
  "word": "${word}",
  "raw_word": "${word}",
  "pos": "Noun | Verb | Adjective | Adverb | Idiom | Phrasal Verb",
  "phonetic": "/IPA phonetic transcription/",
  "definition_en": "Clear, concise English definition",
  "definition_vi": "Nghĩa tiếng Việt chuẩn xác và dễ hiểu",
  "example_en": "A natural, modern example sentence showcasing the word",
  "example_vi": "Dịch câu ví dụ trên sang tiếng Việt tự nhiên",
  "level": "A1 | A2 | B1 | B2 | C1 | C2",
  "topic": "topic_slug",
  "topic_title": "Topic Name",
  "topic_icon": "relevant emoji",
  "dict_link": "https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}",
  "synonyms": ["synonym1", "synonym2", "synonym3", "synonym4"],
  "antonyms": ["antonym1", "antonym2"],
  "collocations": ["common collocation 1", "common collocation 2", "common collocation 3"],
  "nuance_tips": "Ngắn gọn về sắc thái từ hoặc mẹo dùng trong IELTS/giao tiếp"
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
