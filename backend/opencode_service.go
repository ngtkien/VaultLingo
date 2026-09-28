package backend

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

type OpencodeModelItem struct {
	ID            string `json:"id"`
	Name          string `json:"name"`
	Provider      string `json:"provider"`
	ProviderName  string `json:"provider_name"`
	IsRecommended bool   `json:"is_recommended"`
	Description   string `json:"description,omitempty"`
}

type OpencodeStatus struct {
	Installed       bool                `json:"installed"`
	Version         string              `json:"version"`
	HasAuth         bool                `json:"has_auth"`
	ActiveProviders []string            `json:"active_providers"`
	Models          []OpencodeModelItem `json:"models"`
	TotalCount      int                 `json:"total_count"`
	LastUpdated     string              `json:"last_updated"`
	Error           string              `json:"error,omitempty"`
}

func getOpencodeModelsCachePath() string {
	home, _ := os.UserHomeDir()
	configDir := filepath.Join(home, ".config", "VaultLingo")
	_ = os.MkdirAll(configDir, 0755)
	return filepath.Join(configDir, "opencode_models.json")
}

func findOpencodeBinary() (string, error) {
	if p, err := exec.LookPath("opencode"); err == nil {
		return p, nil
	}
	commonPaths := []string{
		"/usr/bin/opencode",
		"/usr/local/bin/opencode",
	}
	home, _ := os.UserHomeDir()
	if home != "" {
		commonPaths = append(commonPaths,
			filepath.Join(home, ".local", "bin", "opencode"),
			filepath.Join(home, ".npm-global", "bin", "opencode"),
			filepath.Join(home, ".cargo", "bin", "opencode"),
		)
	}
	for _, p := range commonPaths {
		if _, err := os.Stat(p); err == nil {
			return p, nil
		}
	}
	return "", fmt.Errorf("opencode binary not found")
}

// CheckOpencodeStatus checks if opencode is installed, its version, and authenticated providers
func CheckOpencodeStatus() OpencodeStatus {
	status := OpencodeStatus{
		Installed:       false,
		Version:         "",
		HasAuth:         false,
		ActiveProviders: []string{},
		Models:          []OpencodeModelItem{},
		TotalCount:      0,
		LastUpdated:     "",
	}

	binPath, err := findOpencodeBinary()
	if err != nil {
		status.Error = "OpenCode CLI is not installed"
		status.Models = DefaultOpencodeModels()
		status.TotalCount = len(status.Models)
		return status
	}
	status.Installed = true

	// Check version
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, binPath, "--version").Output()
	if err == nil {
		status.Version = strings.TrimSpace(string(out))
	}

	// Check auth credentials in ~/.local/share/opencode/auth.json
	home, _ := os.UserHomeDir()
	authPath := filepath.Join(home, ".local", "share", "opencode", "auth.json")
	if data, err := os.ReadFile(authPath); err == nil {
		var creds map[string]interface{}
		if err := json.Unmarshal(data, &creds); err == nil {
			for k := range creds {
				status.ActiveProviders = append(status.ActiveProviders, k)
			}
			if len(status.ActiveProviders) > 0 {
				status.HasAuth = true
			}
		}
	}

	// Read cached models if available
	cacheFile := getOpencodeModelsCachePath()
	if data, err := os.ReadFile(cacheFile); err == nil {
		var cached struct {
			LastUpdated string              `json:"last_updated"`
			Models      []OpencodeModelItem `json:"models"`
		}
		if err := json.Unmarshal(data, &cached); err == nil && len(cached.Models) > 0 {
			status.Models = cached.Models
			status.TotalCount = len(cached.Models)
			status.LastUpdated = cached.LastUpdated
			return status
		}
	}

	// If no cache, return default models
	status.Models = DefaultOpencodeModels()
	status.TotalCount = len(status.Models)
	return status
}

