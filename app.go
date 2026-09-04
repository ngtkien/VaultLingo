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

// Audio Methods (Native OS Player - No GStreamer dependency)
func (a *App) PlayTTS(text string, speed float64) error {
	return backend.PlayTTS(text, speed)
}

func (a *App) PlayAudioUrl(audioUrl string, speed float64) error {
	return backend.PlayAudioUrl(audioUrl, speed)
}

func (a *App) StopAudio() {
	backend.StopAudio()
}

func (a *App) GetVoicesList() []backend.VoiceOption {
	return backend.GetVoicesList()
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

func (a *App) GetQuickQuizExcluding(excludeIDs []int) (backend.Quiz, error) {
	return backend.GetQuickQuizExcluding(excludeIDs)
}

func (a *App) GetAvailableTopics() []map[string]string {
	return backend.GetAvailableTopics()
}

// Dictation Methods
func (a *App) GetDictationCategories() ([]backend.DictationCategoryInfo, error) {
	return backend.GetDictationCategories()
}

func (a *App) GetDictationLevels() ([]backend.DictationLevelInfo, error) {
	return backend.GetDictationLevels()
}

func (a *App) GetDictationSentence(category string) (backend.Dictation, error) {
	return backend.GetDictationSentence(category)
}

func (a *App) GetDictationSentenceWithExclude(category string, excludeIDs []int) (backend.Dictation, error) {
	return backend.GetDictationSentenceWithExclude(category, excludeIDs)
}

func (a *App) GetDictationSentenceFiltered(category string, level string, excludeIDs []int) (backend.Dictation, error) {
	return backend.GetDictationSentenceFiltered(category, level, excludeIDs)
}

func (a *App) CheckDictation(targetSentence, userInput string) backend.DictationResult {
	return backend.CheckDictation(targetSentence, userInput)
}

// Grammar & Question Gym Methods
func (a *App) GetGrammarCategories() ([]backend.GrammarCategoryInfo, error) {
	return backend.GetGrammarCategories()
}

func (a *App) GetGrammarDrill(tenseCategory string, drillType string, excludeIDs []int) (backend.GrammarDrill, error) {
	return backend.GetGrammarDrill(tenseCategory, drillType, excludeIDs)
}

func (a *App) CheckGrammarAnswer(targetQuestion, userInput string) backend.DictationResult {
	return backend.CheckGrammarAnswer(targetQuestion, userInput)
}

// Writing Methods
func (a *App) GetWritingPrompt(level string) (backend.WritingPrompt, error) {
	return backend.GetWritingPrompt(level)
}

func (a *App) QueryAI(systemPrompt, userPrompt string) (string, error) {
	cfg := backend.LoadConfig()
	return backend.CallAI(systemPrompt, userPrompt, cfg)
}

func (a *App) EvaluateWriting(prompt, text, situationVi string) (string, error) {
	cfg := backend.LoadConfig()
	return backend.EvaluateWritingAI(prompt, text, situationVi, cfg)
}


// Translation Methods
func (a *App) TranslateParagraph(text, sourceLang, targetLang, tone string) (backend.TranslationResult, error) {
	cfg := backend.LoadConfig()
	return backend.TranslateParagraph(text, sourceLang, targetLang, tone, cfg)
}

func (a *App) SaveTranslationToObsidian(sourceText, targetText, sourceLang, targetLang, tone string, vocab []backend.ExtractedVocab) (backend.ObsidianSaveResult, error) {
	cfg := backend.LoadConfig()
	return backend.SaveTranslationToObsidian(sourceText, targetText, sourceLang, targetLang, tone, vocab, cfg.ObsidianVaultPath)
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

func (a *App) DeleteWordFromObsidian(wordName string) (bool, error) {
	cfg := backend.LoadConfig()
	return backend.DeleteWordFromObsidian(wordName, cfg.ObsidianVaultPath)
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

func (a *App) SearchWordsInDB(query string, limit int) ([]backend.Word, error) {
	return backend.SearchWordsInDB(query, limit)
}

func (a *App) LookupWordInDB(query string) (*backend.Word, error) {
	return backend.LookupWordInDB(query)
}

func (a *App) SaveWordToDB(w backend.Word) error {
	return backend.SaveWordToDB(w)
}

func (a *App) GetWordCount() (int, error) {
	return backend.GetWordCount()
}

func (a *App) GetListeningTopics() ([]backend.ListeningTopic, error) {
	return backend.GetListeningTopics()
}
