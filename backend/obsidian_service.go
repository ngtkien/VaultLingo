package backend

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"time"
)

func ExpandPath(path string) string {
	if strings.HasPrefix(path, "~/") || path == "~" {
		home, err := os.UserHomeDir()
		if err == nil {
			path = filepath.Join(home, strings.TrimPrefix(path, "~/"))
		}
	}
	return path
}

func GetDefaultVaultPath() string {
	home, _ := os.UserHomeDir()
	// Check common Obsidian vault locations
	candidates := []string{
		filepath.Join(home, "Obsidian", "ZederVault"),
		filepath.Join(home, "Obsidian"),
		filepath.Join(home, "Documents", "Obsidian"),
	}
	for _, p := range candidates {
		if _, err := os.Stat(p); err == nil {
			return p
		}
	}
	return filepath.Join(home, "Obsidian")
}

func SaveWordToObsidian(item Word, customVaultPath string) (ObsidianSaveResult, error) {
	vaultPath := ExpandPath(customVaultPath)
	if vaultPath == "" {
		vaultPath = GetDefaultVaultPath()
	}

	vocabDir := filepath.Join(vaultPath, "English", "Vocab")
	topicDir := filepath.Join(vocabDir, item.Topic)
	if err := os.MkdirAll(topicDir, 0755); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	today := time.Now().Format("2006-01-02")
	tomorrow := time.Now().AddDate(0, 0, 1).Format("2006-01-02")

	fileName := fmt.Sprintf("%s_Vol_01.md", item.Topic)
	filePath := filepath.Join(topicDir, fileName)

	srsTag := fmt.Sprintf(`<!-- srs: {"next_review": "%s", "interval": 1, "repetitions": 0, "status": "learning", "created": "%s"} -->`, tomorrow, today)

	displayWord := strings.Title(item.Word)
	pos := strings.Title(item.POS)
	if pos == "" {
		pos = "Noun"
	}
	dictLink := item.DictLink
	if dictLink == "" {
		dictLink = "https://dictionary.cambridge.org/dictionary/english/" + strings.ToLower(item.Word)
	}

	// If file does not exist, create with YAML header
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		content := fmt.Sprintf(`---
title: "%s Vocabulary - Vol 01"
category: "%s"
date: %s
tags:
  - english/vocabulary
  - %s
---

# %s %s Vocabulary (Vol 01)

### 1. %s
- **Phonetic & POS**: `+"`%s` `%s`"+`
- **Definition**: %s
- **Example**: *%s*
- **Reference**: [Cambridge Dictionary](%s)
%s
`, item.TopicTitle, item.Topic, today, item.Topic, item.TopicIcon, item.TopicTitle, displayWord, pos, item.Phonetic, item.DefinitionEn, item.ExampleEn, dictLink, srsTag)

		if err := os.WriteFile(filePath, []byte(content), 0644); err != nil {
			return ObsidianSaveResult{Success: false, Error: err.Error()}, err
		}
		return ObsidianSaveResult{Success: true, Word: displayWord, File: filePath}, nil
	}

	// If file exists, check if word is already present
	data, err := os.ReadFile(filePath)
	if err == nil {
		if strings.Contains(strings.ToLower(string(data)), strings.ToLower(item.Word)) {
			return ObsidianSaveResult{Success: true, Word: displayWord, File: filePath}, nil
		}
	}

	// Append word
	appendContent := fmt.Sprintf(`
---

### %s
- **Phonetic & POS**: `+"`%s` `%s`"+`
- **Definition**: %s
- **Example**: *%s*
- **Reference**: [Cambridge Dictionary](%s)
%s
`, displayWord, pos, item.Phonetic, item.DefinitionEn, item.ExampleEn, dictLink, srsTag)

	f, err := os.OpenFile(filePath, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}
	defer f.Close()

	if _, err := f.WriteString(appendContent); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	return ObsidianSaveResult{Success: true, Word: displayWord, File: filePath}, nil
}

func SaveWritingToObsidian(title, situationVi, prompt, essayText, aiEvaluation, customVaultPath string) (ObsidianSaveResult, error) {
	vaultPath := ExpandPath(customVaultPath)
	if vaultPath == "" {
		vaultPath = GetDefaultVaultPath()
	}

	writingDir := filepath.Join(vaultPath, "English", "Writing")
	if err := os.MkdirAll(writingDir, 0755); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	today := time.Now().Format("2006-01-02")
	safeTitle := regexp.MustCompile(`[^a-zA-Z0-9_-]+`).ReplaceAllString(title, "_")
	fileName := fmt.Sprintf("%s_%s.md", today, safeTitle)
	filePath := filepath.Join(writingDir, fileName)

	wordCount := len(strings.Fields(essayText))

	content := fmt.Sprintf(`---
title: "%s"
date: %s
type: writing-practice
tags:
  - english/writing
---

# ✍️ %s

> **Tình huống**: %s  
> **Đề bài**: %s  
> **Số từ**: %d từ  

---

## 📝 Bài Viết Của Bạn

%s

---

## 🤖 Nhận Xét & Phân Tích Của AI

%s
`, title, today, title, situationVi, prompt, wordCount, essayText, aiEvaluation)

	if err := os.WriteFile(filePath, []byte(content), 0644); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	return ObsidianSaveResult{Success: true, Word: title, File: filePath}, nil
}

