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

var TopicSlugMap = map[string]string{
	"01_Daily_Life_and_Social":      "Daily_Life_and_Social",
	"02_Workplace_and_Business":     "Workplace_and_Business",
	"03_Current_Events_and_Economy": "Current_Events_and_Economy",
	"04_Science_Tech_and_AI":        "Science_Tech_and_AI",
	"05_Travel_and_Culture":         "Travel_and_Culture",
	"06_Health_and_Wellness":        "Health_and_Wellness",
	"07_Embedded_and_Electronics":   "Embedded_and_Electronics",
	"01_Firmware_and_Architecture":  "Firmware_and_Architecture",
	"02_Hardware_and_Circuits":      "Hardware_and_Circuits",
	"03_Protocols_and_Communication": "Protocols_and_Communication",
	"dest_b1":                       "Destination_B1",
	"dest_b2":                       "Destination_B2",
	"destination_b2":                "Destination_B2",
	"destination_b1":                "Destination_B1",
	"08_General_English":            "General_English",
}

func GetCleanTopicSlug(topic string) string {
	if slug, ok := TopicSlugMap[topic]; ok {
		return slug
	}
	return strings.ReplaceAll(topic, " ", "_")
}

func SaveWordToObsidian(item Word, customVaultPath string) (ObsidianSaveResult, error) {
	vaultPath := ExpandPath(customVaultPath)
	if vaultPath == "" {
		vaultPath = GetDefaultVaultPath()
	}

	vocabDir := filepath.Join(vaultPath, "English", "Vocab")
	if err := os.MkdirAll(vocabDir, 0755); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	today := time.Now().Format("2006-01-02")
	tomorrow := time.Now().AddDate(0, 0, 1).Format("2006-01-02")

	topicSlug := GetCleanTopicSlug(item.Topic)
	fileName := fmt.Sprintf("%s.md", topicSlug)
	filePath := filepath.Join(vocabDir, fileName)

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

	topicTitle := item.TopicTitle
	topicIcon := item.TopicIcon
	if topicTitle == "" {
		topicTitle, topicIcon = GetTopicMeta(item.Topic)
	}

	// If file does not exist, create with clean YAML header
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		content := fmt.Sprintf(`---
title: "%s Vocabulary"
category: "%s"
date: %s
tags:
  - english/vocabulary
  - %s
---

# %s %s Vocabulary

### %s
- **Phonetic & POS**: `+"`%s` `%s`"+`
- **Definition**: %s
- **Example**: *%s*
- **Reference**: [Cambridge Dictionary](%s)
%s
`, topicTitle, topicSlug, today, strings.ToLower(strings.ReplaceAll(topicSlug, "_", "-")), topicIcon, topicTitle, displayWord, pos, item.Phonetic, item.DefinitionEn, item.ExampleEn, dictLink, srsTag)

		if err := os.WriteFile(filePath, []byte(content), 0644); err != nil {
			return ObsidianSaveResult{Success: false, Error: err.Error()}, err
		}
		return ObsidianSaveResult{Success: true, Word: displayWord, File: filePath}, nil
	}

	// If file exists, check if word is already present
	data, err := os.ReadFile(filePath)
	if err == nil {
		wordPattern := regexp.MustCompile(`(?mi)^###\s+(?:[0-9]+\.\s*)?` + regexp.QuoteMeta(displayWord) + `(?:\s+` + "`" + `|$)`)
		if wordPattern.Match(data) {
			return ObsidianSaveResult{Success: true, Word: displayWord, File: filePath}, nil
		}
	}

	// Append word cleanly
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

func DeleteWordFromObsidian(wordName, customVaultPath string) (bool, error) {
	vaultPath := ExpandPath(customVaultPath)
	if vaultPath == "" {
		vaultPath = GetDefaultVaultPath()
	}

	vocabDir := filepath.Join(vaultPath, "English", "Vocab")
	if _, err := os.Stat(vocabDir); os.IsNotExist(err) {
		return false, nil
	}

	cleanTarget := strings.ToLower(strings.TrimSpace(wordName))
	deleted := false

	_ = filepath.Walk(vocabDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() || !strings.HasSuffix(info.Name(), ".md") {
			return nil
		}

		data, err := os.ReadFile(path)
		if err != nil {
			return nil
		}

		content := string(data)
		blocks := strings.Split(content, "### ")
		if len(blocks) <= 1 {
			return nil
		}

		var newBlocks []string
		newBlocks = append(newBlocks, blocks[0])
		fileModified := false

		for _, block := range blocks[1:] {
			lines := strings.Split(block, "\n")
			if len(lines) == 0 {
				continue
			}
			header := strings.TrimSpace(lines[0])
			header = regexp.MustCompile(`^[0-9]+\.\s*`).ReplaceAllString(header, "")
			header = strings.Split(header, "`")[0]
			header = strings.ToLower(strings.TrimSpace(header))

			if header == cleanTarget {
				deleted = true
				fileModified = true
				continue
			}

			newBlocks = append(newBlocks, block)
		}

		if fileModified {
			if len(newBlocks) <= 1 {
				// No more words left in this file
				_ = os.Remove(path)
				parent := filepath.Dir(path)
				if parent != vocabDir {
					_ = os.Remove(parent) // remove empty dir
				}
			} else {
				newContent := strings.Join(newBlocks, "### ")
				newContent = regexp.MustCompile(`\n\s*---\s*\n\s*---\s*\n`).ReplaceAllString(newContent, "\n\n---\n\n")
				_ = os.WriteFile(path, []byte(newContent), 0644)
			}
		}

		return nil
	})

	return deleted, nil
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

> **Scenario**: %s  
> **Đề bài**: %s  
> **Word Count**: %d words  

---

## 📝 Your Essay

%s

---

## 🤖 AI Evaluation & Feedback

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
