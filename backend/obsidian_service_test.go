package backend

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestExpandPath(t *testing.T) {
	home, _ := os.UserHomeDir()

	tests := []struct {
		input    string
		expected string
	}{
		{"~/Documents/Vault", filepath.Join(home, "Documents/Vault")},
		{"/var/data/vault", "/var/data/vault"},
		{"", ""},
	}

	for _, tt := range tests {
		got := ExpandPath(tt.input)
		if got != tt.expected {
			t.Errorf("ExpandPath(%q) = %q, expected %q", tt.input, got, tt.expected)
		}
	}
}

func TestSaveWritingToObsidian(t *testing.T) {
	tempVault, err := os.MkdirTemp("", "obsidian_vault_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempVault)

	res, err := SaveWritingToObsidian(
		"Daily Status Update",
		"Your lead asked for a daily status update.",
		"Write 2-3 sentences reporting your progress.",
		"I have finished the core implementation and tests are passing.",
		"Great job! Clear and concise workplace communication.",
		tempVault,
	)

	if err != nil {
		t.Fatalf("SaveWritingToObsidian returned error: %v", err)
	}
	if !res.Success {
		t.Errorf("expected success true, got false")
	}

	// Verify file was written
	if _, err := os.Stat(res.File); os.IsNotExist(err) {
		t.Fatalf("expected file to exist at %s", res.File)
	}

	content, err := os.ReadFile(res.File)
	if err != nil {
		t.Fatal(err)
	}

	contentStr := string(content)
	if !strings.Contains(contentStr, "Daily Status Update") {
		t.Errorf("expected content to contain title")
	}
	if !strings.Contains(contentStr, "## 📝 Your Essay") {
		t.Errorf("expected content to contain English section header '## 📝 Your Essay'")
	}
	if !strings.Contains(contentStr, "## 🤖 AI Evaluation & Feedback") {
		t.Errorf("expected content to contain English section header '## 🤖 AI Evaluation & Feedback'")
	}
}
