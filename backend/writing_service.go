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

func EvaluateWritingAI(prompt, text, situationVi string, cfg Config) (string, error) {
	if strings.TrimSpace(text) == "" {
		return "Please write something before submitting for evaluation!", nil
	}

	systemInstruction := `You are an expert English writing coach. 
Evaluate the user's short English submission for the given scenario and prompt.
Provide structured, constructive, and friendly feedback in clear Markdown:

1. **Overall Rating & Score (x/10)**: Quick praise and overall impression.
2. **Grammar & Spelling Fixes**: Point out exact errors and provide corrected versions.
3. **Natural Phrasing (More Natural Alternatives)**: Offer 1-2 native-sounding alternatives (Professional & Casual).
4. **Vocabulary Highlight**: Comment on word choices or suggest 2 useful idiomatic collocations.`

	userContent := fmt.Sprintf(`[Context]: %s
[Prompt]: %s
[User Submission]:
"%s"`, situationVi, prompt, text)

	// 1. Antigravity CLI (Native system-authenticated agy CLI)
	if cfg.AiProvider == "agy" {
		fullPrompt := fmt.Sprintf("%s\n\n%s", systemInstruction, userContent)
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

	// 2. OpenRouter (Free & Open Source Models)
	if cfg.AiProvider == "openrouter" {
		if cfg.OpenrouterApiKey == "" {
			return generateLocalMockEvaluation(text), nil
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

	// 3. Groq (Free & Ultra Fast)
	if cfg.AiProvider == "groq" {
		if cfg.GroqApiKey == "" {
			return generateLocalMockEvaluation(text), nil
		}
		model := cfg.GroqModel
		if model == "" {
			model = "llama-3.3-70b-versatile"
		}
		return callOpenAICompatible(client, "https://api.groq.com/openai/v1/chat/completions", cfg.GroqApiKey, model, systemInstruction, userContent, nil)
	}

	// 4. Local Ollama (100% Free & Offline)
	if cfg.AiProvider == "ollama" {
		url := cfg.OllamaUrl
		if url == "" {
			url = "http://localhost:11434"
		}
		model := cfg.OllamaModel
		if model == "" {
			model = "llama3:latest"
		}

		payload := map[string]interface{}{
			"model":  model,
			"prompt": fmt.Sprintf("%s\n\n%s", systemInstruction, userContent),
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

	return generateLocalMockEvaluation(text), nil
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
	return fmt.Sprintf(`### 🌟 AI Evaluation Summary (Local Preview)
* **Word Count**: %d words
* **Clarity & Tone**: Clear and appropriate for the context.

#### 💡 Pro Tips:
- Maintain consistent tense usage and smooth transition connectives.
- *(To receive deep feedback, please configure Antigravity CLI / OpenRouter / Groq in Settings).*`, wordCount)
}
