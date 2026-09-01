package backend

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// resolvePiperCommand finds the right execution command for Piper TTS
func resolvePiperCommand(customPath string) (string, []string, error) {
	if customPath != "" {
		if _, err := os.Stat(customPath); err == nil {
			return customPath, nil, nil
		}
		if p, err := exec.LookPath(customPath); err == nil {
			return p, nil, nil
		}
	}

	// 1. Try binary names in PATH
	for _, binName := range []string{"piper-tts", "piper_tts"} {
		if p, err := exec.LookPath(binName); err == nil {
			return p, nil, nil
		}
	}

	// 2. Check if python3 -m piper is available
	if py, err := exec.LookPath("python3"); err == nil {
		checkCmd := exec.Command(py, "-m", "piper", "--help")
		if err := checkCmd.Run(); err == nil {
			return py, []string{"-m", "piper"}, nil
		}
	}

	// 3. Check /usr/bin/piper only if it supports --model (to avoid libratbag conflict)
	if p, err := exec.LookPath("piper"); err == nil {
		out, _ := exec.Command(p, "--help").CombinedOutput()
		if strings.Contains(string(out), "--model") || strings.Contains(string(out), "-m") {
			return p, nil, nil
		}
	}

	return "", nil, fmt.Errorf("piper TTS engine not found. Install via 'pip install piper-tts' or 'yay -S piper-tts-bin'")
}

// resolvePiperModel finds the ONNX model file
func resolvePiperModel(customModelPath string) (string, error) {
	if customModelPath != "" {
		expanded := expandTilde(customModelPath)
		if _, err := os.Stat(expanded); err == nil {
			return expanded, nil
		}
	}

	home, _ := os.UserHomeDir()
	candidateDirs := []string{
		filepath.Join(home, ".local", "share", "VaultLingo", "models"),
		filepath.Join(home, ".local", "share", "piper"),
		filepath.Join(home, ".local", "share", "piper-voices"),
	}

	// First check known default model filenames
	for _, dir := range candidateDirs {
		defaultModel := filepath.Join(dir, "en_US-lessac-medium.onnx")
		if _, err := os.Stat(defaultModel); err == nil {
			return defaultModel, nil
		}
	}

	// Then check any .onnx file in candidate directories
	for _, dir := range candidateDirs {
		matches, _ := filepath.Glob(filepath.Join(dir, "*.onnx"))
		if len(matches) > 0 {
			return matches[0], nil
		}
	}

	return "", fmt.Errorf("no Piper ONNX model found in ~/.local/share/VaultLingo/models/. Please place an ONNX voice model there")
}

func expandTilde(path string) string {
	if strings.HasPrefix(path, "~/") {
		home, _ := os.UserHomeDir()
		return filepath.Join(home, path[2:])
	}
	return path
}

// SynthesizePiperTTS generates audio using offline Piper TTS
func SynthesizePiperTTS(text, piperPath, modelPath string, speed float64) (string, error) {
	binPath, prefixArgs, err := resolvePiperCommand(piperPath)
	if err != nil {
		return "", err
	}

	resolvedModel, err := resolvePiperModel(modelPath)
	if err != nil {
		return "", err
	}

	cacheKey := getCacheKey("piper-"+filepath.Base(resolvedModel), text, speed)
	cacheFile := filepath.Join(GetAudioCacheDir(), cacheKey+".wav")

	audioCacheMutex.Lock()
	if info, err := os.Stat(cacheFile); err == nil && info.Size() > 0 {
		audioCacheMutex.Unlock()
		return cacheFile, nil
	}
	audioCacheMutex.Unlock()

	tempFile := cacheFile + ".tmp.wav"
	defer os.Remove(tempFile)

	args := append([]string{}, prefixArgs...)
	args = append(args, "--model", resolvedModel, "--output_file", tempFile)

	if speed > 0 && speed != 1.0 {
		lengthScale := 1.0 / speed
		args = append(args, "--length_scale", fmt.Sprintf("%.2f", lengthScale))
	}

	cmd := exec.Command(binPath, args...)
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
