package backend

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
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
			SituationVi:  "Bạn đang bị kẹt xe và sẽ vào muộn 20 phút. Hãy viết tin nhắn thông báo cho nhóm.",
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

func EvaluateWritingAI(prompt, text, situationVi, apiKey, provider, ollamaUrl, ollamaModel string) (string, error) {
	if strings.TrimSpace(text) == "" {
		return "Please write something before submitting for evaluation!", nil
	}

	systemInstruction := `You are an expert English writing coach. 
Evaluate the user's short English submission for the given scenario and prompt.
Provide structured, constructive, and friendly feedback in Vietnamese and English:

1. **Overall Rating & Score (x/10)**: Quick praise and overall impression.
2. **Grammar & Spelling Fixes**: Point out exact errors and provide corrected versions.
3. **Natural Phrasing (Diễn đạt tự nhiên hơn)**: Offer 1-2 native-sounding alternatives (Professional & Casual).
4. **Vocabulary Highlight**: Comment on word choices or suggest 2 useful idiomatic collocations.`

	userContent := fmt.Sprintf(`[Tình huống]: %s
[Đề bài]: %s
[Bài viết của học viên]:
"%s"`, situationVi, prompt, text)

	client := &http.Client{Timeout: 30 * time.Second}

	if provider == "ollama" {
		if ollamaUrl == "" {
			ollamaUrl = "http://localhost:11434"
		}
		if ollamaModel == "" {
			ollamaModel = "llama3:latest"
		}

		payload := map[string]interface{}{
			"model":  ollamaModel,
			"prompt": fmt.Sprintf("%s\n\n%s", systemInstruction, userContent),
			"stream": false,
		}
		bodyBytes, _ := json.Marshal(payload)
		resp, err := client.Post(ollamaUrl+"/api/generate", "application/json", bytes.NewBuffer(bodyBytes))
		if err != nil {
			return "", fmt.Errorf("failed to connect to Ollama at %s: %w", ollamaUrl, err)
		}
		defer resp.Body.Close()

		var res struct {
			Response string `json:"response"`
		}
		_ = json.NewDecoder(resp.Body).Decode(&res)
		return res.Response, nil
	}

	// Default to Google Gemini API
	if apiKey == "" {
		// Use environment variable if available
		// Or provide fallback simulated review
		return generateLocalMockEvaluation(text), nil
	}

	url := fmt.Sprintf("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=%s", apiKey)
	reqBody := map[string]interface{}{
		"contents": []map[string]interface{}{
			{
				"parts": []map[string]string{
					{"text": fmt.Sprintf("%s\n\n%s", systemInstruction, userContent)},
				},
			},
		},
	}
	bodyBytes, _ := json.Marshal(reqBody)
	resp, err := client.Post(url, "application/json", bytes.NewBuffer(bodyBytes))
	if err != nil {
		return "", fmt.Errorf("Gemini API request failed: %w", err)
	}
	defer resp.Body.Close()

	bodyResp, _ := io.ReadAll(resp.Body)
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("Gemini API error (code %d): %s", resp.StatusCode, string(bodyResp))
	}

	var geminiResp struct {
		Candidates []struct {
			Content struct {
				Parts []struct {
					Text string `json:"text"`
				} `json:"parts"`
			} `json:"content"`
		} `json:"candidates"`
	}
	if err := json.Unmarshal(bodyResp, &geminiResp); err != nil || len(geminiResp.Candidates) == 0 || len(geminiResp.Candidates[0].Content.Parts) == 0 {
		return string(bodyResp), nil
	}

	return geminiResp.Candidates[0].Content.Parts[0].Text, nil
}

func generateLocalMockEvaluation(text string) string {
	wordCount := len(strings.Fields(text))
	return fmt.Sprintf(`### 🌟 Đánh giá & Nhận xét AI (Chế độ Local)
* **Số từ**: %d từ
* **Độ trôi chảy**: Tốt, truyền đạt đúng trọng tâm tình huống.

#### 💡 Gợi ý nâng cao & Cách diễn đạt tự nhiên hơn:
- Đảm bảo thì câu đồng nhất và dùng từ nối mượt mà.
- *(Để nhận nhận xét AI chuyên sâu chi tiết từng câu từ Gemini 2.5 Flash, bạn vui lòng nhập Gemini API Key trong phần Cài đặt).*`, wordCount)
}
