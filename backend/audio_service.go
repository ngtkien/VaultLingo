package backend

import (
	"fmt"
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

func PlayTTS(text string, speed float64) error {
	if text == "" {
		return nil
	}
	StopAudio()

	if speed <= 0 {
		speed = 1.0
	}

	ttsUrl := fmt.Sprintf("https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=%s", url.QueryEscape(text))
	return PlayAudioUrl(ttsUrl, speed)
}

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
	default:
		// Linux: try mpv → ffplay → paplay (in priority order)
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
