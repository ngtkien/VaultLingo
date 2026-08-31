package backend

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

func GetWritingPrompt(level string) (WritingPrompt, error) {
	var p WritingPrompt
	var startersJSON, tipsJSON, vocabJSON string
	var query string
	var args []interface{}

	if level == "" || level == "all" {
		query = `
			SELECT id, level, title, category, category_icon, target_min, target_max,
			       situation_vi, prompt, sentence_starters_json, guide_tips_json, suggested_vocab_json
			FROM writing_prompts
			ORDER BY RANDOM()
			LIMIT 1
		`
	} else {
		query = `
			SELECT id, level, title, category, category_icon, target_min, target_max,
			       situation_vi, prompt, sentence_starters_json, guide_tips_json, suggested_vocab_json
			FROM writing_prompts
			WHERE level = ?
			ORDER BY RANDOM()
			LIMIT 1
		`
		args = append(args, level)
	}

	err := DB.QueryRow(query, args...).Scan(
		&p.ID, &p.Level, &p.Title, &p.Category, &p.CategoryIcon,
		&p.TargetMin, &p.TargetMax, &p.SituationVi, &p.Prompt,
		&startersJSON, &tipsJSON, &vocabJSON,
	)

	if err != nil {
		return WritingPrompt{
			Level:        "scenario",
			Title:        "Running Late Message",
			Category:     "Workplace Slack",
			CategoryIcon: "🚗",
			TargetMin:    20,
			TargetMax:    50,
			SituationVi:  "You are stuck in heavy traffic and will be 20 minutes late. Write a Slack message to inform your team.",
			Prompt:       "Write a quick 2 to 3 sentence Slack message to your team explaining the delay.",
			SentenceStarters: []string{
				"Good morning team, I'm currently stuck in heavy traffic on...",
				"I expect to arrive at the office around...",
			},
			GuideTips: []string{
				"State the delay clearly and professionally upfront.",
				"Provide a realistic updated arrival time.",
			},
			SuggestedVocab: []string{"stuck in traffic", "running late", "expect to arrive"},
		}, nil
	}

	_ = json.Unmarshal([]byte(startersJSON), &p.SentenceStarters)
	_ = json.Unmarshal([]byte(tipsJSON), &p.GuideTips)
	_ = json.Unmarshal([]byte(vocabJSON), &p.SuggestedVocab)

	return p, nil
}

// CallAI handles arbitrary prompt execution across configured providers (OpenCode, AGY, OpenRouter, Groq, Ollama)
func CallAI(systemInstruction, userContent string, cfg Config) (string, error) {
	// 1. OpenCode CLI (Local Free AI Agent)
	if cfg.AiProvider == "opencode" {
		fullPrompt := userContent
		if systemInstruction != "" {
			fullPrompt = fmt.Sprintf("%s\n\n%s", systemInstruction, userContent)
		}
		cmdPath, err := exec.LookPath("opencode")
		if err != nil {
			cmdPath = "/usr/bin/opencode"
		}
		cmd := exec.Command(cmdPath, "run", fullPrompt)
		out, err := cmd.CombinedOutput()
		if err != nil {
			return "", fmt.Errorf("opencode execution failed: %s (%w)", string(out), err)
		}
		return strings.TrimSpace(string(out)), nil
	}

	// 2. Antigravity CLI (Native system-authenticated agy CLI)
	if cfg.AiProvider == "agy" || cfg.AiProvider == "" {
		fullPrompt := userContent
		if systemInstruction != "" {
			fullPrompt = fmt.Sprintf("%s\n\n%s", systemInstruction, userContent)
		}
		cmdPath := cfg.AgyPath
		if cmdPath == "" {
			var err error
			cmdPath, err = exec.LookPath("agy")
			if err != nil {
				homeDir, _ := exec.Command("sh", "-c", "echo $HOME").Output()
				cmdPath = strings.TrimSpace(string(homeDir)) + "/.local/bin/agy"
			}
		}

		var args []string
		args = append(args, "-p", fullPrompt)
		if cfg.AgyModel != "" && cfg.AgyModel != "auto" && cfg.AgyModel != "default" {
			args = append(args, "--model", cfg.AgyModel)
		}

		cmd := exec.Command(cmdPath, args...)
		out, err := cmd.CombinedOutput()
		if err != nil {
			return "", fmt.Errorf("Antigravity (agy) execution failed: %s (%w)", string(out), err)
		}
		return strings.TrimSpace(string(out)), nil
	}

	client := &http.Client{Timeout: 35 * time.Second}

	// 3. OpenRouter (Free & Open Source Models)
	if cfg.AiProvider == "openrouter" {
		if cfg.OpenrouterApiKey == "" {
			return generateLocalMockEvaluation(userContent), nil
		}
		model := cfg.OpenrouterModel
		if model == "" {
			model = "meta-llama/llama-3.3-70b-instruct:free"
		}
		return callOpenAICompatible(client, "https://openrouter.ai/api/v1/chat/completions", cfg.OpenrouterApiKey, model, systemInstruction, userContent, map[string]string{
			"HTTP-Referer": "https://github.com/ngtkien/VaultLingo",
			"X-Title":      "VaultLingo",
		})
	}

	// 4. Groq (Free & Ultra Fast)
	if cfg.AiProvider == "groq" {
		if cfg.GroqApiKey == "" {
			return generateLocalMockEvaluation(userContent), nil
		}
		model := cfg.GroqModel
		if model == "" {
			model = "llama-3.3-70b-versatile"
		}
		return callOpenAICompatible(client, "https://api.groq.com/openai/v1/chat/completions", cfg.GroqApiKey, model, systemInstruction, userContent, nil)
	}

	// 5. Local Ollama (100% Free & Offline)
	if cfg.AiProvider == "ollama" {
		url := cfg.OllamaUrl
		if url == "" {
			url = "http://localhost:11434"
		}
		model := cfg.OllamaModel
		if model == "" {
			model = "llama3:latest"
		}

		prompt := userContent
		if systemInstruction != "" {
			prompt = fmt.Sprintf("%s\n\n%s", systemInstruction, userContent)
		}

		payload := map[string]interface{}{
			"model":  model,
			"prompt": prompt,
			"stream": false,
		}
		bodyBytes, _ := json.Marshal(payload)
		resp, err := client.Post(url+"/api/generate", "application/json", bytes.NewBuffer(bodyBytes))
		if err != nil {
			return "", fmt.Errorf("failed to connect to Ollama at %s: %w", url, err)
		}
		defer resp.Body.Close()

		var res struct {
			Response string `json:"response"`
		}
		_ = json.NewDecoder(resp.Body).Decode(&res)
		return res.Response, nil
	}

	return generateLocalMockEvaluation(userContent), nil
}

