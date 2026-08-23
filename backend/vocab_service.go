package backend

import (
	"encoding/json"
	"math"
	"math/rand"
	"strings"
	"time"
)

var TopicMap = map[string]struct {
	Title string
	Icon  string
}{
	"01_Daily_Life_and_Social":       {"Daily Life & Social", "☕"},
	"02_Workplace_and_Business":      {"Workplace & Business", "💼"},
	"03_Current_Events_and_Economy":  {"Current Events & Economy", "📰"},
	"04_Science_Tech_and_AI":         {"Science, AI & Tech", "🤖"},
	"05_Travel_and_Culture":          {"Travel & Culture", "✈️"},
	"06_Health_and_Wellness":         {"Health & Wellness", "🏃"},
	"07_Embedded_and_Electronics":    {"Embedded & Electronics", "⚡"},
	"destination_b1":                 {"Destination B1", "📘"},
	"destination_b2":                 {"Destination B2", "📕"},
}

func GetTopicMeta(topic string) (string, string) {
	if meta, ok := TopicMap[topic]; ok {
		return meta.Title, meta.Icon
	}
	return "General English", "📚"
}

func GetDailyVocab(topicKey string, count int) ([]Word, error) {
	if count <= 0 {
		count = 5
	}

	var words []Word
	var query string
	var args []interface{}

	if topicKey == "" || topicKey == "all" {
		query = `
			SELECT w.id, w.word, w.pos, w.phonetic, w.definition_en, w.definition_vi, 
			       w.example_en, w.example_vi, w.level, w.topic,
			       COALESCE(s.interval, 1), COALESCE(s.repetitions, 0), 
			       COALESCE(s.ease_factor, 2.5), COALESCE(s.next_review, ''), 
			       COALESCE(s.status, 'new')
			FROM words w
			LEFT JOIN srs_reviews s ON w.id = s.word_id
			ORDER BY RANDOM()
			LIMIT ?
		`
		args = append(args, count)
	} else if topicKey == "due_srs" {
		today := time.Now().Format("2006-01-02")
		query = `
			SELECT w.id, w.word, w.pos, w.phonetic, w.definition_en, w.definition_vi, 
			       w.example_en, w.example_vi, w.level, w.topic,
			       s.interval, s.repetitions, s.ease_factor, s.next_review, s.status
			FROM words w
			INNER JOIN srs_reviews s ON w.id = s.word_id
			WHERE s.next_review <= ?
			ORDER BY s.next_review ASC
			LIMIT ?
		`
		args = append(args, today, count)
	} else {
		query = `
			SELECT w.id, w.word, w.pos, w.phonetic, w.definition_en, w.definition_vi, 
			       w.example_en, w.example_vi, w.level, w.topic,
			       COALESCE(s.interval, 1), COALESCE(s.repetitions, 0), 
			       COALESCE(s.ease_factor, 2.5), COALESCE(s.next_review, ''), 
			       COALESCE(s.status, 'new')
			FROM words w
			LEFT JOIN srs_reviews s ON w.id = s.word_id
			WHERE w.topic = ?
			ORDER BY RANDOM()
			LIMIT ?
		`
		args = append(args, topicKey, count)
	}

	rows, err := DB.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var w Word
		err := rows.Scan(
			&w.ID, &w.Word, &w.POS, &w.Phonetic, &w.DefinitionEn, &w.DefinitionVi,
			&w.ExampleEn, &w.ExampleVi, &w.Level, &w.Topic,
			&w.Interval, &w.Repetitions, &w.EaseFactor, &w.NextReview, &w.Status,
		)
		if err != nil {
			continue
		}
		w.RawWord = strings.ToLower(w.Word)
		w.TopicTitle, w.TopicIcon = GetTopicMeta(w.Topic)
		w.DictLink = "https://dictionary.cambridge.org/dictionary/english/" + strings.ReplaceAll(w.RawWord, " ", "-")
		words = append(words, w)
	}

	return words, nil
}

