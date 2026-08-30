import { LookupWordInDB, SaveWordToDB, EvaluateWriting } from '../../../wailsjs/go/main/App.js';
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

/**
 * Cleans and formats genuine word results without fabricating fake data
 */
export function ensureRichUnifiedResult(result: SmartWordResult): SmartWordResult {
  // Clean and parse examples
  let examples: BilingualExample[] = [];
  if (result.examples && result.examples.length > 0) {
    examples = result.examples;
  } else if (result.word.example_en) {
    const rawEn = result.word.example_en;
    const rawVi = result.word.example_vi || '';

    // Split on | if multiple sentences were bundled together, remove trailing noise
    const enParts = rawEn.split('|').map(s => s.replace(/\s*\b\d{3,}\b\s*$/, '').trim()).filter(Boolean);
    const viParts = rawVi.split('|').map(s => s.replace(/\s*\b\d{3,}\b\s*$/, '').trim()).filter(Boolean);

    for (let i = 0; i < enParts.length; i++) {
      examples.push({
        en: enParts[i],
        vi: viParts[i] || viParts[0] || ''
      });
    }
  }

  return {
    ...result,
    examples,
    word_family: result.word_family || [],
    etymology: result.etymology || '',
    collocations: result.collocations || [],
    synonyms: result.synonyms || [],
    antonyms: result.antonyms || [],
    mnemonic_hook: result.mnemonic_hook || '',
    nuance_tips: result.nuance_tips || ''
  };
}

/**
 * Searches for a word across:
 * 1. Native SQLite Database file (vocab.db via LookupWordInDB) - 0ms
 * 2. Online Dictionary API (Oxford/Cambridge phonetics & definition)
 * 3. AI Structured Synthesis into 6-block template -> Auto-saved to SQLite DB!
 * 4. Honest Clean Fallback with direct Oxford/Cambridge links
 */
export async function lookupSmartDictionary(rawQuery: string, forceAI = false): Promise<SmartWordResult> {
  const query = rawQuery.trim().toLowerCase();
  if (!query) {
    throw new Error('Please enter a word to search');
  }

  // If forceAI is explicitly requested (via "AI Deep Enrich ✨"), run AI engine & save to SQLite DB
  if (forceAI) {
    try {
      const aiResult = await lookupViaAI(query);
      if (aiResult) {
        try {
          await SaveWordToDB(aiResult.word);
        } catch (dbErr) {
          console.warn('Failed saving AI word to SQLite DB:', dbErr);
        }
        return ensureRichUnifiedResult(aiResult);
      }
    } catch (err) {
      console.warn('Force AI lookup failed, falling back:', err);
    }
  }

  // 1. Native SQLite Database File Lookup (Instant 0ms from vocab.db)
  try {
    const dbWord = await LookupWordInDB(query);
    if (dbWord && dbWord.word) {
      const res: SmartWordResult = {
        word: dbWord,
        isLocal: true,
        source: 'app_vocab'
      };
      return ensureRichUnifiedResult(res);
    }
  } catch (err) {
    // Word not found in SQLite yet, proceed to Online / AI pipeline
  }

  // 2. Online Dictionary API + AI Template Synthesis
  try {
    const onlineData = await lookupViaOnlineAPI(query);
    const aiResult = await lookupViaAI(query, onlineData);
    if (aiResult) {
      // Auto-save the AI-structured word directly into SQLite DB (vocab.db)
      try {
        await SaveWordToDB(aiResult.word);
      } catch (dbErr) {
        console.warn('Failed auto-saving word to SQLite DB:', dbErr);
      }
      return ensureRichUnifiedResult(aiResult);
    }

    if (onlineData) {
      try {
        await SaveWordToDB(onlineData.word);
      } catch (dbErr) {
        console.warn('Failed saving online word to SQLite DB:', dbErr);
      }
      return ensureRichUnifiedResult(onlineData);
    }
  } catch (aiErr) {
    console.warn('Online & AI dictionary lookup fallback:', aiErr);
  }

  // 3. Clean Honest Fallback Entry (No slop, clear Cambridge/Oxford/Longman links)
  const synth = createSynthesizedEntry(query);
  return ensureRichUnifiedResult(synth);
}

/**
 * Uses backend AI engine with Oxford lexicographer standards to generate rich, structured JSON for the word
 */
