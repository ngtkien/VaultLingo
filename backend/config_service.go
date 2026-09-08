package backend

import (
	"encoding/json"
	"os"
	"path/filepath"
)

func GetConfigPath() string {
	home, _ := os.UserHomeDir()
	configDir := filepath.Join(home, ".config", "VaultLingo")
	_ = os.MkdirAll(configDir, 0755)
	return filepath.Join(configDir, "config.json")
}

func LoadConfig() Config {
	defaultCfg := Config{
		ObsidianVaultPath: GetDefaultVaultPath(),
		AiProvider:        "agy",
		AgyModel:          "gemini-3.7-flash",
		AgyEffort:         "low",
		AgyPath:           "",
		OpenrouterApiKey:    "",
		OpenrouterModel:     "openrouter/free",
		GroqApiKey:          "",
		GroqModel:           "qwen/qwen3.6-27b",
		OllamaUrl:           "http://localhost:11434",
		OllamaModel:         "qwen2.5:7b",
		AutoPlayAudio:       true,
		DefaultAudioSpeed:   1.0,
		TTSProvider:         "edge",
		TTSVoice:            "en-US-JennyNeural",
		OpencodeModel:       "opencode/mimo-v2.5-free",
		TranslationProvider: "default",
		TranslationModel:    "qwen/qwen3.6-27b",
	}

	configPath := GetConfigPath()
	data, err := os.ReadFile(configPath)
	if err != nil {
		return defaultCfg
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return defaultCfg
	}

	if cfg.ObsidianVaultPath == "" {
		cfg.ObsidianVaultPath = defaultCfg.ObsidianVaultPath
	}
	if cfg.AiProvider == "" {
		cfg.AiProvider = "agy"
	}
	if cfg.AgyModel == "" {
		cfg.AgyModel = "gemini-3.7-flash"
	}
	if cfg.OpenrouterModel == "" || cfg.OpenrouterModel == "meta-llama/llama-3.3-70b-instruct:free" {
		cfg.OpenrouterModel = "openrouter/free"
	}
	if cfg.OpencodeModel == "" || cfg.OpencodeModel == "openrouter/free" || cfg.OpencodeModel == "deepseek-v4-flash" {
		cfg.OpencodeModel = "opencode/mimo-v2.5-free"
	}
	if cfg.GroqModel == "" || cfg.GroqModel == "llama-3.3-70b-versatile" || cfg.GroqModel == "llama-3.1-8b-instant" {
		cfg.GroqModel = "qwen/qwen3.6-27b"
	}
	if cfg.TranslationProvider == "" {
		cfg.TranslationProvider = "default"
	}
	if cfg.TranslationModel == "" {
		cfg.TranslationModel = "qwen/qwen3.6-27b"
	}
	if cfg.OllamaUrl == "" {
		cfg.OllamaUrl = "http://localhost:11434"
	}
	if cfg.OllamaModel == "" {
		cfg.OllamaModel = "qwen2.5:7b"
	}
	if cfg.TTSProvider == "" {
		cfg.TTSProvider = "edge"
	}
	if cfg.TTSVoice == "" {
		cfg.TTSVoice = "en-US-JennyNeural"
	}

	return cfg
}

func SaveConfig(cfg Config) error {
	configPath := GetConfigPath()
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(configPath, data, 0644)
}
