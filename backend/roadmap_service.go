package backend

import (
	"time"
)

// Roadmap progress is keyed by session_id (1-64). The static plan itself lives
// in the frontend (roadmap.ts); this service only persists study state and
// mock test scores, keeping content separate from progress.

func GetRoadmapProgress() (map[int]RoadmapProgress, error) {
	rows, err := DB.Query(`SELECT session_id, status, COALESCE(actual_date,''), COALESCE(note,'') FROM roadmap_progress`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	out := make(map[int]RoadmapProgress)
	for rows.Next() {
		var p RoadmapProgress
		if err := rows.Scan(&p.SessionID, &p.Status, &p.ActualDate, &p.Note); err == nil {
			out[p.SessionID] = p
		}
	}
	return out, nil
}

// MarkSession upserts a session status. "done" records today as actual_date;
// "missed" records the day it was missed; "pending" clears the record.
func MarkSession(sessionID int, status string, note string) error {
	today := time.Now().Format("2006-01-02")
	switch status {
	case "done":
		_, err := DB.Exec(`INSERT INTO roadmap_progress(session_id, status, actual_date, note)
			VALUES(?, 'done', ?, ?)
			ON CONFLICT(session_id) DO UPDATE SET status='done', actual_date=excluded.actual_date, note=excluded.note`,
			sessionID, today, note)
		return err
	case "missed":
		_, err := DB.Exec(`INSERT INTO roadmap_progress(session_id, status, actual_date, note)
			VALUES(?, 'missed', ?, ?)
			ON CONFLICT(session_id) DO UPDATE SET status='missed', actual_date=excluded.actual_date, note=excluded.note`,
			sessionID, today, note)
		return err
	default: // pending → reset
		_, err := DB.Exec(`DELETE FROM roadmap_progress WHERE session_id = ?`, sessionID)
		return err
	}
}

func AddMockScore(skill string, band float64, note string) error {
	_, err := DB.Exec(`INSERT INTO mock_scores(skill, band, taken_at, note) VALUES(?, ?, ?, ?)`,
		skill, band, time.Now().Format("2006-01-02 15:04"), note)
	return err
}

func GetMockScores() ([]MockScore, error) {
	rows, err := DB.Query(`SELECT id, skill, band, taken_at, COALESCE(note,'') FROM mock_scores ORDER BY taken_at DESC`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []MockScore
	for rows.Next() {
		var m MockScore
		if err := rows.Scan(&m.ID, &m.Skill, &m.Band, &m.TakenAt, &m.Note); err == nil {
			out = append(out, m)
		}
	}
	return out, nil
}

func DeleteMockScore(id int) error {
	_, err := DB.Exec(`DELETE FROM mock_scores WHERE id = ?`, id)
	return err
}
