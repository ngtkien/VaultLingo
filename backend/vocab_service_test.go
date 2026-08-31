package backend

import (
	"testing"
)

func TestGetTopicMeta(t *testing.T) {
	title, icon := GetTopicMeta("07_Embedded_and_Electronics")
	if title != "Embedded & Electronics" || icon != "⚡" {
		t.Errorf("unexpected topic meta: %s, %s", title, icon)
	}

	defTitle, defIcon := GetTopicMeta("unknown_topic")
	if defTitle != "General English" || defIcon != "📚" {
		t.Errorf("unexpected fallback topic meta: %s, %s", defTitle, defIcon)
	}
}

func TestGetAvailableTopics(t *testing.T) {
	topics := GetAvailableTopics()
	if len(topics) < 5 {
		t.Errorf("expected at least 5 topics, got %d", len(topics))
	}
}

func TestDatabase_LookupAndSearch(t *testing.T) {
	_, err := InitDB()
	if err != nil {
		t.Fatalf("InitDB failed: %v", err)
	}

	// Search words
	results, err := SearchWordsInDB("comp", 5)
	if err != nil {
		t.Fatalf("SearchWordsInDB failed: %v", err)
	}
	if len(results) == 0 {
		t.Errorf("expected at least 1 search result for 'comp'")
	}

	// Lookup known word
	w, err := LookupWordInDB("compare")
	if err != nil {
		t.Fatalf("LookupWordInDB('compare') failed: %v", err)
	}
	if w == nil || w.Word != "compare" {
		t.Errorf("expected word 'compare', got %v", w)
	}
	if w.DefinitionEn == "" {
		t.Errorf("expected non-empty definition_en for 'compare'")
	}
}
