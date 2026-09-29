package backend

import (
	"encoding/json"
	"strings"
)

func GetReadingPassages() ([]ReadingPassageMeta, error) {
	rows, err := DB.Query(`SELECT id, title, band_level, COALESCE(topic,''), questions_json
		FROM reading_passages ORDER BY band_level, id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []ReadingPassageMeta
	for rows.Next() {
		var m ReadingPassageMeta
		var qjson string
		if err := rows.Scan(&m.ID, &m.Title, &m.BandLevel, &m.Topic, &qjson); err != nil {
			continue
		}
		var sets []ReadingQuestionSet
		if json.Unmarshal([]byte(qjson), &sets) == nil {
			for _, s := range sets {
				m.QuestionCount += len(s.Items)
			}
		}
		out = append(out, m)
	}
	return out, nil
}

func GetReadingPassage(id int) (ReadingPassage, error) {
	var p ReadingPassage
	var qjson string
	err := DB.QueryRow(`SELECT id, title, band_level, COALESCE(topic,''), text, questions_json
		FROM reading_passages WHERE id = ?`, id).
		Scan(&p.ID, &p.Title, &p.BandLevel, &p.Topic, &p.Text, &qjson)
	if err != nil {
		return p, err
	}
	_ = json.Unmarshal([]byte(qjson), &p.Questions)
	p.WordCount = len(strings.Fields(p.Text))
	return p, nil
}

// CheckReadingAnswers grades user answers against stored items.
// Matching is case-insensitive, trimmed; gapfill accepts exact expected string.
func CheckReadingAnswers(passageID int, answers []ReadingAnswerInput) (ReadingResult, error) {
	p, err := GetReadingPassage(passageID)
	if err != nil {
		return ReadingResult{}, err
	}

	given := make(map[int]string, len(answers))
	for _, a := range answers {
		given[a.ItemID] = a.Given
	}

	res := ReadingResult{PassageID: passageID}
	for _, set := range p.Questions {
		for _, item := range set.Items {
			g := strings.TrimSpace(given[item.ID])
			ok := answersEqual(g, item.Answer)
			if ok {
				res.Correct++
			}
			res.Total++
			res.Details = append(res.Details, ReadingAnswerDetail{
				ItemID:      item.ID,
				Question:    item.Question,
				Given:       g,
				Expected:    item.Answer,
				Correct:     ok,
				Explanation: item.Explanation,
			})
		}
	}
	if res.Total > 0 {
		res.Percentage = res.Correct * 100 / res.Total
		res.BandEstimate = readingBandEstimate(res.Percentage)
	}
	return res, nil
}

func answersEqual(given, expected string) bool {
	g := strings.ToLower(strings.TrimSpace(given))
	e := strings.ToLower(strings.TrimSpace(expected))
	if g == e {
		return true
	}
	// Accept alternative answers separated by "|" in the stored answer.
	for _, alt := range strings.Split(e, "|") {
		if g == strings.TrimSpace(alt) {
			return true
		}
	}
	return false
}

// readingBandEstimate maps percentage correct to an approximate IELTS band
// (aligned with the Academic Reading raw-score conversion scaled to any test size).
func readingBandEstimate(pct int) float64 {
	switch {
	case pct >= 95:
		return 9.0
	case pct >= 88:
		return 8.5
	case pct >= 80:
		return 8.0
	case pct >= 75:
		return 7.5
	case pct >= 68:
		return 7.0
	case pct >= 60:
		return 6.5
	case pct >= 53:
		return 6.0
	case pct >= 45:
		return 5.5
	case pct >= 35:
		return 5.0
	case pct >= 28:
		return 4.5
	case pct >= 20:
		return 4.0
	default:
		return 3.5
	}
}
