import { LookupWordInDB, SaveWordToDB, QueryAI } from '../../../wailsjs/go/main/App.js';
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
  debugLogs?: string[];
  executionTimeMs?: number;
}

/**
 * Robustly parses and splits bilingual example sentences from raw database strings,
 * cleaning noisy metadata like ": : id=com.petervn.ejdict..." and handling "/" or "|" delimiters.
 */
export function parseExamplePairs(rawEn: string | undefined | null, rawVi: string | undefined | null): BilingualExample[] {
  if (!rawEn) return [];

  const cleanString = (str: string) => {
    return str
      .replace(/:\s*:\s*id=[^"'\s]*/gi, '')
      .replace(/id=[a-zA-Z0-9._&=-]+/gi, '')
      .replace(/\s*\b\d{3,}\b\s*$/, '')
      .trim();
  };

  const cleanEn = cleanString(rawEn);
  const cleanVi = cleanString(rawVi || '');

  const splitSentences = (text: string) => {
    if (!text) return [];
    return text
      .split(/(?:\s*[/|]\s*|\r?\n+)/)
      .map(s => s.replace(/^["'“”\s]+|["'“”\s]+$/g, '').trim())
      .filter(s => s.length > 0);
  };

  const enParts = splitSentences(cleanEn);
  const viParts = splitSentences(cleanVi);

  if (enParts.length === 0) return [];

  const pairs: BilingualExample[] = [];
  for (let i = 0; i < enParts.length; i++) {
    pairs.push({
      en: enParts[i],
      vi: viParts[i] || (enParts.length === 1 ? (viParts[0] || '') : '')
    });
  }

  return pairs;
}

/**
 * Cleans and formats genuine word results without fabricating fake data
 */
export function ensureRichUnifiedResult(result: SmartWordResult): SmartWordResult {
  const w = result.word as any;

  // 1. Examples
  let examples: BilingualExample[] = [];
  if (result.examples && result.examples.length > 0) {
    examples = result.examples.map(ex => ({
      en: ex.en.replace(/:\s*:\s*id=[^"'\s]*/gi, '').replace(/id=[a-zA-Z0-9._&=-]+/gi, '').replace(/\s*\b\d{3,}\b\s*$/, '').trim(),
      vi: ex.vi.replace(/:\s*:\s*id=[^"'\s]*/gi, '').replace(/id=[a-zA-Z0-9._&=-]+/gi, '').replace(/\s*\b\d{3,}\b\s*$/, '').trim()
    }));
  } else if (w.examples_json && w.examples_json !== '[]') {
    try {
      const parsed = JSON.parse(w.examples_json);
      if (Array.isArray(parsed) && parsed.length > 0) {
        examples = parsed.map(ex => ({
          en: (ex.en || '').replace(/:\s*:\s*id=[^"'\s]*/gi, '').replace(/id=[a-zA-Z0-9._&=-]+/gi, '').replace(/\s*\b\d{3,}\b\s*$/, '').trim(),
          vi: (ex.vi || '').replace(/:\s*:\s*id=[^"'\s]*/gi, '').replace(/id=[a-zA-Z0-9._&=-]+/gi, '').replace(/\s*\b\d{3,}\b\s*$/, '').trim()
        }));
      }
    } catch {}
  }

  if (examples.length === 0 && w.example_en) {
    examples = parseExamplePairs(w.example_en, w.example_vi);
  }

  // 2. Word Family
  let word_family: WordFamilyMember[] = result.word_family || [];
  if (word_family.length === 0 && w.word_family_json && w.word_family_json !== '[]') {
    try {
      const parsed = JSON.parse(w.word_family_json);
      if (Array.isArray(parsed)) word_family = parsed;
    } catch {}
  }

  // 3. Synonyms & Antonyms
  let synonyms: string[] = result.synonyms || [];
  if (synonyms.length === 0 && w.synonyms_json && w.synonyms_json !== '[]') {
    try {
      const parsed = JSON.parse(w.synonyms_json);
      if (Array.isArray(parsed)) synonyms = parsed;
    } catch {}
  }

  let antonyms: string[] = result.antonyms || [];
  if (antonyms.length === 0 && w.antonyms_json && w.antonyms_json !== '[]') {
    try {
      const parsed = JSON.parse(w.antonyms_json);
      if (Array.isArray(parsed)) antonyms = parsed;
    } catch {}
  }

  // 4. Collocations
  let collocations: string[] = result.collocations || [];
  if (collocations.length === 0 && w.collocations_json && w.collocations_json !== '[]') {
    try {
      const parsed = JSON.parse(w.collocations_json);
      if (Array.isArray(parsed)) collocations = parsed;
    } catch {}
  }

  // 5. Etymology
  let etymology = result.etymology || w.etymology || '';

  // 6. Nuance tips
  let nuance_tips = result.nuance_tips || w.nuance_tips || '';

  return {
    ...result,
    examples,
    word_family,
    synonyms,
    antonyms,
    collocations,
    etymology,
    nuance_tips
  };
}

/**
 * Intelligent Multi-Tier Orchestrator for Lexicon Lookups
 */
export async function smartLookup(
  term: string, 
  onLog?: (msg: string) => void
): Promise<SmartWordResult | null> {
  const cleanTerm = term.trim().toLowerCase();
  if (!cleanTerm) return null;

  const logs: string[] = [];
  const log = (msg: string) => {
    logs.push(msg);
    if (onLog) onLog(msg);
  };

  const startTime = performance.now();
  log(`🔍 Pipeline initialized for term: "${cleanTerm}"`);

  // Tier 1: Local SQLite Dictionary Lookup (Instant sub-5ms)
  try {
    log(`[Tier 1] Querying embedded SQLite dictionary database...`);
    const dbWord = await LookupWordInDB(cleanTerm);
    
    if (dbWord && dbWord.id > 0) {
      log(`✅ SQLite HIT! Retrieved 6-block lexical record for "${dbWord.word}".`);
      
      const rawResult: SmartWordResult = {
        word: dbWord,
        isLocal: true,
        source: 'lexicon',
        debugLogs: logs,
        executionTimeMs: Math.round(performance.now() - startTime)
      };

      const unified = ensureRichUnifiedResult(rawResult);

      if (!unified.word.definition_vi || unified.examples?.length === 0) {
        log(`⚠️ SQLite HIT for "${dbWord.word}", but record is incomplete (missing Vietnamese definitions/examples). Auto-upgrading via AI...`);
        try {
          const enriched = await enrichWordWithAI(cleanTerm, unified, log);
          enriched.debugLogs = logs;
          enriched.executionTimeMs = Math.round(performance.now() - startTime);
          return enriched;
        } catch (enrichErr) {
          log(`⚠️ AI background upgrade skipped: ${enrichErr}`);
          return unified;
        }
      }

      return unified;
    } else {
      log(`[Tier 1] SQLite MISS for "${cleanTerm}". Escalating to Tier 2 AI Enrichment...`);
    }
  } catch (err) {
    log(`⚠️ Tier 1 SQLite query failed: ${err}`);
  }

  // Tier 2: AI Deep Enrichment
  try {
    log(`[Tier 2] Invoking AI Provider to synthesize structured lexical dataset...`);
    const aiResult = await enrichWordWithAI(cleanTerm, null, log);
    aiResult.debugLogs = logs;
    aiResult.executionTimeMs = Math.round(performance.now() - startTime);
    return aiResult;
  } catch (aiErr) {
    log(`❌ Tier 2 AI synthesis error: ${aiErr}`);
  }

  return null;
}

/**
 * Calls AI Engine to generate Oxford 6-block structured data
 */
async function enrichWordWithAI(
  term: string, 
  existing: SmartWordResult | null,
  log: (msg: string) => void
): Promise<SmartWordResult> {
  const prompt = `You are an elite Oxford lexicographer.
Provide comprehensive, structured linguistic data for the English word or phrase: "${term}".

Respond STRICTLY with a valid JSON object without markdown fences, formatting, or commentary.
Required JSON schema:
{
  "word": "${term}",
  "pos": "noun/verb/adjective/idiom...",
  "phonetic": "/.../",
  "definition_en": "Clear Oxford-style definition in English",
  "definition_vi": "Bản dịch nghĩa tiếng Việt chính xác, súc tích",
  "examples": [
    { "en": "Example sentence in English 1.", "vi": "Bản dịch câu ví dụ 1 tiếng Việt." },
    { "en": "Example sentence in English 2.", "vi": "Bản dịch câu ví dụ 2 tiếng Việt." }
  ],
  "synonyms": ["syn1", "syn2", "syn3"],
  "antonyms": ["ant1", "ant2"],
  "collocations": ["collocation 1", "collocation 2", "collocation 3"],
  "word_family": [
    { "pos": "noun", "word": "..." },
    { "pos": "verb", "word": "..." },
    { "pos": "adjective", "word": "..." }
  ],
  "etymology": "Latin/Greek roots and morphological history",
  "nuance_tips": "Practical usage notes or common learner traps"
}`;

  log(`🤖 Sending payload to AI engine...`);
  const responseRaw = await QueryAI(prompt);
  
  let jsonStr = responseRaw.trim();
  if (jsonStr.startsWith('```json')) {
    jsonStr = jsonStr.replace(/^```json\s*/, '').replace(/```\s*$/, '');
  } else if (jsonStr.startsWith('```')) {
    jsonStr = jsonStr.replace(/^```\s*/, '').replace(/```\s*$/, '');
  }

  const data = JSON.parse(jsonStr);
  log(`✨ AI generated valid Oxford 6-block lexical schema.`);

  const newWord: backend.Word = {
    id: existing?.word?.id || 0,
    word: data.word || term,
    pos: data.pos || 'noun',
    phonetic: data.phonetic || '/.../',
    definition_en: data.definition_en || '',
    definition_vi: data.definition_vi || '',
    example_en: data.examples?.[0]?.en || '',
    example_vi: data.examples?.[0]?.vi || '',
    topic_key: existing?.word?.topic_key || 'ai_enriched',
    topic_title: existing?.word?.topic_title || 'AI Enriched',
    dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(term)}`,
    mastery_level: 0,
    review_count: 0,
    last_reviewed_at: '',
    next_review_at: '',
    srs_interval_days: 1,
    srs_ease_factor: 2.5
  };

  const wordWithExtras: any = {
    ...newWord,
    examples_json: JSON.stringify(data.examples || []),
    synonyms_json: JSON.stringify(data.synonyms || []),
    antonyms_json: JSON.stringify(data.antonyms || []),
    collocations_json: JSON.stringify(data.collocations || []),
    word_family_json: JSON.stringify(data.word_family || []),
    etymology: data.etymology || '',
    nuance_tips: data.nuance_tips || ''
  };

  // Persist into SQLite cache
  try {
    await SaveWordToDB(wordWithExtras);
    log(`💾 Stored complete enriched entry for "${term}" into local SQLite cache.`);
  } catch (saveErr) {
    log(`⚠️ Failed to persist word into SQLite: ${saveErr}`);
  }

  return {
    word: newWord,
    isLocal: false,
    source: 'ai',
    synonyms: data.synonyms || [],
    antonyms: data.antonyms || [],
    collocations: data.collocations || [],
    word_family: data.word_family || [],
    etymology: data.etymology || '',
    nuance_tips: data.nuance_tips || '',
    examples: data.examples || []
  };
}

export const lookupSmartDictionary = smartLookup;
