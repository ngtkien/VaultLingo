package backend

import (
	"os"
	"path/filepath"
	"testing"
)

func TestSaveTranslationToObsidian(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "vaultlingo_trans_test_*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	sourceText := "Resilience is the ability to adapt to difficult situations."
	targetText := "Khả năng phục hồi là năng lực thích ứng trước những tình huống khó khăn."
	sourceLang := "English"
	targetLang := "Vietnamese"
	tone := "Editorial & Journalistic"

	vocab := []ExtractedVocab{
		{
			Word:     "resilience",
			POS:      "noun",
			Phonetic: "/rɪˈzɪl.jəns/",
			Meaning:  "Khả năng phục hồi",
		},
	}

	res, err := SaveTranslationToObsidian(sourceText, targetText, sourceLang, targetLang, tone, vocab, tmpDir)
	if err != nil {
		t.Fatalf("SaveTranslationToObsidian returned unexpected error: %v", err)
	}

	if !res.Success {
		t.Fatalf("Expected success to be true, got false. Error: %s", res.Error)
	}

	if _, err := os.Stat(res.File); os.IsNotExist(err) {
		t.Fatalf("Expected file to exist at %s, but it was not found", res.File)
	}

	content, err := os.ReadFile(res.File)
	if err != nil {
		t.Fatalf("Failed to read created translation note: %v", err)
	}

	contentStr := string(content)
	if !filepath.IsAbs(res.File) {
		t.Errorf("Expected absolute file path, got %s", res.File)
	}
	if len(contentStr) == 0 {
		t.Errorf("File content should not be empty")
	}
}

func TestParseTranslationResponse_WithThinkTagsAndMarkdown(t *testing.T) {
	raw := "<think>\nI need to translate \"Hello world\" to Vietnamese.\nThe tone is Editorial.\nVocabulary: world (danh từ).\n</think>\nHere is the translation:\n```json\n{\n  \"translated_text\": \"Xin chào thế giới\",\n  \"source_lang\": \"English\",\n  \"target_lang\": \"Vietnamese\",\n  \"tone\": \"Editorial\",\n  \"key_vocabulary\": [\n    {\n      \"word\": \"world\",\n      \"pos\": \"noun\",\n      \"phonetic\": \"/wɜːld/\",\n      \"meaning\": \"thế giới\"\n    }\n  ],\n  \"nuance_notes\": [\n    \"Một lời chào kinh điển.\"\n  ]\n}\n```\nHope that helps!"

	res := parseTranslationResponse(raw, "English", "Vietnamese", "Editorial")
	if res.TranslatedText != "Xin chào thế giới" {
		t.Errorf("Expected translated text 'Xin chào thế giới', got '%s'", res.TranslatedText)
	}
	if len(res.KeyVocabulary) != 1 || res.KeyVocabulary[0].Word != "world" {
		t.Errorf("Expected 1 vocab item 'world', got %+v", res.KeyVocabulary)
	}
	if len(res.NuanceNotes) != 1 {
		t.Errorf("Expected 1 nuance note, got %+v", res.NuanceNotes)
	}
}

func TestParseTranslationResponse_CleanFallback(t *testing.T) {
	raw := `<think>Some thinking</think>Dưới đây là bản dịch: Khả năng phục hồi là chìa khóa.`
	res := parseTranslationResponse(raw, "English", "Vietnamese", "Editorial")

	if res.TranslatedText != "Khả năng phục hồi là chìa khóa." {
		t.Errorf("Expected clean text without think tags or intros, got '%s'", res.TranslatedText)
	}
}

func TestGetEffectiveTranslationConfig(t *testing.T) {
	baseCfg := Config{
		AiProvider:          "agy",
		AgyModel:            "gemini-3.7-flash",
		GroqModel:           "llama-3.1-8b-instant",
		TranslationProvider: "groq",
		TranslationModel:    "qwen/qwen3.6-27b",
	}

	eff := GetEffectiveTranslationConfig(baseCfg)
	if eff.AiProvider != "groq" {
		t.Errorf("Expected AiProvider to be 'groq', got '%s'", eff.AiProvider)
	}
	if eff.GroqModel != "qwen/qwen3.6-27b" {
		t.Errorf("Expected GroqModel to be 'qwen/qwen3.6-27b', got '%s'", eff.GroqModel)
	}

	// Default fallback to global
	defaultCfg := Config{
		AiProvider:          "agy",
		AgyModel:            "gemini-3.7-flash",
		TranslationProvider: "default",
	}
	effDefault := GetEffectiveTranslationConfig(defaultCfg)
	if effDefault.AiProvider != "agy" {
		t.Errorf("Expected AiProvider to stay 'agy', got '%s'", effDefault.AiProvider)
	}
}