func GetSavedObsidianVocab(customVaultPath string) ([]ObsidianItem, error) {
	vaultPath := ExpandPath(customVaultPath)
	if vaultPath == "" {
		vaultPath = GetDefaultVaultPath()
	}

	vocabDir := filepath.Join(vaultPath, "English", "Vocab")
	var items []ObsidianItem

	if _, err := os.Stat(vocabDir); os.IsNotExist(err) {
		return items, nil
	}

	today := time.Now().Format("2006-01-02")

	_ = filepath.Walk(vocabDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() || !strings.HasSuffix(info.Name(), ".md") {
			return nil
		}

		data, err := os.ReadFile(path)
		if err != nil {
			return nil
		}

		content := string(data)
		topicKey := filepath.Base(filepath.Dir(path))
		topicTitle, _ := GetTopicMeta(topicKey)

		// Regex to parse word entries
		wordBlocks := strings.Split(content, "### ")
		for _, block := range wordBlocks[1:] {
			lines := strings.Split(block, "\n")
			if len(lines) == 0 {
				continue
			}

			wordHeader := strings.TrimSpace(lines[0])
			wordHeader = regexp.MustCompile(`^[0-9]+\.\s*`).ReplaceAllString(wordHeader, "")

			item := ObsidianItem{
				Word:       wordHeader,
				TopicKey:   topicKey,
				TopicTitle: topicTitle,
				FilePath:   path,
				Status:     "learning",
			}

			for _, line := range lines {
				if strings.HasPrefix(line, "- **Definition**:") {
					item.Definition = strings.TrimSpace(strings.TrimPrefix(line, "- **Definition**:"))
				} else if strings.HasPrefix(line, "- **Example**:") {
					item.Example = strings.TrimSpace(strings.TrimPrefix(line, "- **Example**:"))
				} else if strings.HasPrefix(line, "- **Phonetic & POS**:") {
					item.Phonetic = strings.TrimSpace(strings.TrimPrefix(line, "- **Phonetic & POS**:"))
				} else if strings.Contains(line, "<!-- srs:") {
					srsRegex := regexp.MustCompile(`<!-- srs:\s*(\{.*?\})\s*-->`)
					matches := srsRegex.FindStringSubmatch(line)
					if len(matches) > 1 {
						var srsMeta struct {
							NextReview  string `json:"next_review"`
							Interval    int    `json:"interval"`
							Repetitions int    `json:"repetitions"`
							Status      string `json:"status"`
						}
						if err := json.Unmarshal([]byte(matches[1]), &srsMeta); err == nil {
							item.NextReview = srsMeta.NextReview
							item.Interval = srsMeta.Interval
							item.Repetitions = srsMeta.Repetitions
							item.Status = srsMeta.Status
							item.IsDue = item.NextReview <= today
						}
					}
				}
			}

			if item.Word != "" {
				items = append(items, item)
			}
		}

		return nil
	})

	return items, nil
}

func UpdateObsidianSrsReview(wordName, filePath string, rating int) error {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return err
	}

	content := string(data)
	today := time.Now()

	// Find the block containing wordName
	blocks := strings.Split(content, "### ")
	var newBlocks []string
	newBlocks = append(newBlocks, blocks[0])

	for _, block := range blocks[1:] {
		if strings.Contains(strings.ToLower(block), strings.ToLower(wordName)) {
			// Extract existing SRS info
			interval := 1
			repetitions := 0

			srsRegex := regexp.MustCompile(`<!-- srs:\s*(\{.*?\})\s*-->`)
			matches := srsRegex.FindStringSubmatch(block)
			if len(matches) > 1 {
				var meta struct {
					Interval    int `json:"interval"`
					Repetitions int `json:"repetitions"`
				}
				_ = json.Unmarshal([]byte(matches[1]), &meta)
				interval = meta.Interval
				repetitions = meta.Repetitions
			}

			if rating < 2 {
				repetitions = 0
				interval = 1
			} else {
				if repetitions == 0 {
					interval = 1
				} else if repetitions == 1 {
					interval = 6
				} else {
					interval = interval * 2
				}
				repetitions++
			}

			nextReview := today.AddDate(0, 0, interval).Format("2006-01-02")
			newSrsTag := fmt.Sprintf(`<!-- srs: {"next_review": "%s", "interval": %d, "repetitions": %d, "status": "reviewing"} -->`, nextReview, interval, repetitions)

			if srsRegex.MatchString(block) {
				block = srsRegex.ReplaceAllString(block, newSrsTag)
			} else {
				block = block + "\n" + newSrsTag + "\n"
			}
		}
		newBlocks = append(newBlocks, block)
	}

	newContent := strings.Join(newBlocks, "### ")
	return os.WriteFile(filePath, []byte(newContent), 0644)
}

func OpenInObsidian(filePath string) error {
	var cmd *exec.Cmd
	switch runtime.GOOS {
	case "darwin":
		cmd = exec.Command("open", filePath)
	case "linux":
		cmd = exec.Command("xdg-open", filePath)
	default:
		cmd = exec.Command("xdg-open", filePath)
	}
	return cmd.Start()
}
