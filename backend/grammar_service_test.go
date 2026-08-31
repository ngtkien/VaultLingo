package backend

import (
	"testing"
)

func TestCheckGrammarAnswer_Perfect(t *testing.T) {
	target := "How often does she study English grammar?"
	input := "How often does she study English grammar?"

	res := CheckGrammarAnswer(target, input)
	if res.Accuracy != 100 {
		t.Errorf("expected 100 accuracy, got %d", res.Accuracy)
	}
	if !res.Passed {
		t.Errorf("expected passed true, got false")
	}
}

func TestCheckGrammarAnswer_PunctuationAndCaseInsensitive(t *testing.T) {
	target := "Could you tell me where the nearest subway station is?"
	input := "could you tell me where the nearest subway station is"

	res := CheckGrammarAnswer(target, input)
	if res.Accuracy < 90 {
		t.Errorf("expected high accuracy despite missing question mark, got %d", res.Accuracy)
	}
	if !res.Passed {
		t.Errorf("expected passed true, got false")
	}
}
