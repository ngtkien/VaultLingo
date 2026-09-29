package backend

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

// ---------- Speaking prompt bank ----------

func GetSpeakingPrompts(part int, topic string) ([]SpeakingPrompt, error) {
	query := `SELECT id, part, COALESCE(topic,''), question, COALESCE(cues_json,'[]'), COALESCE(hint_vi,''), COALESCE(sample_ideas_json,'[]') FROM speaking_prompts`
	var conditions []string
	var args []interface{}
	if part > 0 {
		conditions = append(conditions, "part = ?")
		args = append(args, part)
	}
	if topic != "" && topic != "all" {
		conditions = append(conditions, "topic = ?")
		args = append(args, topic)
	}
	if len(conditions) > 0 {
		query += " WHERE " + strings.Join(conditions, " AND ")
	}
	query += " ORDER BY RANDOM() LIMIT 40"

	rows, err := DB.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []SpeakingPrompt
	for rows.Next() {
		var p SpeakingPrompt
		var cuesJSON, ideasJSON string
		if err := rows.Scan(&p.ID, &p.Part, &p.Topic, &p.Question, &cuesJSON, &p.HintVi, &ideasJSON); err != nil {
			continue
		}
		_ = json.Unmarshal([]byte(cuesJSON), &p.Cues)
		_ = json.Unmarshal([]byte(ideasJSON), &p.SampleIdeas)
		out = append(out, p)
	}
	return out, nil
}

func GetSpeakingTopics() ([]string, error) {
	rows, err := DB.Query(`SELECT DISTINCT topic FROM speaking_prompts WHERE topic != '' ORDER BY topic`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []string
	for rows.Next() {
		var t string
		if rows.Scan(&t) == nil {
			out = append(out, t)
		}
	}
	return out, nil
}

// ---------- Recording (native recorder, independent of webview mic support) ----------

var recordCmd *exec.Cmd
var recordPath string

func recordingsDir() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		homeDir = "."
	}
	dir := filepath.Join(homeDir, ".local", "share", "VaultLingo", "recordings")
	if err := os.MkdirAll(dir, 0755); err != nil {
		return "", err
	}
	return dir, nil
}

func detectRecorder() string {
	if _, err := exec.LookPath("arecord"); err == nil {
		return "arecord"
	}
	if _, err := exec.LookPath("ffmpeg"); err == nil {
		return "ffmpeg"
	}
	return ""
}

func GetRecordingStatus() RecordingStatus {
	rec := detectRecorder()
	status := RecordingStatus{
		Available: rec != "",
		Recorder:  rec,
		Recording: recordCmd != nil,
	}
	if !status.Available {
		status.Message = "No recorder found (install alsa-utils or ffmpeg). Self-check mode only."
	} else {
		status.Message = "Recorder ready: " + rec
	}
	return status
}

func StartSpeakingRecording() (RecordingStatus, error) {
	status := GetRecordingStatus()
	if status.Recording {
		return status, fmt.Errorf("already recording")
	}
	if !status.Available {
		return status, fmt.Errorf("no recorder available")
	}
	dir, err := recordingsDir()
	if err != nil {
		return status, err
	}
	recordPath = filepath.Join(dir, fmt.Sprintf("speaking_%s.wav", time.Now().Format("20060102_150405")))

	if status.Recorder == "arecord" {
		recordCmd = exec.Command("arecord", "-q", "-f", "cd", "-t", "wav", recordPath)
	} else {
		recordCmd = exec.Command("ffmpeg", "-y", "-loglevel", "error", "-f", "pulse", "-i", "default", recordPath)
	}
	if err := recordCmd.Start(); err != nil {
		recordCmd = nil
		return status, fmt.Errorf("failed to start recorder: %w", err)
	}
	status.Recording = true
	return status, nil
}

func StopSpeakingRecording() (RecordingStatus, error) {
	status := GetRecordingStatus()
	if recordCmd == nil {
		return status, fmt.Errorf("not recording")
	}
	// SIGINT lets arecord/ffmpeg finalize the WAV header properly.
	_ = recordCmd.Process.Signal(os.Interrupt)
	done := make(chan error, 1)
	go func() { done <- recordCmd.Wait() }()
	select {
	case <-done:
	case <-time.After(3 * time.Second):
		_ = recordCmd.Process.Kill()
		<-done
	}
	recordCmd = nil
	status.Recording = false
	status.AudioPath = recordPath
	return status, nil
}

// ---------- Attempts & AI evaluation ----------

func SaveSpeakingAttempt(promptID int, audioPath string, duration int, feedback string) error {
	_, err := DB.Exec(`INSERT INTO speaking_attempts(prompt_id, audio_path, duration, feedback, created_at) VALUES(?, ?, ?, ?, ?)`,
		promptID, audioPath, duration, feedback, time.Now().Format("2006-01-02 15:04"))
	return err
}

func GetSpeakingAttempts(promptID int) ([]SpeakingAttempt, error) {
	query := `SELECT id, COALESCE(prompt_id,0), audio_path, duration, feedback, created_at FROM speaking_attempts`
	var args []interface{}
	if promptID > 0 {
		query += " WHERE prompt_id = ?"
		args = append(args, promptID)
	}
	query += " ORDER BY id DESC LIMIT 20"

	rows, err := DB.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []SpeakingAttempt
	for rows.Next() {
		var a SpeakingAttempt
		if err := rows.Scan(&a.ID, &a.PromptID, &a.AudioPath, &a.Duration, &a.Feedback, &a.CreatedAt); err == nil {
			out = append(out, a)
		}
	}
	return out, nil
}

// EvaluateSpeakingAI scores a speaking transcript against IELTS band descriptors.
// Transcript-based so it works with every configured AI provider (all text-mode).
// If the recorded audio file exists and the provider is agentic (agy/opencode),
// the prompt also references the audio path so the agent may listen directly.
func EvaluateSpeakingAI(transcript string, part int, question string, audioPath string, durationSec int, cfg Config) (string, error) {
	if strings.TrimSpace(transcript) == "" {
		return "", fmt.Errorf("empty transcript")
	}
	partDesc := map[int]string{
		1: "Part 1 (short answer, ~30-45 seconds per question)",
		2: "Part 2 (cue card long turn, target 1-2 minutes)",
		3: "Part 3 (discussion, extended answers with reasons and examples)",
	}[part]

	systemInstruction := fmt.Sprintf(`You are an IELTS speaking examiner. Evaluate this %s response.
Return a valid JSON object strictly matching this schema:
{
  "band_estimate": 5.5,
  "fluency": "1-2 sentence feedback on fluency and coherence",
  "lexical": "1-2 sentence feedback on vocabulary range and accuracy",
  "grammar": "1-2 sentence feedback on grammatical range and accuracy",
  "pronunciation_note": "only if audio is available, else empty string",
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["specific fix 1", "specific fix 2"],
  "better_answer": "a natural band 7 sample answer of 3-5 sentences"
}
Estimate band realistically for a learner targeting 6.0. Be honest, not flattering.`, partDesc)

	userContent := fmt.Sprintf(`[Question]: %s
[Duration]: %d seconds
[Transcript of what the user said]:
"%s"`, question, durationSec, transcript)

	// Agentic CLIs (agy/opencode) can read the audio file themselves.
	if audioPath != "" && (cfg.AiProvider == "agy" || cfg.AiProvider == "opencode") {
		userContent += fmt.Sprintf("\n[Audio file]: %s\nIf you can read audio files, transcribe it yourself and evaluate that instead of the provided transcript.", audioPath)
	}

	return CallAI(systemInstruction, userContent, cfg)
}
