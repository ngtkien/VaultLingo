package backend

type Word struct {
	ID               int     `json:"id"`
	Word             string  `json:"word"`
	RawWord          string  `json:"raw_word"`
	POS              string  `json:"pos"`
	Phonetic         string  `json:"phonetic"`
	DefinitionEn     string  `json:"definition_en"`
	DefinitionVi     string  `json:"definition_vi"`
	ExampleEn        string  `json:"example_en"`
	ExampleVi        string  `json:"example_vi"`
	Level            string  `json:"level"`
	Topic            string  `json:"topic"`
	TopicTitle       string  `json:"topic_title"`
	TopicIcon        string  `json:"topic_icon"`
	DictLink         string  `json:"dict_link"`
	Interval         int     `json:"interval,omitempty"`
	Repetitions      int     `json:"repetitions,omitempty"`
	EaseFactor       float64 `json:"ease_factor,omitempty"`
	NextReview       string  `json:"next_review,omitempty"`
	Status           string  `json:"status,omitempty"`
	SynonymsJSON     string  `json:"synonyms_json,omitempty"`
	AntonymsJSON     string  `json:"antonyms_json,omitempty"`
	CollocationsJSON string  `json:"collocations_json,omitempty"`
	WordFamilyJSON   string  `json:"word_family_json,omitempty"`
	Etymology        string  `json:"etymology,omitempty"`
	MnemonicHook     string  `json:"mnemonic_hook,omitempty"`
	NuanceTips       string  `json:"nuance_tips,omitempty"`
	ExamplesJSON     string  `json:"examples_json,omitempty"`
}
type Idiom struct {
	ID        int    `json:"id"`
	Idiom     string `json:"idiom"`
	Phonetic  string `json:"phonetic"`
	MeaningEn string `json:"meaning_en"`
	MeaningVi string `json:"meaning_vi"`
	Example   string `json:"example"`
	ExampleVi string `json:"example_vi"`
}

type Quiz struct {
	ID              int      `json:"id"`
	Category        string   `json:"category"`
	CategoryIcon    string   `json:"category_icon"`
	Question        string   `json:"question"`
	Options         []string `json:"options"`
	Correct         string   `json:"correct"`
	CorrectSentence string   `json:"correct_sentence"`
	Explanation     string   `json:"explanation"`
	Tip             string   `json:"tip"`
}

type Dictation struct {
	ID           int    `json:"id"`
	Level        string `json:"level"`
	LevelColor   string `json:"level_color"`
	Category     string `json:"category"`
	CategoryIcon string `json:"category_icon"`
	Sentence     string `json:"sentence"`
	SentenceVi   string `json:"sentence_vi"`
	Hint         string `json:"hint"`
}

type DictationCategoryInfo struct {
	Category     string `json:"category"`
	CategoryIcon string `json:"category_icon"`
	Count        int    `json:"count"`
}

type DictationLevelInfo struct {
	Level      string `json:"level"`
	LevelColor string `json:"level_color"`
	Count      int    `json:"count"`
}

type GrammarDrill struct {
	ID             int      `json:"id"`
	Type           string   `json:"type"` // "question_form", "tense_shift", "tag_question", "indirect"
	TenseCategory  string   `json:"tense_category"` // "Present Simple", "Past Simple", "Present Perfect", etc.
	CategoryIcon   string   `json:"category_icon"`
	Level          string   `json:"level"`
	PromptContext  string   `json:"prompt_context"`
	PromptVi       string   `json:"prompt_vi"`
	Instruction    string   `json:"instruction"`
	TargetQuestion string   `json:"target_question"`
	TargetVi       string   `json:"target_vi"`
	QuasmBreakdown string   `json:"quasm_breakdown"`
	GrammarTip     string   `json:"grammar_tip"`
	ScrambleWords  []string `json:"scramble_words"`
}

type GrammarCategoryInfo struct {
	TenseCategory string `json:"tense_category"`
	CategoryIcon  string `json:"category_icon"`
	Type          string `json:"type"`
	Count         int    `json:"count"`
}

