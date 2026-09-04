package backend

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// TranslateParagraph handles bidirectional translation (EN <-> VI) with deep linguistic analysis
func TranslateParagraph(text, sourceLang, targetLang, tone string, cfg Config) (TranslationResult, error) {
	trimmed := strings.TrimSpace(text)
	if trimmed == "" {
		return TranslationResult{}, fmt.Errorf("text cannot be empty")
	}

	if sourceLang == "" {
		sourceLang = "English"
	}
	if targetLang == "" {
		targetLang = "Vietnamese"
	}
	if tone == "" {
		tone = "Editorial / Natural"
	}

	systemPrompt := fmt.Sprintf(`You are an elite bilingual translator and linguist specializing in English and Vietnamese.
Translate the provided text faithfully, capturing nuances, idiomatic expressions, and natural rhythm.
Target translation tone style: %s

You MUST respond STRICTLY with a single valid JSON object. Do not include markdown code fences (like `+"`"+`json), commentary, or extra text.
Required JSON schema:
{
  "translated_text": "High quality natural translation of the full text",
  "source_lang": "%s",
  "target_lang": "%s",
  "tone": "%s",
  "key_vocabulary": [
    {
      "word": "key term / collocations / idioms",
      "pos": "noun/verb/adj/idiom/collocation",
      "phonetic": "/.../",
      "meaning": "Contextual meaning in the target language"
    }
  ],
  "nuance_notes": [
    "Short practical note explaining notable grammar structures, register, or nuance traps"
  ]
}`, tone, sourceLang, targetLang, tone)

	userPrompt := fmt.Sprintf("Translate the following text from %s to %s with %s tone:\n\n%s", sourceLang, targetLang, tone, trimmed)

	responseRaw, err := CallAI(systemPrompt, userPrompt, cfg)
	if err != nil {
		return TranslationResult{}, fmt.Errorf("AI translation failed: %w", err)
	}

	cleanJSON := strings.TrimSpace(responseRaw)
	if strings.HasPrefix(cleanJSON, "```json") {
		cleanJSON = strings.TrimPrefix(cleanJSON, "```json")
		cleanJSON = strings.TrimSuffix(cleanJSON, "```")
	} else if strings.HasPrefix(cleanJSON, "```") {
		cleanJSON = strings.TrimPrefix(cleanJSON, "```")
		cleanJSON = strings.TrimSuffix(cleanJSON, "```")
	}
	cleanJSON = strings.TrimSpace(cleanJSON)

	var result TranslationResult
	if err := json.Unmarshal([]byte(cleanJSON), &result); err != nil {
		// Fallback: If JSON unmarshaling fails, treat the response text as the translated text
		result = TranslationResult{
			TranslatedText: strings.TrimSpace(responseRaw),
			SourceLang:     sourceLang,
			TargetLang:     targetLang,
			Tone:           tone,
			KeyVocabulary:  []ExtractedVocab{},
			NuanceNotes:    []string{},
		}
	}

	if result.SourceLang == "" {
		result.SourceLang = sourceLang
	}
	if result.TargetLang == "" {
		result.TargetLang = targetLang
	}
	if result.Tone == "" {
		result.Tone = tone
	}

	return result, nil
}

// SaveTranslationToObsidian saves the bilingual translation and extracted vocabulary to the user's Obsidian Vault
func SaveTranslationToObsidian(sourceText, targetText, sourceLang, targetLang, tone string, vocab []ExtractedVocab, customVaultPath string) (ObsidianSaveResult, error) {
	vaultPath := ExpandPath(customVaultPath)
	if vaultPath == "" {
		vaultPath = GetDefaultVaultPath()
	}

	transDir := filepath.Join(vaultPath, "English", "Translations")
	if err := os.MkdirAll(transDir, 0755); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	today := time.Now().Format("2006-01-02")

	// Generate a concise title preview from source text
	words := strings.Fields(sourceText)
	titlePreview := "Paragraph"
	if len(words) > 0 {
		end := 5
		if len(words) < end {
			end = len(words)
		}
		titlePreview = strings.Join(words[:end], " ")
	}

	safeTitle := regexp.MustCompile(`[^a-zA-Z0-9_-]+`).ReplaceAllString(titlePreview, "_")
	safeTitle = strings.Trim(safeTitle, "_")
	if len(safeTitle) > 35 {
		safeTitle = safeTitle[:35]
	}
	if safeTitle == "" {
		safeTitle = "Translation"
	}

	fileName := fmt.Sprintf("%s_%s_%d.md", today, safeTitle, time.Now().Unix()%10000)
	filePath := filepath.Join(transDir, fileName)

	var vocabMD strings.Builder
	if len(vocab) > 0 {
		vocabMD.WriteString("## 📚 Key Vocabulary & Expressions\n\n")
		for _, v := range vocab {
			phon := ""
			if v.Phonetic != "" {
				phon = fmt.Sprintf(" `[%s]`", v.Phonetic)
			}
			pos := ""
			if v.POS != "" {
				pos = fmt.Sprintf(" *(%s)*", v.POS)
			}
			vocabMD.WriteString(fmt.Sprintf("- **%s**%s%s: %s\n", v.Word, pos, phon, v.Meaning))
		}
		vocabMD.WriteString("\n---\n\n")
	}

	content := fmt.Sprintf(`---
title: "Translation: %s"
date: %s
type: translation
source_lang: "%s"
target_lang: "%s"
tone: "%s"
tags:
  - english/translation
---

# ✍️ Bilingual Translation (%s ➔ %s)

> **Tone**: %s | **Date**: %s

---

## 📖 Source Text (%s)

%s

---

## 🎯 Translated Text (%s)

%s

---

%s`, titlePreview, today, sourceLang, targetLang, tone, sourceLang, targetLang, tone, today, sourceLang, sourceText, targetLang, targetText, vocabMD.String())

	if err := os.WriteFile(filePath, []byte(content), 0644); err != nil {
		return ObsidianSaveResult{Success: false, Error: err.Error()}, err
	}

	return ObsidianSaveResult{Success: true, Word: titlePreview, File: filePath}, nil
}
