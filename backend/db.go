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

	// Existing installations keep their personal SQLite file. Import new
	// packaged lessons once instead of leaving them on the old content set.
	if err := migrateBundledContent(db, appDataDir); err != nil {
		fmt.Println("Content migration warning:", err)
	}

	DB = db
	return db, nil
}

const bundledContentVersion = 2

func migrateBundledContent(db *sql.DB, appDataDir string) error {
	_, err := db.Exec(`CREATE TABLE IF NOT EXISTS content_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)`)
	if err != nil {
		return err
	}
	var version int
	_ = db.QueryRow(`SELECT CAST(value AS INTEGER) FROM content_meta WHERE key = 'bundled_content_version'`).Scan(&version)
	if version >= bundledContentVersion {
		return nil
	}
	seedFile, err := os.CreateTemp(appDataDir, "vaultlingo-content-*.db")
	if err != nil {
		return err
	}
	seedPath := seedFile.Name()
	defer os.Remove(seedPath)
	if _, err = seedFile.Write(embeddedVocabDB); err != nil {
		seedFile.Close()
		return err
	}
	if err = seedFile.Close(); err != nil {
		return err
	}
	if _, err = db.Exec(`ATTACH DATABASE ? AS bundled`, seedPath); err != nil {
		return err
	}
	defer db.Exec(`DETACH DATABASE bundled`)
	// Do not overwrite a user's own words or study state. Content tables are
	// additive and use their natural unique keys from the bundled database.
	queries := []string{
		`INSERT OR IGNORE INTO words SELECT * FROM bundled.words`,
		`INSERT OR IGNORE INTO idioms SELECT * FROM bundled.idioms`,
		`INSERT OR IGNORE INTO dictations SELECT * FROM bundled.dictations`,
		`INSERT OR REPLACE INTO listening_topics SELECT * FROM bundled.listening_topics`,
		`INSERT OR IGNORE INTO grammar_drills SELECT * FROM bundled.grammar_drills`,
		`INSERT OR IGNORE INTO writing_prompts SELECT * FROM bundled.writing_prompts`,
	}
	for _, query := range queries {
		if _, err = db.Exec(query); err != nil {
			return err
		}
	}
	// quizzes in old databases did not have a unique constraint.
	_, _ = db.Exec(`DELETE FROM quizzes WHERE id NOT IN (SELECT MIN(id) FROM quizzes GROUP BY question)`)
	_, _ = db.Exec(`CREATE UNIQUE INDEX IF NOT EXISTS idx_quizzes_question_unique ON quizzes(question)`)
	if _, err = db.Exec(`INSERT OR IGNORE INTO quizzes SELECT * FROM bundled.quizzes`); err != nil {
		return err
	}
	_, err = db.Exec(`INSERT INTO content_meta(key, value) VALUES('bundled_content_version', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value`, bundledContentVersion)
	return err
}
