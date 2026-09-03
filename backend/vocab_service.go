package backend

import (
	"encoding/json"
	"fmt"
	"math"
	"math/rand"
	"strings"
	"time"
)

var TopicMap = map[string]struct {
	Title string
	Icon  string
}{
	"01_Daily_Life_and_Social":      {"Daily Life & Social", "☕"},
	"02_Workplace_and_Business":     {"Workplace & Business", "💼"},
	"03_Current_Events_and_Economy": {"Current Events & Economy", "📰"},
	"04_Science_Tech_and_AI":        {"Science, AI & Tech", "🤖"},
	"05_Travel_and_Culture":         {"Travel & Culture", "✈️"},
	"06_Health_and_Wellness":        {"Health & Wellness", "🏃"},
	"07_Embedded_and_Electronics":   {"Embedded & Electronics", "⚡"},
	"destination_b1":                {"Destination B1", "📘"},
	"destination_b2":                {"Destination B2", "📕"},
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
	// Pick a stable entry for the local calendar day.  RANDOM() made the
	// "daily" card change every time the view was refreshed.
	var count int
	if err := DB.QueryRow(`SELECT COUNT(*) FROM idioms`).Scan(&count); err != nil || count == 0 {
		return Idiom{
			Idiom:     "Think outside the box",
			Phonetic:  "/θɪŋk ˌaʊtˈsaɪd ðə bɒks/",
			MeaningEn: "To think in an original, creative, and unconventional way.",
			MeaningVi: "Tư duy đột phá, sáng tạo khác biệt",
			Example:   "To solve this problem, we must think outside the box.",
			ExampleVi: "Để giải quyết vấn đề này, chúng ta cần tư duy sáng tạo.",
		}, nil
	}

	dayIndex := int(time.Now().Unix() / 86400 % int64(count))
	err := DB.QueryRow(`
		SELECT id, idiom, phonetic, meaning_en, meaning_vi, example, example_vi
		FROM idioms
		ORDER BY id ASC
		LIMIT 1 OFFSET ?
	`, dayIndex).Scan(&idiom.ID, &idiom.Idiom, &idiom.Phonetic, &idiom.MeaningEn, &idiom.MeaningVi, &idiom.Example, &idiom.ExampleVi)

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

// GetQuickQuizExcluding returns a different quiz while there are unseen IDs.
// It lets the UI offer a genuine "next question" control without client-side
// random retries.
func GetQuickQuizExcluding(excludeIDs []int) (Quiz, error) {
	var q Quiz
	var optionsJSON string
	conditions := ""
	args := make([]interface{}, 0, len(excludeIDs))
	if len(excludeIDs) > 0 {
		placeholders := make([]string, len(excludeIDs))
		for i, id := range excludeIDs {
			placeholders[i] = "?"
			args = append(args, id)
		}
		conditions = "WHERE id NOT IN (" + strings.Join(placeholders, ",") + ")"
	}

	err := DB.QueryRow(fmt.Sprintf(`
		SELECT id, category, category_icon, question, options_json, correct, correct_sentence, explanation, tip
		FROM quizzes %s ORDER BY RANDOM() LIMIT 1
	`, conditions), args...).Scan(&q.ID, &q.Category, &q.CategoryIcon, &q.Question, &optionsJSON, &q.Correct, &q.CorrectSentence, &q.Explanation, &q.Tip)
	if err != nil && len(excludeIDs) > 0 {
		return GetQuickQuizExcluding(nil)
	}
	if err != nil {
		return GetQuickQuiz()
	}
	if err := json.Unmarshal([]byte(optionsJSON), &q.Options); err != nil {
		return Quiz{}, err
	}
	return shuffleQuizOptions(q), nil
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
		return shuffleQuizOptions(Quiz{
			Category:        "Prepositions",
			CategoryIcon:    "🎯",
			Question:        "Choose the correct preposition: 'She is really good ___ explaining concepts.'",
			Options:         []string{"A. at", "B. in", "C. on", "D. with"},
			Correct:         "A",
			CorrectSentence: "She is really good at explaining concepts.",
			Explanation:     "We always use 'good AT doing something'.",
			Tip:             "Remember: good AT.",
		}), nil
	}

	if err := json.Unmarshal([]byte(optionsJSON), &q.Options); err != nil {
		return Quiz{}, err
	}
	return shuffleQuizOptions(q), nil
}

