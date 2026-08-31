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
	OpenrouterApiKey  string  `json:"openrouter_api_key"`
	OpenrouterModel   string  `json:"openrouter_model"`
	GroqApiKey        string  `json:"groq_api_key"`
	GroqModel         string  `json:"groq_model"`
	OllamaUrl         string  `json:"ollama_url"`
	OllamaModel       string  `json:"ollama_model"`
	AutoPlayAudio     bool    `json:"auto_play_audio"`
	DefaultAudioSpeed float64 `json:"default_audio_speed"`
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
