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

// GetEffectiveTranslationConfig resolves the specific AI config dedicated to Paragraph Translator.
// GetEffectiveTranslationConfig resolves the specific AI config dedicated to Paragraph Translator.
// If TranslationProvider is set to "default" or empty, it inherits the global AiProvider and its settings without mutation.
func GetEffectiveTranslationConfig(cfg Config) Config {
	if cfg.TranslationProvider == "" || cfg.TranslationProvider == "default" {
		return cfg
	}

	transCfg := cfg
	transCfg.AiProvider = cfg.TranslationProvider
	if cfg.TranslationModel != "" {
		switch transCfg.AiProvider {
		case "groq":
			transCfg.GroqModel = cfg.TranslationModel
		case "ollama":
			transCfg.OllamaModel = cfg.TranslationModel
		case "openrouter":
			transCfg.OpenrouterModel = cfg.TranslationModel
		case "agy":
			transCfg.AgyModel = cfg.TranslationModel
		case "opencode":
			transCfg.OpencodeModel = cfg.TranslationModel
		}
	}
	return transCfg
}

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

	// Resolve dedicated Translation AI config (allows separating Translation AI from Writing AI)
	effectiveCfg := GetEffectiveTranslationConfig(cfg)

	responseRaw, err := CallAI(systemPrompt, userPrompt, effectiveCfg)
	if err != nil {
		return TranslationResult{}, fmt.Errorf("AI translation failed: %w", err)
	}

	result := parseTranslationResponse(responseRaw, sourceLang, targetLang, tone)
	return result, nil
}

// parseTranslationResponse cleanly parses raw AI responses, stripping think tags, markdown code blocks,
// extracting valid JSON objects, and preventing raw JSON/thinking output from leaking into the UI.
func parseTranslationResponse(responseRaw, sourceLang, targetLang, tone string) TranslationResult {
	cleaned := strings.TrimSpace(responseRaw)

	// 1. Strip reasoning / thinking tags (<think>...</think>, <thought>...</thought>)
	reThink := regexp.MustCompile(`(?is)<(think|thought)>.*?</(think|thought)>`)
	cleaned = strings.TrimSpace(reThink.ReplaceAllString(cleaned, ""))

	// 2. Try extracting JSON object from markdown code blocks or outermost braces { ... }
	var jsonStr string
	reCodeBlock := regexp.MustCompile(`(?is)` + "```" + `(?:json)?\s*(\{[\s\S]*?\})\s*` + "```")
	if match := reCodeBlock.FindStringSubmatch(cleaned); len(match) > 1 {
		jsonStr = strings.TrimSpace(match[1])
	} else {
		firstBrace := strings.Index(cleaned, "{")
		lastBrace := strings.LastIndex(cleaned, "}")
		if firstBrace != -1 && lastBrace != -1 && lastBrace > firstBrace {
			jsonStr = strings.TrimSpace(cleaned[firstBrace : lastBrace+1])
		}
	}

	var result TranslationResult
	parsedSuccessfully := false

	if jsonStr != "" {
		// Clean trailing commas in JSON object/arrays (common LLM JSON syntax error)
		reTrailingCommas := regexp.MustCompile(`,\s*([}\]])`)
		fixedJSON := reTrailingCommas.ReplaceAllString(jsonStr, "$1")

		if err := json.Unmarshal([]byte(fixedJSON), &result); err == nil && strings.TrimSpace(result.TranslatedText) != "" {
			parsedSuccessfully = true
		}
	}

	// 3. Fallback: regex extraction if JSON unmarshaling failed but key fields exist
	if !parsedSuccessfully {
		reTrans := regexp.MustCompile(`(?is)"translated_text"\s*:\s*"((?:[^"\\]|\\.)*)"`)
		if match := reTrans.FindStringSubmatch(cleaned); len(match) > 1 {
			result.TranslatedText = unescapeJSONString(match[1])
			parsedSuccessfully = true

			// Also attempt to extract vocabulary
			reVocabWord := regexp.MustCompile(`(?is)"word"\s*:\s*"([^"]+)"[\s\S]*?"pos"\s*:\s*"([^"]*)"[\s\S]*?"meaning"\s*:\s*"([^"]*)"`)
			for _, m := range reVocabWord.FindAllStringSubmatch(cleaned, -1) {
				if len(m) >= 4 {
					result.KeyVocabulary = append(result.KeyVocabulary, ExtractedVocab{
						Word:    m[1],
						POS:     m[2],
						Meaning: m[3],
					})
				}
			}
		}
	}

	// 4. Final safety fallback: If no structured JSON could be parsed, extract clean text only.
	// Ensure we NEVER output raw JSON braces or think tags into the UI.
	if !parsedSuccessfully || strings.TrimSpace(result.TranslatedText) == "" {
		fallbackText := cleaned
		// Remove any remaining code fences
		reFence := regexp.MustCompile("```(?:json)?|```")
		fallbackText = reFence.ReplaceAllString(fallbackText, "")

		// Remove common conversational intros
		reIntro := regexp.MustCompile(`(?i)^(here is the translation|dưới đây là bản dịch|bản dịch là|translation:)\s*[:\-]?\s*`)
		fallbackText = reIntro.ReplaceAllString(strings.TrimSpace(fallbackText), "")

		result.TranslatedText = strings.TrimSpace(fallbackText)
		if result.KeyVocabulary == nil {
			result.KeyVocabulary = []ExtractedVocab{}
		}
		if result.NuanceNotes == nil {
			result.NuanceNotes = []string{}
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

	return result
}

func unescapeJSONString(s string) string {
	var out string
	if err := json.Unmarshal([]byte(`"`+s+`"`), &out); err == nil {
		return out
	}
	s = strings.ReplaceAll(s, `\"`, `"`)
	s = strings.ReplaceAll(s, `\n`, "\n")
	s = strings.ReplaceAll(s, `\t`, "\t")
	return s
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
