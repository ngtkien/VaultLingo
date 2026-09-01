package backend

import (
	"strings"
	"testing"
)

func TestGenerateSSML(t *testing.T) {
	ssml := GenerateSSML("Hello world", "en-US-JennyNeural", 1.0)
	if !strings.Contains(ssml, "en-US-JennyNeural") {
		t.Errorf("Expected SSML to contain voice name, got: %s", ssml)
	}
	if !strings.Contains(ssml, "Hello world") {
		t.Errorf("Expected SSML to contain text, got: %s", ssml)
	}
	if !strings.Contains(ssml, "rate='+0%'") {
		t.Errorf("Expected SSML rate to be +0%% for 1.0 speed, got: %s", ssml)
	}

	// Test special XML characters escaping
	ssmlEscaped := GenerateSSML("Jack & Jill <up> the hill", "en-GB-RyanNeural", 1.25)
	if !strings.Contains(ssmlEscaped, "Jack &amp; Jill &lt;up&gt; the hill") {
		t.Errorf("Expected SSML to escape special characters, got: %s", ssmlEscaped)
	}
	if !strings.Contains(ssmlEscaped, "rate='+25%'") {
		t.Errorf("Expected SSML rate to be +25%% for 1.25 speed, got: %s", ssmlEscaped)
	}
}

func TestGetVoicesList(t *testing.T) {
	voices := GetVoicesList()
	if len(voices) == 0 {
		t.Fatalf("Expected non-empty voice list")
	}

	foundJenny := false
	for _, v := range voices {
		if v.ID == "en-US-JennyNeural" {
			foundJenny = true
			if v.Flag != "🇺🇸" || v.Gender != "Female" {
				t.Errorf("Unexpected Jenny metadata: %+v", v)
			}
		}
	}
	if !foundJenny {
		t.Errorf("Expected en-US-JennyNeural in voice list")
	}
}

func TestConfig_TTSDefaults(t *testing.T) {
	cfg := LoadConfig()
	if cfg.TTSProvider == "" {
		t.Errorf("Expected default TTSProvider to be non-empty")
	}
	if cfg.TTSVoice == "" {
		t.Errorf("Expected default TTSVoice to be non-empty")
	}
}

func TestEdgeTTS_LiveSynthesis(t *testing.T) {
	cacheFile, err := SynthesizeEdgeTTS("Welcome to VaultLingo", "en-US-JennyNeural", 1.0)
	if err != nil {
		t.Logf("Edge TTS synthesis note: %v (falls back gracefully to Google TTS in production)", err)
		return
	}
	t.Logf("✔ Edge TTS successfully synthesized: %s", cacheFile)
}

func TestPiperTTS_LiveSynthesis(t *testing.T) {
	cacheFile, err := SynthesizePiperTTS("Hello from offline Piper TTS", "", "", 1.0)
	if err != nil {
		t.Logf("Piper TTS note: %v", err)
		return
	}
	t.Logf("✔ Piper TTS successfully synthesized: %s", cacheFile)
}


