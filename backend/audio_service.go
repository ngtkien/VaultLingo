package backend

import (
	"fmt"
	"log"
	"net/url"
	"os/exec"
	"runtime"
	"sync"
)

var (
	currentCmd *exec.Cmd
	audioMutex sync.Mutex
)

func StopAudio() {
	audioMutex.Lock()
	defer audioMutex.Unlock()

	if currentCmd != nil && currentCmd.Process != nil {
		_ = currentCmd.Process.Kill()
		currentCmd = nil
	}
}

// GetVoicesList returns available high-quality neural voices
func GetVoicesList() []VoiceOption {
	return AvailableVoices
}

// PlayTTS plays speech based on user configuration (Edge TTS -> Piper -> Google Fallback)
func PlayTTS(text string, speed float64) error {
	if text == "" {
		return nil
	}
	StopAudio()

	if speed <= 0 {
		speed = 1.0
	}

	cfg := LoadConfig()
	provider := cfg.TTSProvider
	if provider == "" {
		provider = "edge"
	}

	switch provider {
	case "piper":
		filePath, err := SynthesizePiperTTS(text, cfg.PiperPath, cfg.PiperModelPath, speed)
		if err == nil {
			return PlayAudioFile(filePath, 1.0) // Speed already baked into Piper synthesis
		}
		log.Printf("⚠️ Piper TTS failed (%v), falling back to Edge TTS", err)
		fallthrough

	case "edge":
		voice := cfg.TTSVoice
		if voice == "" {
			voice = defaultEdgeVoice
		}
		filePath, err := SynthesizeEdgeTTS(text, voice, speed)
		if err == nil {
			return PlayAudioFile(filePath, 1.0) // Speed already baked into Edge SSML prosody rate
		}
		log.Printf("⚠️ Edge TTS failed (%v), falling back to Google Translate TTS", err)
		fallthrough

	default: // "google" or fallback
		return playGoogleTTS(text, speed)
	}
}

func playGoogleTTS(text string, speed float64) error {
	ttsUrl := fmt.Sprintf("https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=%s", url.QueryEscape(text))
	return PlayAudioUrl(ttsUrl, speed)
}

// PlayAudioFile plays a local audio file (MP3/WAV)
func PlayAudioFile(filePath string, speed float64) error {
	return PlayAudioUrl(filePath, speed)
}

// PlayAudioUrl plays an audio URL or local file path using mpv/ffplay
func PlayAudioUrl(audioUrl string, speed float64) error {
	if audioUrl == "" {
		return nil
	}
	StopAudio()

	if speed <= 0 {
		speed = 1.0
	}

	audioMutex.Lock()
	defer audioMutex.Unlock()

	var cmd *exec.Cmd
	speedStr := fmt.Sprintf("--speed=%.2f", speed)

	switch runtime.GOOS {
	case "darwin":
		if _, err := exec.LookPath("mpv"); err == nil {
			cmd = exec.Command("mpv", "--no-video", "--really-quiet", speedStr, audioUrl)
		} else {
			return fmt.Errorf("audio player not found: please install mpv (brew install mpv)")
		}
	case "windows":
		if _, err := exec.LookPath("mpv.exe"); err == nil {
			cmd = exec.Command("mpv.exe", "--no-video", "--really-quiet", speedStr, audioUrl)
		} else if _, err := exec.LookPath("ffplay.exe"); err == nil {
			cmd = exec.Command("ffplay.exe", "-nodisp", "-autoexit", "-loglevel", "quiet", audioUrl)
		} else {
			return fmt.Errorf("audio player not found: please install mpv or ffmpeg")
		}
	default:
		// Linux: try mpv → ffplay
		if _, err := exec.LookPath("mpv"); err == nil {
			cmd = exec.Command("mpv", "--no-video", "--really-quiet", "--input-terminal=no", "--no-input-default-bindings", speedStr, audioUrl)
		} else if _, err := exec.LookPath("ffplay"); err == nil {
			cmd = exec.Command("ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audioUrl)
		} else {
			return fmt.Errorf("audio player not found: please install mpv (sudo pacman -S mpv / sudo apt install mpv)")
		}
	}

	currentCmd = cmd
	go func() {
		_ = cmd.Run()
		audioMutex.Lock()
		if currentCmd == cmd {
			currentCmd = nil
		}
		audioMutex.Unlock()
	}()

	return nil
}