async function lookupViaAI(word: string, onlineContext?: SmartWordResult | null): Promise<SmartWordResult | null> {
  const contextNote = onlineContext
    ? `Online Phonetic: ${onlineContext.word.phonetic || ''}, Raw Definition: ${onlineContext.word.definition_en || ''}`
    : '';

  const prompt = `You are a distinguished Oxford lexicographer and English-Vietnamese linguist.
Create an accurate, authentic dictionary entry for the English word "${word}".
${contextNote}

Return ONLY valid JSON (no markdown formatting, no backticks, no markdown codeblock tags) strictly matching this schema:
{
  "word": "${word}",
  "raw_word": "${word}",
  "pos": "Noun | Verb | Adjective | Adverb | Phrasal Verb | Idiom",
  "phonetic": "/IPA transcription/",
  "definition_en": "Accurate, clear English definition (Oxford/Cambridge standard)",
  "definition_vi": "Nghĩa tiếng Việt chuẩn mực, tự nhiên, giải thích rõ sắc thái",
  "example_en": "Natural authentic example sentence showcasing the word in context",
  "example_vi": "Bản dịch tiếng Việt tự nhiên của câu ví dụ",
  "level": "A1 | A2 | B1 | B2 | C1 | C2",
  "topic": "topic_slug",
  "topic_title": "Topic Title",
  "topic_icon": "emoji",
  "dict_link": "https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}",
  "synonyms": ["real_synonym_1", "real_synonym_2", "real_synonym_3"],
  "antonyms": ["real_antonym_1", "real_antonym_2"],
  "collocations": ["natural collocation 1", "natural collocation 2", "natural collocation 3"],
  "word_family": [
    { "pos": "Noun", "word": "real_noun_form" },
    { "pos": "Verb", "word": "real_verb_form" },
    { "pos": "Adjective", "word": "real_adj_form" }
  ],
  "etymology": "Concise historical root origin (e.g. Latin/Greek/Old English root)",
  "mnemonic_hook": "A clever, memorable memory hook to remember this word easily",
  "examples": [
    { "en": "Example sentence 1 in daily or academic context.", "vi": "Dịch ví dụ 1 sang tiếng Việt." },
    { "en": "Example sentence 2 in workplace or IELTS context.", "vi": "Dịch ví dụ 2 sang tiếng Việt." }
  ],
  "nuance_tips": "Key usage tips or common errors to avoid in IELTS Speaking/Writing"
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
 * Free Dictionary API with short 1.5s timeout
 */
async function lookupViaOnlineAPI(word: string): Promise<SmartWordResult | null> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 1500);

  try {
    const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`;
    const resp = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (!resp.ok) {
      return null;
    }

    const entries = await resp.json();
    if (!entries || !entries.length) {
      return null;
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
      phonetic: phonetic || `/${word}/`,
      definition_en: firstDef?.definition || 'Definition retrieved from international dictionary.',
      definition_vi: '',
      example_en: firstDef?.example || `Natural usage example for "${entry.word || word}".`,
      example_vi: '',
      level: 'B1 Intermediate',
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
  } catch (err) {
    clearTimeout(timeoutId);
    return null;
  }
}

/**
 * Creates an honest, clean dictionary entry prompt when offline data is unavailable
 */
function createSynthesizedEntry(word: string): SmartWordResult {
  const capitalized = word.charAt(0).toUpperCase() + word.slice(1);
  const wordObj = new backend.Word({
    id: Date.now(),
    word: word,
    raw_word: word,
    pos: 'Word',
    phonetic: `/${word}/`,
    definition_en: `Click "AI Deep Enrich ✨" or choose an external dictionary below (Cambridge, Oxford, Longman, Merriam-Webster) to explore complete definitions and usage notes for "${capitalized}".`,
    definition_vi: `Chọn "AI Deep Enrich ✨" hoặc bấm các liên kết từ điển bên dưới để xem chi tiết toàn bộ nghĩa, phiên âm và ví dụ cho từ "${capitalized}".`,
    example_en: `Search query: "${word}". Explore comprehensive entries via official dictionary links below.`,
    example_vi: `Từ khóa: "${word}". Khám phá chi tiết qua các liên kết từ điển chính thống bên dưới.`,
    level: 'Vocabulary',
    topic: 'vocabulary',
    topic_title: 'Dictionary Lookup',
    topic_icon: '📖',
    dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
  });

  return {
    word: wordObj,
    isLocal: true,
    synonyms: [],
    antonyms: [],
    collocations: [],
    nuance_tips: 'Click "AI Deep Enrich ✨" for in-depth AI linguistic analysis, or open external dictionary links below.',
    source: 'lexicon'
  };
}
