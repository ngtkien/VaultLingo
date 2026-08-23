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
		AgyPath:           "",
		OpenrouterApiKey:  "",
		OpenrouterModel:   "meta-llama/llama-3.3-70b-instruct:free",
		GroqApiKey:        "",
		GroqModel:         "llama-3.3-70b-versatile",
		OllamaUrl:         "http://localhost:11434",
		OllamaModel:       "llama3:latest",
		AutoPlayAudio:     true,
		DefaultAudioSpeed: 1.0,
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
	if cfg.OpenrouterModel == "" {
		cfg.OpenrouterModel = "meta-llama/llama-3.3-70b-instruct:free"
	}
	if cfg.GroqModel == "" {
		cfg.GroqModel = "llama-3.3-70b-versatile"
	}
	if cfg.OllamaUrl == "" {
		cfg.OllamaUrl = "http://localhost:11434"
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
