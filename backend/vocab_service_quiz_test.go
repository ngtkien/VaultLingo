package backend

import "testing"

func TestShuffleQuizOptionsPreservesCorrectAnswer(t *testing.T) {
	q := Quiz{
		Options: []string{"A. at", "B. in", "C. on", "D. for"},
		Correct: "A",
	}
	shuffled := shuffleQuizOptions(q)
	if len(shuffled.Options) != 4 {
		t.Fatalf("expected four options, got %d", len(shuffled.Options))
	}
	for _, option := range shuffled.Options {
		if option[0:1] == shuffled.Correct && option[3:] != "at" {
			t.Fatalf("correct label %q no longer points to the correct text: %q", shuffled.Correct, option)
		}
	}
}