type WritingPrompt struct {
	ID               int      `json:"id"`
	Level            string   `json:"level"`
	Title            string   `json:"title"`
	Category         string   `json:"category"`
	CategoryIcon     string   `json:"category_icon"`
	TargetMin        int      `json:"target_min"`
	TargetMax        int      `json:"target_max"`
	SituationVi      string   `json:"situation_vi"`
	Prompt           string   `json:"prompt"`
	SentenceStarters []string `json:"sentence_starters"`
	GuideTips        []string `json:"guide_tips"`
	SuggestedVocab   []string `json:"suggested_vocab"`
}

type ObsidianItem struct {
	Word        string `json:"word"`
	POS         string `json:"pos"`
	Phonetic    string `json:"phonetic"`
	Definition  string `json:"definition"`
	Example     string `json:"example"`
	TopicKey    string `json:"topic_key"`
	TopicTitle  string `json:"topic_title"`
	DictLink    string `json:"dict_link"`
	FilePath    string `json:"file_path"`
	NextReview  string `json:"next_review"`
	Interval    int    `json:"interval"`
	Repetitions int    `json:"repetitions"`
	Status      string `json:"status"`
	IsDue       bool   `json:"is_due"`
}

type ObsidianSaveResult struct {
	Success bool   `json:"success"`
	Word    string `json:"word,omitempty"`
	File    string `json:"file,omitempty"`
	Error   string `json:"error,omitempty"`
}

type Config struct {
	ObsidianVaultPath string  `json:"obsidian_vault_path"`
	AiProvider        string  `json:"ai_provider"` // "agy", "openrouter", "groq", "ollama"
	AgyModel          string  `json:"agy_model"`
	AgyPath           string  `json:"agy_path"`
	AgyEffort         string  `json:"agy_effort,omitempty"`
	OpenrouterApiKey  string  `json:"openrouter_api_key"`
	OpenrouterModel   string  `json:"openrouter_model"`
	GroqApiKey        string  `json:"groq_api_key"`
	GroqModel         string  `json:"groq_model"`
	OllamaUrl         string  `json:"ollama_url"`
	OllamaModel       string  `json:"ollama_model"`
	AutoPlayAudio     bool    `json:"auto_play_audio"`
	DefaultAudioSpeed float64 `json:"default_audio_speed"`
	TTSProvider       string  `json:"tts_provider"` // "edge", "piper", "google"
	TTSVoice          string  `json:"tts_voice"`    // e.g. "en-US-JennyNeural"
	PiperPath           string  `json:"piper_path,omitempty"`
	PiperModelPath      string  `json:"piper_model_path,omitempty"`
	OpencodeModel       string  `json:"opencode_model,omitempty"`
	TranslationProvider string  `json:"translation_provider,omitempty"` // "default", "groq", "ollama", "openrouter", "agy", "opencode"
	TranslationModel    string  `json:"translation_model,omitempty"`    // e.g. "qwen/qwen3.8-27b"
}

type DiffToken struct {
	Type  string `json:"type"` // "correct", "wrong", "missing", "extra"
	Word  string `json:"word"`
	Match string `json:"match,omitempty"`
}

type DictationResult struct {
	Accuracy int         `json:"accuracy"`
	Passed   bool        `json:"passed"`
	Tokens   []DiffToken `json:"tokens"`
}

type ListeningQA struct {
	Question string `json:"q"`
	Answer   string `json:"a"`
}

type ListeningTopic struct {
	ID       int           `json:"id"`
	TopicID  int           `json:"topic_id"`
	Title    string        `json:"title"`
	Icon     string        `json:"icon"`
	AudioURL string        `json:"audio"`
	WebURL   string        `json:"url"`
	QA       []ListeningQA `json:"qa"`
}

type ExtractedVocab struct {
	Word     string `json:"word"`
	POS      string `json:"pos"`
	Phonetic string `json:"phonetic"`
	Meaning  string `json:"meaning"`
}

