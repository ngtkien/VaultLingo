package backend

import (
	"bytes"
	"crypto/md5"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

const (
	trustedClientToken = "6A5AA1D4E5B74C97921667A57184A1E0"
	secGecToken        = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"
	edgeWSSBaseURL     = "wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1"
	edgeOrigin         = "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold"
	edgeUserAgent      = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
	defaultEdgeVoice    = "en-US-JennyNeural"
	windowsEpochDiff   = 11644473600 // Difference in seconds between Unix epoch (1970) and Windows epoch (1601)
)

type VoiceOption struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Locale      string `json:"locale"`
	Country     string `json:"country"`
	Flag        string `json:"flag"`
	Gender      string `json:"gender"`
	Description string `json:"description"`
}

var AvailableVoices = []VoiceOption{
	{
		ID:          "en-US-JennyNeural",
		Name:        "Jenny (US)",
		Locale:      "en-US",
		Country:     "United States",
		Flag:        "🇺🇸",
		Gender:      "Female",
		Description: "Warm, natural & conversational American female voice (Recommended)",
	},
	{
		ID:          "en-US-GuyNeural",
		Name:        "Guy (US)",
		Locale:      "en-US",
		Country:     "United States",
		Flag:        "🇺🇸",
		Gender:      "Male",
		Description: "Deep, clear & professional American male voice",
	},
	{
		ID:          "en-US-AriaNeural",
		Name:        "Aria (US)",
		Locale:      "en-US",
		Country:     "United States",
		Flag:        "🇺🇸",
		Gender:      "Female",
		Description: "Expressive & articulate American female voice",
	},
	{
		ID:          "en-US-ChristopherNeural",
		Name:        "Christopher (US)",
		Locale:      "en-US",
		Country:     "United States",
		Flag:        "🇺🇸",
		Gender:      "Male",
		Description: "Calm & authoritative American male voice",
	},
	{
		ID:          "en-GB-SoniaNeural",
		Name:        "Sonia (UK)",
		Locale:      "en-GB",
		Country:     "United Kingdom",
		Flag:        "🇬🇧",
		Gender:      "Female",
		Description: "Standard British Received Pronunciation (RP) female voice",
	},
	{
		ID:          "en-GB-RyanNeural",
		Name:        "Ryan (UK)",
		Locale:      "en-GB",
		Country:     "United Kingdom",
		Flag:        "🇬🇧",
		Gender:      "Male",
		Description: "Crisp & polite British RP male voice",
	},
	{
		ID:          "en-AU-NatashaNeural",
		Name:        "Natasha (AU)",
		Locale:      "en-AU",
		Country:     "Australia",
		Flag:        "🇦🇺",
		Gender:      "Female",
		Description: "Friendly & authentic Australian English female voice",
	},
	{
		ID:          "en-AU-WilliamNeural",
		Name:        "William (AU)",
		Locale:      "en-AU",
		Country:     "Australia",
		Flag:        "🇦🇺",
		Gender:      "Male",
		Description: "Natural Australian English male voice",
	},
}

var audioCacheMutex sync.Mutex

func GetAudioCacheDir() string {
	home, _ := os.UserHomeDir()
	cacheDir := filepath.Join(home, ".cache", "VaultLingo", "audio")
	_ = os.MkdirAll(cacheDir, 0755)
	return cacheDir
}

func getCacheKey(voice, text string, speed float64) string {
	h := md5.New()
	h.Write([]byte(fmt.Sprintf("%s|%.2f|%s", voice, speed, text)))
	return hex.EncodeToString(h.Sum(nil))
}

func escapeSSML(s string) string {
	s = strings.ReplaceAll(s, "&", "&amp;")
	s = strings.ReplaceAll(s, "<", "&lt;")
	s = strings.ReplaceAll(s, ">", "&gt;")
	s = strings.ReplaceAll(s, "\"", "&quot;")
	s = strings.ReplaceAll(s, "'", "&apos;")
	return s
}

// GenerateSecMSGec computes the mandatory anti-abuse Sec-MS-GEC token
func GenerateSecMSGec() string {
	nowUnix := time.Now().Unix()
	ticks := (nowUnix + windowsEpochDiff) * 10000000
	ticks -= ticks % (300 * 10000000) // 5-minute window in 100ns units

	strToHash := fmt.Sprintf("%d%s", ticks, secGecToken)
	sum := sha256.Sum256([]byte(strToHash))
	return strings.ToUpper(hex.EncodeToString(sum[:]))
}

