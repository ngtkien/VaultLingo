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
