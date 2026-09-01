package backend

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// SynthesizePiperTTS generates audio using offline Piper TTS binary
func SynthesizePiperTTS(text, piperPath, modelPath string, speed float64) (string, error) {
	if piperPath == "" {
		// Look up in PATH
		if p, err := exec.LookPath("piper"); err == nil {
			piperPath = p
		} else {
			return "", fmt.Errorf("piper binary not found. Please specify piper path in Settings or install piper")
		}
	}

	if modelPath == "" {
		return "", fmt.Errorf("piper onnx model path is not configured. Please download an ONNX voice model and set its path in Settings")
	}

	if _, err := os.Stat(modelPath); os.IsNotExist(err) {
		return "", fmt.Errorf("piper model file not found at: %s", modelPath)
	}

	cacheKey := getCacheKey("piper-"+filepath.Base(modelPath), text, speed)
	cacheFile := filepath.Join(GetAudioCacheDir(), cacheKey+".wav")

	audioCacheMutex.Lock()
	if info, err := os.Stat(cacheFile); err == nil && info.Size() > 0 {
		audioCacheMutex.Unlock()
		return cacheFile, nil
	}
	audioCacheMutex.Unlock()

	tempFile := cacheFile + ".tmp.wav"
	defer os.Remove(tempFile)

	args := []string{
		"--model", modelPath,
		"--output_file", tempFile,
	}

	if speed > 0 && speed != 1.0 {
		// Piper uses length_scale (inverse of speed, e.g. speed=2.0 -> length_scale=0.5)
		lengthScale := 1.0 / speed
		args = append(args, "--length_scale", fmt.Sprintf("%.2f", lengthScale))
	}

	cmd := exec.Command(piperPath, args...)
	cmd.Stdin = strings.NewReader(text)

	var errBuf strings.Builder
	cmd.Stderr = &errBuf

	if err := cmd.Run(); err != nil {
		return "", fmt.Errorf("piper execution failed: %v (%s)", err, errBuf.String())
	}

	audioCacheMutex.Lock()
	defer audioCacheMutex.Unlock()

	if err := os.Rename(tempFile, cacheFile); err != nil {
		return "", fmt.Errorf("failed to save piper audio: %w", err)
	}

	return cacheFile, nil
}
