package backend

import (
	"strings"
	"testing"
)

func TestClassifyOpencodeModel(t *testing.T) {
	tests := []struct {
		modelID      string
		wantProvider string
		wantRec      bool
	}{
		{
			modelID:      "opencode-go/deepseek-v4-flash",
			wantProvider: "opencode-go",
			wantRec:      true,
		},
		{
			modelID:      "opencode-go/qwen3.8-flash",
			wantProvider: "opencode-go",
			wantRec:      true,
		},
		{
			modelID:      "opencode-zen/deepseek-v4-flash",
			wantProvider: "opencode-zen",
			wantRec:      true,
		},
		{
			modelID:      "opencode/mimo-v2.5-free",
			wantProvider: "opencode",
			wantRec:      true,
		},
		{
			modelID:      "custom-provider/custom-model",
			wantProvider: "custom-provider",
			wantRec:      false,
		},
	}

	for _, tc := range tests {
		item := classifyOpencodeModel(tc.modelID)
		if item.Provider != tc.wantProvider {
			t.Errorf("classifyOpencodeModel(%q).Provider = %q, want %q", tc.modelID, item.Provider, tc.wantProvider)
		}
		if item.IsRecommended != tc.wantRec {
			t.Errorf("classifyOpencodeModel(%q).IsRecommended = %v, want %v", tc.modelID, item.IsRecommended, tc.wantRec)
		}
	}
}

func TestDefaultOpencodeModels(t *testing.T) {
	models := DefaultOpencodeModels()
	if len(models) == 0 {
		t.Fatalf("DefaultOpencodeModels returned empty list")
	}

	hasGo := false
	hasZen := false
	hasFree := false

	for _, m := range models {
		if m.Provider == "opencode-go" {
			hasGo = true
		}
		if m.Provider == "opencode-zen" {
			hasZen = true
		}
		if m.Provider == "opencode" {
			hasFree = true
		}
	}

	if !hasGo {
		t.Errorf("DefaultOpencodeModels missing opencode-go models")
	}
	if !hasZen {
		t.Errorf("DefaultOpencodeModels missing opencode-zen models")
	}
	if !hasFree {
		t.Errorf("DefaultOpencodeModels missing free opencode models")
	}
}

func TestCheckOpencodeStatus(t *testing.T) {
	status := CheckOpencodeStatus()
	if !status.Installed {
		t.Logf("OpenCode CLI is not installed in test environment")
		return
	}
	if status.Version == "" {
		t.Errorf("Expected version to be non-empty when installed")
	}
	if len(status.Models) == 0 {
		t.Errorf("Expected at least fallback or cached models in status")
	}
}

func TestFetchOpencodeModels(t *testing.T) {
	status, err := FetchOpencodeModels()
	if err != nil {
		t.Fatalf("FetchOpencodeModels failed: %v", err)
	}
	if status.TotalCount == 0 {
		t.Fatalf("FetchOpencodeModels returned 0 models")
	}
	t.Logf("Successfully fetched %d models from OpenCode CLI! Version: %s, ActiveProviders: %v",
		status.TotalCount, status.Version, status.ActiveProviders)
}

func TestCallAI_Opencode(t *testing.T) {
	status := CheckOpencodeStatus()
	if !status.Installed || !status.HasAuth {
		t.Skip("OpenCode not installed or no auth credentials configured")
	}

	cfg := Config{
		AiProvider:    "opencode",
		OpencodeModel: "opencode-go/deepseek-v4-flash",
	}

	out, err := CallAI("You are a helpful assistant.", "What is 1+1? Answer with just the single number.", cfg)
	if err != nil {
		t.Fatalf("CallAI with opencode failed: %v", err)
	}
	if !strings.Contains(out, "2") {
		t.Errorf("Expected response to contain '2', got: %s", out)
	}
	t.Logf("CallAI via OpenCode Go succeeded with response: %q", out)
}


