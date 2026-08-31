package backend

import (
	"database/sql"
	_ "embed"
	"fmt"
	"os"
	"path/filepath"

	_ "modernc.org/sqlite"
)

//go:embed data/vocab.db
var embeddedVocabDB []byte

var DB *sql.DB

func InitDB() (*sql.DB, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		homeDir = "."
	}

	appDataDir := filepath.Join(homeDir, ".local", "share", "VaultLingo")
	_ = os.MkdirAll(appDataDir, 0755)

	dbPath := filepath.Join(appDataDir, "vocab.db")

	// If database doesn't exist in appDataDir, automatically unpack the embedded database
	if _, err := os.Stat(dbPath); os.IsNotExist(err) {
		if len(embeddedVocabDB) > 0 {
			_ = os.WriteFile(dbPath, embeddedVocabDB, 0644)
		}
	}

	// Connect to SQLite
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open sqlite database: %w", err)
	}

	// Ensure SRS table exists
	_, _ = db.Exec(`
		CREATE TABLE IF NOT EXISTS srs_reviews (
			word_id INTEGER PRIMARY KEY,
			interval INTEGER DEFAULT 1,
			repetitions INTEGER DEFAULT 0,
			ease_factor REAL DEFAULT 2.5,
			next_review TEXT,
			last_reviewed TEXT,
			status TEXT DEFAULT 'learning'
		);
	`)

	// Ensure listening_topics table exists
	_, _ = db.Exec(`
		CREATE TABLE IF NOT EXISTS listening_topics (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			topic_id INTEGER UNIQUE NOT NULL,
			title TEXT NOT NULL,
			icon TEXT DEFAULT '🎧',
			audio_url TEXT NOT NULL,
			web_url TEXT,
			qa_json TEXT NOT NULL
		);
	`)

	// Ensure rich linguistic columns exist in words table
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN synonyms_json TEXT DEFAULT '[]';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN antonyms_json TEXT DEFAULT '[]';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN collocations_json TEXT DEFAULT '[]';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN word_family_json TEXT DEFAULT '[]';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN etymology TEXT DEFAULT '';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN mnemonic_hook TEXT DEFAULT '';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN nuance_tips TEXT DEFAULT '';`)
	_, _ = db.Exec(`ALTER TABLE words ADD COLUMN examples_json TEXT DEFAULT '[]';`)

	DB = db
	return db, nil
}