// ---------- IELTS Roadmap ----------

type RoadmapProgress struct {
	SessionID  int    `json:"session_id"`
	Status     string `json:"status"` // "pending" | "done" | "missed"
	ActualDate string `json:"actual_date,omitempty"`
	Note       string `json:"note,omitempty"`
}

type MockScore struct {
	ID      int     `json:"id"`
	Skill   string  `json:"skill"` // "L" | "R" | "W" | "S"
	Band    float64 `json:"band"`
	TakenAt string  `json:"taken_at"`
	Note    string  `json:"note,omitempty"`
}

// ---------- Speaking Lab ----------

type SpeakingPrompt struct {
	ID          int      `json:"id"`
	Part        int      `json:"part"` // 1 | 2 | 3
	Topic       string   `json:"topic"`
	Question    string   `json:"question"`
	Cues        []string `json:"cues"`
	HintVi      string   `json:"hint_vi"`
	SampleIdeas []string `json:"sample_ideas"`
}

type SpeakingAttempt struct {
	ID        int    `json:"id"`
	PromptID  int    `json:"prompt_id"`
	AudioPath string `json:"audio_path"`
	Duration  int    `json:"duration"`
	Feedback  string `json:"feedback"`
	CreatedAt string `json:"created_at"`
}

type RecordingStatus struct {
	Available  bool   `json:"available"`
	Recorder   string `json:"recorder"` // "arecord" | "ffmpeg"
	Message    string `json:"message"`
	Recording  bool   `json:"recording"`
	AudioPath  string `json:"audio_path,omitempty"`
}

// ---------- Reading Lab ----------

type ReadingQuestionItem struct {
	ID          int      `json:"id"`
	Question    string   `json:"question"`
	Options     []string `json:"options,omitempty"`
	Answer      string   `json:"answer"`
	Explanation string   `json:"explanation,omitempty"`
}

type ReadingQuestionSet struct {
	Type        string                `json:"type"` // "tfng" | "gapfill" | "matching_heading" | "mcq"
	Instruction string                `json:"instruction"`
	Items       []ReadingQuestionItem `json:"items"`
}

type ReadingPassage struct {
	ID        int                  `json:"id"`
	Title     string               `json:"title"`
	BandLevel float64              `json:"band_level"`
	Topic     string               `json:"topic"`
	WordCount int                  `json:"word_count"`
	Text      string               `json:"text"`
	Questions []ReadingQuestionSet `json:"questions"`
}

type ReadingPassageMeta struct {
	ID            int     `json:"id"`
	Title         string  `json:"title"`
	BandLevel     float64 `json:"band_level"`
	Topic         string  `json:"topic"`
	WordCount     int     `json:"word_count"`
	QuestionCount int     `json:"question_count"`
}

type ReadingAnswerInput struct {
	ItemID int    `json:"item_id"`
	Given  string `json:"given"`
}

type ReadingAnswerDetail struct {
	ItemID      int    `json:"item_id"`
	Question    string `json:"question"`
	Given       string `json:"given"`
	Expected    string `json:"expected"`
	Correct     bool   `json:"correct"`
	Explanation string `json:"explanation,omitempty"`
}

type ReadingResult struct {
	PassageID    int                   `json:"passage_id"`
	Correct      int                   `json:"correct"`
	Total        int                   `json:"total"`
	Percentage   int                   `json:"percentage"`
	BandEstimate float64               `json:"band_estimate"`
	Details      []ReadingAnswerDetail `json:"details"`
}

type TranslationResult struct {
	TranslatedText string           `json:"translated_text"`
	SourceLang     string           `json:"source_lang"`
	TargetLang     string           `json:"target_lang"`
	Tone           string           `json:"tone"`
	KeyVocabulary  []ExtractedVocab `json:"key_vocabulary"`
	NuanceNotes    []string         `json:"nuance_notes"`
}
