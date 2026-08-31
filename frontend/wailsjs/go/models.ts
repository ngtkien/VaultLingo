export namespace backend {
	
	export class Config {
	    obsidian_vault_path: string;
	    ai_provider: string;
	    agy_model: string;
	    agy_path: string;
	    agy_effort?: string;
	    openrouter_api_key: string;
	    openrouter_model: string;
	    groq_api_key: string;
	    groq_model: string;
	    ollama_url: string;
	    ollama_model: string;
	    auto_play_audio: boolean;
	    default_audio_speed: number;
	
	    static createFrom(source: any = {}) {
	        return new Config(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.obsidian_vault_path = source["obsidian_vault_path"];
	        this.ai_provider = source["ai_provider"];
	        this.agy_model = source["agy_model"];
	        this.agy_path = source["agy_path"];
	        this.agy_effort = source["agy_effort"];
	        this.openrouter_api_key = source["openrouter_api_key"];
	        this.openrouter_model = source["openrouter_model"];
	        this.groq_api_key = source["groq_api_key"];
	        this.groq_model = source["groq_model"];
	        this.ollama_url = source["ollama_url"];
	        this.ollama_model = source["ollama_model"];
	        this.auto_play_audio = source["auto_play_audio"];
	        this.default_audio_speed = source["default_audio_speed"];
	    }
	}
	export class Dictation {
	    id: number;
	    level: string;
	    level_color: string;
	    category: string;
	    category_icon: string;
	    sentence: string;
	    sentence_vi: string;
	    hint: string;
	
	    static createFrom(source: any = {}) {
	        return new Dictation(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.id = source["id"];
	        this.level = source["level"];
	        this.level_color = source["level_color"];
	        this.category = source["category"];
	        this.category_icon = source["category_icon"];
	        this.sentence = source["sentence"];
	        this.sentence_vi = source["sentence_vi"];
	        this.hint = source["hint"];
	    }
	}
	export class DiffToken {
	    type: string;
	    word: string;
	    match?: string;
	
	    static createFrom(source: any = {}) {
	        return new DiffToken(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.type = source["type"];
	        this.word = source["word"];
	        this.match = source["match"];
	    }
	}
	export class DictationResult {
	    accuracy: number;
	    passed: boolean;
	    tokens: DiffToken[];
	
	    static createFrom(source: any = {}) {
	        return new DictationResult(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.accuracy = source["accuracy"];
	        this.passed = source["passed"];
	        this.tokens = this.convertValues(source["tokens"], DiffToken);
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}
	
	export class Idiom {
	    id: number;
	    idiom: string;
	    phonetic: string;
	    meaning_en: string;
	    meaning_vi: string;
	    example: string;
	    example_vi: string;
	
	    static createFrom(source: any = {}) {
	        return new Idiom(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.id = source["id"];
	        this.idiom = source["idiom"];
	        this.phonetic = source["phonetic"];
	        this.meaning_en = source["meaning_en"];
	        this.meaning_vi = source["meaning_vi"];
	        this.example = source["example"];
	        this.example_vi = source["example_vi"];
	    }
	}
	export class ListeningQA {
	    q: string;
	    a: string;
	
	    static createFrom(source: any = {}) {
	        return new ListeningQA(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.q = source["q"];
	        this.a = source["a"];
	    }
	}
	export class ListeningTopic {
	    id: number;
	    topic_id: number;
	    title: string;
	    icon: string;
	    audio: string;
	    url: string;
	    qa: ListeningQA[];
	
	    static createFrom(source: any = {}) {
	        return new ListeningTopic(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.id = source["id"];
	        this.topic_id = source["topic_id"];
	        this.title = source["title"];
	        this.icon = source["icon"];
	        this.audio = source["audio"];
	        this.url = source["url"];
	        this.qa = this.convertValues(source["qa"], ListeningQA);
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}
	export class ObsidianItem {
	    word: string;
	    pos: string;
	    phonetic: string;
	    definition: string;
	    example: string;
	    topic_key: string;
	    topic_title: string;
	    dict_link: string;
	    file_path: string;
	    next_review: string;
	    interval: number;
	    repetitions: number;
	    status: string;
	    is_due: boolean;
	
	    static createFrom(source: any = {}) {
	        return new ObsidianItem(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.word = source["word"];
	        this.pos = source["pos"];
	        this.phonetic = source["phonetic"];
	        this.definition = source["definition"];
	        this.example = source["example"];
	        this.topic_key = source["topic_key"];
	        this.topic_title = source["topic_title"];
	        this.dict_link = source["dict_link"];
	        this.file_path = source["file_path"];
	        this.next_review = source["next_review"];
	        this.interval = source["interval"];
	        this.repetitions = source["repetitions"];
	        this.status = source["status"];
	        this.is_due = source["is_due"];
	    }
	}
	export class ObsidianSaveResult {
	    success: boolean;
	    word?: string;
	    file?: string;
	    error?: string;
	
	    static createFrom(source: any = {}) {
	        return new ObsidianSaveResult(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.success = source["success"];
	        this.word = source["word"];
	        this.file = source["file"];
	        this.error = source["error"];
	    }
	}
	export class Quiz {
	    id: number;
	    category: string;
	    category_icon: string;
	    question: string;
	    options: string[];
	    correct: string;
	    correct_sentence: string;
	    explanation: string;
	    tip: string;
	
	    static createFrom(source: any = {}) {
	        return new Quiz(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.id = source["id"];
	        this.category = source["category"];
	        this.category_icon = source["category_icon"];
	        this.question = source["question"];
	        this.options = source["options"];
	        this.correct = source["correct"];
	        this.correct_sentence = source["correct_sentence"];
	        this.explanation = source["explanation"];
	        this.tip = source["tip"];
	    }
	}
	export class Word {
	    id: number;
	    word: string;
	    raw_word: string;
	    pos: string;
	    phonetic: string;
	    definition_en: string;
	    definition_vi: string;
	    example_en: string;
	    example_vi: string;
	    level: string;
	    topic: string;
	    topic_title: string;
	    topic_icon: string;
	    dict_link: string;
	    interval?: number;
	    repetitions?: number;
	    ease_factor?: number;
	    next_review?: string;
	    status?: string;
	    synonyms_json?: string;
	    antonyms_json?: string;
	    collocations_json?: string;
	    word_family_json?: string;
	    etymology?: string;
	    mnemonic_hook?: string;
	    nuance_tips?: string;
	    examples_json?: string;
	
	    static createFrom(source: any = {}) {
	        return new Word(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.id = source["id"];
	        this.word = source["word"];
	        this.raw_word = source["raw_word"];
	        this.pos = source["pos"];
	        this.phonetic = source["phonetic"];
	        this.definition_en = source["definition_en"];
	        this.definition_vi = source["definition_vi"];
	        this.example_en = source["example_en"];
	        this.example_vi = source["example_vi"];
	        this.level = source["level"];
	        this.topic = source["topic"];
	        this.topic_title = source["topic_title"];
	        this.topic_icon = source["topic_icon"];
	        this.dict_link = source["dict_link"];
	        this.interval = source["interval"];
	        this.repetitions = source["repetitions"];
	        this.ease_factor = source["ease_factor"];
	        this.next_review = source["next_review"];
	        this.status = source["status"];
	        this.synonyms_json = source["synonyms_json"];
	        this.antonyms_json = source["antonyms_json"];
	        this.collocations_json = source["collocations_json"];
	        this.word_family_json = source["word_family_json"];
	        this.etymology = source["etymology"];
	        this.mnemonic_hook = source["mnemonic_hook"];
	        this.nuance_tips = source["nuance_tips"];
	        this.examples_json = source["examples_json"];
	    }
	}
	export class WritingPrompt {
	    id: number;
	    level: string;
	    title: string;
	    category: string;
	    category_icon: string;
	    target_min: number;
	    target_max: number;
	    situation_vi: string;
	    prompt: string;
	    sentence_starters: string[];
	    guide_tips: string[];
	    suggested_vocab: string[];
	
	    static createFrom(source: any = {}) {
	        return new WritingPrompt(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.id = source["id"];
	        this.level = source["level"];
	        this.title = source["title"];
	        this.category = source["category"];
	        this.category_icon = source["category_icon"];
	        this.target_min = source["target_min"];
	        this.target_max = source["target_max"];
	        this.situation_vi = source["situation_vi"];
	        this.prompt = source["prompt"];
	        this.sentence_starters = source["sentence_starters"];
	        this.guide_tips = source["guide_tips"];
	        this.suggested_vocab = source["suggested_vocab"];
	    }
	}

}