// GenerateSSML builds the XML payload for Edge TTS
func GenerateSSML(text, voice string, speed float64) string {
	if voice == "" {
		voice = defaultEdgeVoice
	}
	ratePercent := int((speed - 1.0) * 100)
	rateStr := "+0%"
	if ratePercent >= 0 {
		rateStr = fmt.Sprintf("+%d%%", ratePercent)
	} else {
		rateStr = fmt.Sprintf("%d%%", ratePercent)
	}

	escapedText := escapeSSML(text)

	return fmt.Sprintf(
		`<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>`+
			`<voice name='%s'>`+
			`<prosody rate='%s' pitch='+0Hz'>%s</prosody>`+
			`</voice>`+
			`</speak>`,
		voice, rateStr, escapedText,
	)
}

// SynthesizeEdgeTTS requests audio from Microsoft Edge Neural TTS and returns the path to cached MP3
func SynthesizeEdgeTTS(text, voice string, speed float64) (string, error) {
	if voice == "" {
		voice = defaultEdgeVoice
	}
	if speed <= 0 {
		speed = 1.0
	}

	cacheKey := getCacheKey(voice, text, speed)
	cacheFile := filepath.Join(GetAudioCacheDir(), cacheKey+".mp3")

	audioCacheMutex.Lock()
	if info, err := os.Stat(cacheFile); err == nil && info.Size() > 0 {
		audioCacheMutex.Unlock()
		return cacheFile, nil
	}
	audioCacheMutex.Unlock()

	connID := strings.ReplaceAll(uuid.New().String(), "-", "")
	secGec := GenerateSecMSGec()
	wsURL := fmt.Sprintf("%s?TrustedClientToken=%s&Sec-MS-GEC=%s&Sec-MS-GEC-Version=1-130.0.2849.68&ConnectionId=%s",
		edgeWSSBaseURL, trustedClientToken, secGec, url.QueryEscape(connID))

	dialer := websocket.Dialer{
		HandshakeTimeout: 10 * time.Second,
	}

	headers := http.Header{}
	headers.Set("Origin", edgeOrigin)
	headers.Set("User-Agent", edgeUserAgent)
	headers.Set("Pragma", "no-cache")
	headers.Set("Cache-Control", "no-cache")

	ws, _, err := dialer.Dial(wsURL, headers)
	if err != nil {
		return "", fmt.Errorf("failed to connect to Edge TTS websocket: %w", err)
	}
	defer ws.Close()

	// 1. Send speech.config message
	timestamp := time.Now().UTC().Format("Mon Jan 02 2006 15:04:05 GMT+0000 (Coordinated Universal Time)")
	configMsg := fmt.Sprintf("Content-Type:application/json; charset=utf-8\r\nPath:speech.config\r\n\r\n"+
		`{"context":{"synthesis":{"audio":{"metadataoptions":{"sentenceBoundaryEnabled":"false","wordBoundaryEnabled":"false"},"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}`)
	if err := ws.WriteMessage(websocket.TextMessage, []byte(configMsg)); err != nil {
		return "", fmt.Errorf("failed to send speech.config: %w", err)
	}

	// 2. Send SSML request
	reqID := strings.ReplaceAll(uuid.New().String(), "-", "")
	ssml := GenerateSSML(text, voice, speed)
	ssmlMsg := fmt.Sprintf("X-RequestId:%s\r\nContent-Type:application/ssml+xml\r\nX-Timestamp:%s\r\nPath:ssml\r\n\r\n%s", reqID, timestamp, ssml)
	if err := ws.WriteMessage(websocket.TextMessage, []byte(ssmlMsg)); err != nil {
		return "", fmt.Errorf("failed to send ssml request: %w", err)
	}

	// 3. Receive audio stream
	var audioBuffer bytes.Buffer
	turnEndReceived := false

	ws.SetReadDeadline(time.Now().Add(15 * time.Second))

	for {
		msgType, data, err := ws.ReadMessage()
		if err != nil {
			break
		}

		if msgType == websocket.TextMessage {
			msgStr := string(data)
			if strings.Contains(msgStr, "Path:turn.end") {
				turnEndReceived = true
				break
			}
		} else if msgType == websocket.BinaryMessage {
			// Binary message format: [2 bytes header len] + [header string: Path:audio\r\n...] + [raw mp3 binary audio]
			if len(data) > 2 {
				headerLen := int(data[0])<<8 | int(data[1])
				if len(data) > 2+headerLen {
					payload := data[2+headerLen:]
					audioBuffer.Write(payload)
				}
			}
		}
	}

	if audioBuffer.Len() == 0 && !turnEndReceived {
		return "", fmt.Errorf("edge tts returned empty audio data")
	}

	// Write to cache file atomically
	audioCacheMutex.Lock()
	defer audioCacheMutex.Unlock()

	tempFile := cacheFile + ".tmp"
	if err := os.WriteFile(tempFile, audioBuffer.Bytes(), 0644); err != nil {
		return "", fmt.Errorf("failed to write audio cache: %w", err)
	}
	_ = os.Rename(tempFile, cacheFile)

	return cacheFile, nil
}