func RecordSrsReview(wordID int, rating int) error {
	// SuperMemo-2 (SM-2) Algorithm: rating from 1 (Again), 2 (Hard), 3 (Good), 4 (Easy)
	var interval, repetitions int
	var easeFactor float64
	var status string

	err := DB.QueryRow(`SELECT interval, repetitions, ease_factor, status FROM srs_reviews WHERE word_id = ?`, wordID).
		Scan(&interval, &repetitions, &easeFactor, &status)

	if err != nil {
		interval = 1
		repetitions = 0
		easeFactor = 2.5
		status = "learning"
	}

	today := time.Now()
	if rating < 2 { // Again / Failed
		repetitions = 0
		interval = 1
		status = "learning"
	} else {
		if repetitions == 0 {
			interval = 1
		} else if repetitions == 1 {
			interval = 6
		} else {
			interval = int(math.Round(float64(interval) * easeFactor))
		}
		repetitions++
		status = "reviewing"
	}

	// Update ease factor: EF' = EF + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
	grade := float64(rating + 1) // 2 to 5
	easeFactor = easeFactor + (0.1 - (5.0-grade)*(0.08+(5.0-grade)*0.02))
	if easeFactor < 1.3 {
		easeFactor = 1.3
	}

	nextReview := today.AddDate(0, 0, interval).Format("2006-01-02")
	lastReviewed := today.Format("2006-01-02")

	_, err = DB.Exec(`
		INSERT INTO srs_reviews (word_id, interval, repetitions, ease_factor, next_review, last_reviewed, status)
		VALUES (?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(word_id) DO UPDATE SET
			interval = excluded.interval,
			repetitions = excluded.repetitions,
			ease_factor = excluded.ease_factor,
			next_review = excluded.next_review,
			last_reviewed = excluded.last_reviewed,
			status = excluded.status
	`, wordID, interval, repetitions, easeFactor, nextReview, lastReviewed, status)

	return err
}

func GetDailyIdiom() (Idiom, error) {
	var idiom Idiom
	err := DB.QueryRow(`
		SELECT id, idiom, phonetic, meaning_en, meaning_vi, example, example_vi
		FROM idioms
		ORDER BY RANDOM()
		LIMIT 1
	`).Scan(&idiom.ID, &idiom.Idiom, &idiom.Phonetic, &idiom.MeaningEn, &idiom.MeaningVi, &idiom.Example, &idiom.ExampleVi)

	if err != nil {
		// Fallback sample idiom
		return Idiom{
			Idiom:     "Think outside the box",
			Phonetic:  "/θɪŋk ˌaʊtˈsaɪd ðə bɒks/",
			MeaningEn: "To think in an original, creative, and unconventional way.",
			MeaningVi: "Tư duy đột phá, sáng tạo khác biệt",
			Example:   "To solve this problem, we must think outside the box.",
			ExampleVi: "Để giải quyết vấn đề này, chúng ta cần tư duy sáng tạo.",
		}, nil
	}
	return idiom, nil
}

func GetQuickQuiz() (Quiz, error) {
	var q Quiz
	var optionsJSON string

	err := DB.QueryRow(`
		SELECT id, category, category_icon, question, options_json, correct, correct_sentence, explanation, tip
		FROM quizzes
		ORDER BY RANDOM()
		LIMIT 1
	`).Scan(&q.ID, &q.Category, &q.CategoryIcon, &q.Question, &optionsJSON, &q.Correct, &q.CorrectSentence, &q.Explanation, &q.Tip)

	if err != nil {
		return Quiz{
			Category:        "Prepositions",
			CategoryIcon:    "🎯",
			Question:        "Choose the correct preposition: 'She is really good ___ explaining concepts.'",
			Options:         []string{"A. at", "B. in", "C. on", "D. with"},
			Correct:         "A",
			CorrectSentence: "She is really good at explaining concepts.",
			Explanation:     "We always use 'good AT doing something'.",
			Tip:             "Remember: good AT.",
		}, nil
	}

	_ = json.Unmarshal([]byte(optionsJSON), &q.Options)
	return q, nil
}

func GetAvailableTopics() []map[string]string {
	return []map[string]string{
		{"key": "all", "title": "All Topics Mix", "icon": "🎲"},
		{"key": "destination_b1", "title": "Destination B1", "icon": "📘"},
		{"key": "destination_b2", "title": "Destination B2", "icon": "📕"},
		{"key": "07_Embedded_and_Electronics", "title": "Embedded & Tech", "icon": "⚡"},
		{"key": "01_Daily_Life_and_Social", "title": "Daily Life & Social", "icon": "☕"},
		{"key": "02_Workplace_and_Business", "title": "Workplace & Career", "icon": "💼"},
		{"key": "03_Current_Events_and_Economy", "title": "Current Events & Economy", "icon": "📰"},
		{"key": "04_Science_Tech_and_AI", "title": "Science, AI & Tech", "icon": "🤖"},
		{"key": "05_Travel_and_Culture", "title": "Travel & Culture", "icon": "✈️"},
		{"key": "06_Health_and_Wellness", "title": "Health & Wellness", "icon": "🏃"},
		{"key": "due_srs", "title": "Due Reviews (SRS)", "icon": "🔄"},
	}
}

func init() {
	rand.Seed(time.Now().UnixNano())
}