// FetchOpencodeModels executes `opencode models` dynamically, parses, categorizes, and updates cache
func FetchOpencodeModels() (OpencodeStatus, error) {
	status := CheckOpencodeStatus()
	binPath, err := findOpencodeBinary()
	if err != nil {
		return status, fmt.Errorf("opencode CLI not installed: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, binPath, "models")
	out, err := cmd.CombinedOutput()
	if err != nil {
		status.Error = fmt.Sprintf("Failed to run 'opencode models': %s", string(out))
		if len(status.Models) == 0 {
			status.Models = DefaultOpencodeModels()
			status.TotalCount = len(status.Models)
		}
		return status, fmt.Errorf("failed to fetch models: %s (%w)", string(out), err)
	}

	lines := strings.Split(string(out), "\n")
	var parsedModels []OpencodeModelItem
	seen := make(map[string]bool)

	for _, rawLine := range lines {
		line := strings.TrimSpace(rawLine)
		if line == "" || strings.HasPrefix(line, "Error:") || strings.HasPrefix(line, "Warning:") || strings.HasPrefix(line, "---") {
			continue
		}
		if seen[line] {
			continue
		}
		seen[line] = true

		item := classifyOpencodeModel(line)
		parsedModels = append(parsedModels, item)
	}

	if len(parsedModels) == 0 {
		parsedModels = DefaultOpencodeModels()
	}

	// Update cache
	nowStr := time.Now().Format("2006-01-02 15:04:05")
	cachePayload := struct {
		LastUpdated string              `json:"last_updated"`
		Models      []OpencodeModelItem `json:"models"`
	}{
		LastUpdated: nowStr,
		Models:      parsedModels,
	}

	if data, err := json.MarshalIndent(cachePayload, "", "  "); err == nil {
		_ = os.WriteFile(getOpencodeModelsCachePath(), data, 0644)
	}

	status.Models = parsedModels
	status.TotalCount = len(parsedModels)
	status.LastUpdated = nowStr
	status.Error = ""

	return status, nil
}

// GetOpencodeModels returns available OpenCode models from cache or defaults
func GetOpencodeModels() []OpencodeModelItem {
	status := CheckOpencodeStatus()
	if len(status.Models) > 0 {
		return status.Models
	}
	return DefaultOpencodeModels()
}

func classifyOpencodeModel(modelID string) OpencodeModelItem {
	parts := strings.SplitN(modelID, "/", 2)
	provider := "opencode"
	modelName := modelID

	if len(parts) == 2 {
		provider = parts[0]
		modelName = parts[1]
	}

	providerName := "OpenCode Free"
	switch provider {
	case "opencode-go":
		providerName = "OpenCode Go (Subscribed)"
	case "opencode-zen":
		providerName = "OpenCode Zen (Pay-per-token)"
	case "opencode":
		providerName = "OpenCode Free"
	default:
		providerName = provider
	}

	isRec := false
	desc := ""

	// Highlight best recommended models for language learning & reasoning
	switch {
	case strings.Contains(modelName, "nemotron-3-ultra-free"):
		isRec = true
		desc = "Best Free: Reliable JSON + Strong Bilingual EN/VI ⭐"
	case strings.Contains(modelName, "space-bunny-free"):
		isRec = true
		desc = "Fastest Consistent Free Model ⭐"
	case strings.Contains(modelName, "nemotron-3.5-lightning-free"):
		desc = "Free - Fast but Unstable Latency"
	case strings.Contains(modelName, "mimo-v2.6-flash-free"):
		desc = "Free - Quick but Flaky on Long Prompts"
	case strings.Contains(modelName, "deepseek-v4-flash"):
		isRec = true
		desc = "Ultra-Fast, Premier Reasoning & Code ⭐"
	case strings.Contains(modelName, "deepseek-v4-pro"):
		isRec = true
		desc = "Deep Linguistic Nuance & Grammar"
	case strings.Contains(modelName, "qwen3.8-flash"):
		isRec = true
		desc = "Lightning Speed, Exceptional Bilingual EN/VI ⭐"
	case strings.Contains(modelName, "qwen3.8-max"), strings.Contains(modelName, "qwen3.7-max"):
		isRec = true
		desc = "Highest Linguistic Capability Qwen"
	case strings.Contains(modelName, "kimi-k3"):
		isRec = true
		desc = "Deep Context & Natural Style Flow ⭐"
	case strings.Contains(modelName, "glm-5.3-flash"):
		isRec = true
		desc = "High-speed General Intelligence"
	case strings.Contains(modelName, "gpt-5.6-luna"):
		isRec = true
		desc = "Next-gen Advanced Assistant"
	}

	return OpencodeModelItem{
		ID:            modelID,
		Name:          modelName,
		Provider:      provider,
		ProviderName:  providerName,
		IsRecommended: isRec,
		Description:   desc,
	}
}

// DefaultOpencodeModels provides immediate fallback options if CLI hasn't refreshed yet (prioritizing Free models)
func DefaultOpencodeModels() []OpencodeModelItem {
	presets := []string{
		"opencode/nemotron-3-ultra-free",
		"opencode/space-bunny-free",
		"opencode/nemotron-3.5-lightning-free",
		"opencode/mimo-v2.6-flash-free",
		"opencode-go/deepseek-v4-flash",
		"opencode-go/qwen3.8-flash",
		"opencode-go/kimi-k3",
		"opencode-go/glm-5.3-flash",
		"opencode-go/deepseek-v4-pro",
		"opencode-go/qwen3.8-max",
		"opencode-go/minimax-m3",
		"opencode-go/gpt-5.6-luna",
		"opencode-zen/deepseek-v4-flash",
		"opencode-zen/qwen3.8-flash",
		"opencode-zen/claude-3-7-sonnet",
	}

	var res []OpencodeModelItem
	for _, id := range presets {
		res = append(res, classifyOpencodeModel(id))
	}
	return res
}
