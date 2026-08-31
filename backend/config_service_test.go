package backend

import (
	"os"
	"path/filepath"
	"testing"
)

func TestLoadConfig_Defaults(t *testing.T) {
	cfg := LoadConfig()

	if cfg.AiProvider == "" {
		t.Errorf("expected default AiProvider to be non-empty")
	}
	if cfg.AgyModel == "" {
		t.Errorf("expected default AgyModel to be non-empty")
	}
	if cfg.OpenrouterModel == "" {
		t.Errorf("expected default OpenrouterModel to be non-empty")
	}
}

func TestGetConfigPath(t *testing.T) {
	path := GetConfigPath()
	if path == "" {
		t.Errorf("expected config path to be non-empty")
	}
	if filepath.Base(path) != "config.json" {
		t.Errorf("expected filename to be config.json, got %s", filepath.Base(path))
	}
}

func TestSaveAndLoadConfig(t *testing.T) {
	origConfigData, _ := os.ReadFile(GetConfigPath())
	defer func() {
		if len(origConfigData) > 0 {
			_ = os.WriteFile(GetConfigPath(), origConfigData, 0644)
		}
	}()

	testCfg := Config{
		ObsidianVaultPath: "~/TestVault",
		AiProvider:        "agy",
		AgyModel:          "gemini-3.7-flash",
		AgyEffort:         "low",
		AutoPlayAudio:     false,
		DefaultAudioSpeed: 0.85,
	}

	err := SaveConfig(testCfg)
	if err != nil {
		t.Errorf("SaveConfig failed: %v", err)
	}

	loaded := LoadConfig()
	if loaded.AgyModel != "gemini-3.7-flash" {
		t.Errorf("unexpected loaded agy model: %s", loaded.AgyModel)
	}
}