func EvaluateWritingAI(prompt, text, situationVi string, cfg Config) (string, error) {
	if strings.TrimSpace(text) == "" {
		return "Please write something before submitting for evaluation!", nil
	}

	systemInstruction := `You are an expert English writing coach and IELTS examiner.
Evaluate the user's English submission for the given scenario and prompt.
Return your evaluation as a valid JSON object strictly matching this schema:
{
  "score": 7.5,
  "score_label": "Great Effort",
  "overall_feedback": "A concise 1-2 sentence overall summary in Vietnamese praising strong points and highlighting key areas to improve.",
  "prompt_alignment": "Well aligned with the prompt",
  "corrections": [
    {
      "original": "exact original mistake",
      "correction": "exact corrected version",
      "reason": "Brief grammatical explanation in Vietnamese"
    }
  ],
  "alternatives": [
    {
      "style": "Professional",
      "text": "A natural, polished native sentence suitable for workplace/formal communication."
    },
    {
      "style": "Casual / Quick Slack",
      "text": "A natural, concise native sentence suitable for casual messaging."
    }
  ],
  "vocabulary_highlights": [
    {
      "term": "useful phrase / collocation",
      "meaning": "Vietnamese explanation of how to use it"
    }
  ]
}

If you cannot format as JSON, provide clear labeled markdown.`

	userContent := fmt.Sprintf(`[Context]: %s
[Prompt]: %s
[User Submission]:
"%s"`, situationVi, prompt, text)

	return CallAI(systemInstruction, userContent, cfg)
}

func callOpenAICompatible(client *http.Client, endpoint, apiKey, model, systemPrompt, userPrompt string, extraHeaders map[string]string) (string, error) {
	payload := map[string]interface{}{
		"model": model,
		"messages": []map[string]string{
			{"role": "system", "content": systemPrompt},
			{"role": "user", "content": userPrompt},
		},
		"temperature": 0.3,
	}

	bodyBytes, _ := json.Marshal(payload)
	req, err := http.NewRequest("POST", endpoint, bytes.NewBuffer(bodyBytes))
	if err != nil {
		return "", err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)
	for k, v := range extraHeaders {
		req.Header.Set(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("API request to %s failed: %w", endpoint, err)
	}
	defer resp.Body.Close()

	bodyResp, _ := io.ReadAll(resp.Body)
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("API error (code %d): %s", resp.StatusCode, string(bodyResp))
	}

	var chatResp struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	if err := json.Unmarshal(bodyResp, &chatResp); err != nil || len(chatResp.Choices) == 0 {
		return string(bodyResp), nil
	}

	return chatResp.Choices[0].Message.Content, nil
}

func generateLocalMockEvaluation(text string) string {
	wordCount := len(strings.Fields(text))
	mockJSON := map[string]interface{}{
		"score":            8.0,
		"score_label":      "Good Effort",
		"overall_feedback": fmt.Sprintf("Bài viết dài %d từ, ngữ cảnh diễn đạt rõ ràng và đúng trọng tâm yêu cầu.", wordCount),
		"prompt_alignment": "Well aligned with scenario",
		"corrections": []map[string]string{
			{
				"original":   "Preview mode",
				"correction": "Configure AI Provider in Settings",
				"reason":     "Để nhận phân tích ngữ pháp thời gian thực từ AI.",
			},
		},
		"alternatives": []map[string]string{
			{
				"style": "Professional",
				"text":  text,
			},
		},
		"vocabulary_highlights": []map[string]string{
			{
				"term":    "workplace communication",
				"meaning": "Giao tiếp chuyên nghiệp trong môi trường công sở.",
			},
		},
	}
	bytesOut, _ := json.MarshalIndent(mockJSON, "", "  ")
	return string(bytesOut)
}
