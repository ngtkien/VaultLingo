package main

import (
	"context"
	"fmt"

	"VaultLingo/backend"
)

// App struct
type App struct {
	ctx context.Context
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	_, err := backend.InitDB()
	if err != nil {
		fmt.Println("Error initializing DB:", err)
	}
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s, welcome to VaultLingo! 🚀", name)
}

// Vocab Methods
func (a *App) GetDailyVocab(topic string, count int) ([]backend.Word, error) {
	return backend.GetDailyVocab(topic, count)
}

func (a *App) RecordSrsReview(wordID int, rating int) error {
	return backend.RecordSrsReview(wordID, rating)
}

func (a *App) GetDailyIdiom() (backend.Idiom, error) {
	return backend.GetDailyIdiom()
}

func (a *App) GetQuickQuiz() (backend.Quiz, error) {
	return backend.GetQuickQuiz()
}

func (a *App) GetAvailableTopics() []map[string]string {
	return backend.GetAvailableTopics()
}

// Dictation Methods
func (a *App) GetDictationSentence(category string) (backend.Dictation, error) {
	return backend.GetDictationSentence(category)
}

func (a *App) CheckDictation(targetSentence, userInput string) backend.DictationResult {
	return backend.CheckDictation(targetSentence, userInput)
}

// Writing Methods
func (a *App) GetWritingPrompt(level string) (backend.WritingPrompt, error) {
	return backend.GetWritingPrompt(level)
}

func (a *App) EvaluateWriting(prompt, text, situationVi string) (string, error) {
	cfg := backend.LoadConfig()
	return backend.EvaluateWritingAI(prompt, text, situationVi, cfg.GeminiApiKey, cfg.AiProvider, cfg.OllamaUrl, cfg.OllamaModel)
}

// Obsidian Vault Methods
func (a *App) SaveWordToObsidian(item backend.Word) (backend.ObsidianSaveResult, error) {
	cfg := backend.LoadConfig()
	return backend.SaveWordToObsidian(item, cfg.ObsidianVaultPath)
}

func (a *App) SaveAllWordsToObsidian(items []backend.Word) ([]backend.ObsidianSaveResult, error) {
	cfg := backend.LoadConfig()
	var results []backend.ObsidianSaveResult
	for _, item := range items {
		res, err := backend.SaveWordToObsidian(item, cfg.ObsidianVaultPath)
		if err == nil {
			results = append(results, res)
		}
	}
	return results, nil
}

func (a *App) SaveWritingToObsidian(title, situationVi, prompt, essayText, aiEvaluation string) (backend.ObsidianSaveResult, error) {
	cfg := backend.LoadConfig()
	return backend.SaveWritingToObsidian(title, situationVi, prompt, essayText, aiEvaluation, cfg.ObsidianVaultPath)
}

func (a *App) GetSavedObsidianVocab() ([]backend.ObsidianItem, error) {
	cfg := backend.LoadConfig()
	return backend.GetSavedObsidianVocab(cfg.ObsidianVaultPath)
}

func (a *App) UpdateObsidianSrsReview(wordName, filePath string, rating int) error {
	return backend.UpdateObsidianSrsReview(wordName, filePath, rating)
}

func (a *App) OpenInObsidian(filePath string) error {
	return backend.OpenInObsidian(filePath)
}

// Configuration Methods
func (a *App) GetConfig() backend.Config {
	return backend.LoadConfig()
}

func (a *App) SaveConfig(cfg backend.Config) error {
	return backend.SaveConfig(cfg)
}
