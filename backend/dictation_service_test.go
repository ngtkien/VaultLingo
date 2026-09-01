package backend

import (
	"testing"
)

func TestCleanWord(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Hello,", "hello"},
		{"world!", "world"},
		{"it's", "it's"},
		{"\"Quote\"", "quote"},
		{"test...", "test"},
		{"", ""},
	}

	for _, tt := range tests {
		got := cleanWord(tt.input)
		if got != tt.expected {
			t.Errorf("cleanWord(%q) = %q, expected %q", tt.input, got, tt.expected)
		}
	}
}

func TestCheckDictation_PerfectMatch(t *testing.T) {
	target := "Please share your screen so that we can review the design mockup together."
	input := "Please share your screen so that we can review the design mockup together."

	res := CheckDictation(target, input)

	if res.Accuracy != 100 {
		t.Errorf("expected accuracy 100, got %d", res.Accuracy)
	}
	if !res.Passed {
		t.Errorf("expected passed true, got false")
	}
	for _, tok := range res.Tokens {
		if tok.Type != "correct" {
			t.Errorf("expected all tokens to be correct, found: %v", tok)
		}
	}
}

func TestCheckDictation_PartialMistakes(t *testing.T) {
	target := "The quick brown fox jumps over the lazy dog"
	input := "The fast brown fox leaped over the lazy cat"

	res := CheckDictation(target, input)

	if res.Accuracy <= 0 || res.Accuracy >= 100 {
		t.Errorf("expected partial accuracy between 0 and 100, got %d", res.Accuracy)
	}

	hasWrong := false
	for _, tok := range res.Tokens {
		if tok.Type == "wrong" || tok.Type == "missing" {
			hasWrong = true
			break
		}
	}
	if !hasWrong {
		t.Errorf("expected diff tokens to contain wrong/missing entries")
	}
}

func TestCheckDictation_EmptyInput(t *testing.T) {
	target := "Hello world"
	input := ""

	res := CheckDictation(target, input)

	if res.Accuracy != 0 {
		t.Errorf("expected accuracy 0 for empty input, got %d", res.Accuracy)
	}
	if res.Passed {
		t.Errorf("expected passed false for empty input")
	}
}

func TestGetDictationLevels(t *testing.T) {
	_, err := InitDB()
	if err != nil {
		t.Fatalf("InitDB failed: %v", err)
	}

	levels, err := GetDictationLevels()
	if err != nil {
		t.Fatalf("GetDictationLevels failed: %v", err)
	}
	if len(levels) == 0 {
		t.Errorf("expected non-empty levels list")
	}
}

func TestGetDictationSentenceFiltered(t *testing.T) {
	_, err := InitDB()
	if err != nil {
		t.Fatalf("InitDB failed: %v", err)
	}

	// Test filtering by A2
	d, err := GetDictationSentenceFiltered("all", "A2", nil)
	if err != nil {
		t.Fatalf("GetDictationSentenceFiltered A2 failed: %v", err)
	}
	if d.Sentence == "" {
		t.Errorf("expected non-empty sentence")
	}

	// Test filtering by B2
	d2, err := GetDictationSentenceFiltered("all", "B2", nil)
	if err != nil {
		t.Fatalf("GetDictationSentenceFiltered B2 failed: %v", err)
	}
	if d2.Sentence == "" {
		t.Errorf("expected non-empty sentence")
	}
}