// shuffleQuizOptions removes the answer-position pattern from seeded data.
// Options are stored with their display labels, so both the labels and the
// correct key must be regenerated after every shuffle.
func shuffleQuizOptions(q Quiz) Quiz {
	correctText := ""
	cleaned := make([]string, 0, len(q.Options))
	for _, option := range q.Options {
		text := strings.TrimSpace(option)
		if len(text) >= 3 && text[1] == '.' && text[2] == ' ' {
			if string(text[0]) == q.Correct {
				correctText = text[3:]
			}
			text = text[3:]
		}
		cleaned = append(cleaned, text)
	}
	if correctText == "" || len(cleaned) < 2 {
		return q
	}
	rand.Shuffle(len(cleaned), func(i, j int) { cleaned[i], cleaned[j] = cleaned[j], cleaned[i] })
	q.Options = make([]string, len(cleaned))
	for i, text := range cleaned {
		label := string(rune('A' + i))
		q.Options[i] = label + ". " + text
		if text == correctText {
			q.Correct = label
		}
	}
	return q
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

func LookupWordInDB(query string) (*Word, error) {
	query = strings.TrimSpace(query)
	if query == "" {
		return nil, fmt.Errorf("empty query")
	}

	var w Word
	err := DB.QueryRow(`
		SELECT w.id, w.word, w.pos, w.phonetic, w.definition_en, w.definition_vi, 
		       w.example_en, w.example_vi, w.level, w.topic,
		       COALESCE(s.interval, 1), COALESCE(s.repetitions, 0), 
		       COALESCE(s.ease_factor, 2.5), COALESCE(s.next_review, ''), 
		       COALESCE(s.status, 'new'),
		       COALESCE(w.synonyms_json, '[]'),
		       COALESCE(w.antonyms_json, '[]'),
		       COALESCE(w.collocations_json, '[]'),
		       COALESCE(w.word_family_json, '[]'),
		       COALESCE(w.etymology, ''),
		       COALESCE(w.mnemonic_hook, ''),
		       COALESCE(w.nuance_tips, ''),
		       COALESCE(w.examples_json, '[]')
		FROM words w
		LEFT JOIN srs_reviews s ON w.id = s.word_id
		WHERE LOWER(w.word) = LOWER(?)
		LIMIT 1
	`, query).Scan(
		&w.ID, &w.Word, &w.POS, &w.Phonetic, &w.DefinitionEn, &w.DefinitionVi,
		&w.ExampleEn, &w.ExampleVi, &w.Level, &w.Topic,
		&w.Interval, &w.Repetitions, &w.EaseFactor, &w.NextReview, &w.Status,
		&w.SynonymsJSON, &w.AntonymsJSON, &w.CollocationsJSON, &w.WordFamilyJSON,
		&w.Etymology, &w.MnemonicHook, &w.NuanceTips, &w.ExamplesJSON,
	)

	if err != nil {
		return nil, err
	}

	w.RawWord = strings.ToLower(w.Word)
	w.TopicTitle, w.TopicIcon = GetTopicMeta(w.Topic)
	w.DictLink = "https://dictionary.cambridge.org/dictionary/english/" + strings.ReplaceAll(w.RawWord, " ", "-")
	return &w, nil
}

func SaveWordToDB(w Word) error {
	word := strings.TrimSpace(w.Word)
	if word == "" {
		return fmt.Errorf("empty word")
	}

	if w.SynonymsJSON == "" {
		w.SynonymsJSON = "[]"
	}
	if w.AntonymsJSON == "" {
		w.AntonymsJSON = "[]"
	}
	if w.CollocationsJSON == "" {
		w.CollocationsJSON = "[]"
	}
	if w.WordFamilyJSON == "" {
		w.WordFamilyJSON = "[]"
	}
	if w.ExamplesJSON == "" {
		w.ExamplesJSON = "[]"
	}

	_, err := DB.Exec(`
		INSERT INTO words (
			word, pos, phonetic, definition_en, definition_vi, 
			example_en, example_vi, level, topic, source,
			synonyms_json, antonyms_json, collocations_json, word_family_json,
			etymology, mnemonic_hook, nuance_tips, examples_json
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'dictionary', ?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(word) DO UPDATE SET
			pos = excluded.pos,
			phonetic = excluded.phonetic,
			definition_en = excluded.definition_en,
			definition_vi = excluded.definition_vi,
			example_en = excluded.example_en,
			example_vi = excluded.example_vi,
			level = excluded.level,
			topic = excluded.topic,
			synonyms_json = excluded.synonyms_json,
			antonyms_json = excluded.antonyms_json,
			collocations_json = excluded.collocations_json,
			word_family_json = excluded.word_family_json,
			etymology = excluded.etymology,
			mnemonic_hook = excluded.mnemonic_hook,
			nuance_tips = excluded.nuance_tips,
			examples_json = excluded.examples_json
	`,
		word, w.POS, w.Phonetic, w.DefinitionEn, w.DefinitionVi,
		w.ExampleEn, w.ExampleVi, w.Level, w.Topic,
		w.SynonymsJSON, w.AntonymsJSON, w.CollocationsJSON, w.WordFamilyJSON,
		w.Etymology, w.MnemonicHook, w.NuanceTips, w.ExamplesJSON,
	)

	return err
}

// GetWordCount is intentionally a single aggregate query. The UI calls it at
// startup and after a successful dictionary write, never while the user types.
func GetWordCount() (int, error) {
	var count int
	err := DB.QueryRow(`SELECT COUNT(*) FROM words`).Scan(&count)
	return count, err
}

// SearchWordsInDB performs fast prefix and substring search across SQLite words table
func SearchWordsInDB(query string, limit int) ([]Word, error) {
	if strings.TrimSpace(query) == "" {
		return []Word{}, nil
	}
	if limit <= 0 || limit > 50 {
		limit = 10
	}

	q := strings.ToLower(strings.TrimSpace(query))
	sqlQuery := `
		SELECT id, word, pos, phonetic, definition_en, definition_vi, example_en, example_vi, level, topic
		FROM words
		WHERE LOWER(word) LIKE ? OR LOWER(word) LIKE ?
		ORDER BY 
			CASE 
				WHEN LOWER(word) = ? THEN 1
				WHEN LOWER(word) LIKE ? THEN 2
				ELSE 3
			END,
			LENGTH(word) ASC
		LIMIT ?
	`
	rows, err := DB.Query(sqlQuery, q+"%", "%"+q+"%", q, q+"%", limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []Word
	for rows.Next() {
		var w Word
		err := rows.Scan(
			&w.ID, &w.Word, &w.POS, &w.Phonetic,
			&w.DefinitionEn, &w.DefinitionVi,
			&w.ExampleEn, &w.ExampleVi,
			&w.Level, &w.Topic,
		)
		if err == nil {
			results = append(results, w)
		}
	}
	return results, nil
}

func GetListeningTopics() ([]ListeningTopic, error) {
	rows, err := DB.Query(`
		SELECT id, topic_id, title, icon, audio_url, web_url, qa_json
		FROM listening_topics
		ORDER BY id ASC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var topics []ListeningTopic
	for rows.Next() {
		var t ListeningTopic
		var qaJSON string
		if err := rows.Scan(&t.ID, &t.TopicID, &t.Title, &t.Icon, &t.AudioURL, &t.WebURL, &qaJSON); err == nil {
			_ = json.Unmarshal([]byte(qaJSON), &t.QA)
			topics = append(topics, t)
		}
	}
	return topics, nil
}
