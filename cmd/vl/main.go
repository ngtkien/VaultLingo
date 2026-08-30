package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strings"
	"time"

	"VaultLingo/backend"
)

// ANSI color escape codes (Zero-bloat pure terminal formatting)
const (
	colorReset  = "\033[0m"
	colorBold   = "\033[1m"
	colorDim    = "\033[2m"
	colorCyan   = "\033[36m"
	colorGreen  = "\033[32m"
	colorYellow = "\033[33m"
	colorBlue   = "\033[34m"
	colorPurple = "\033[35m"
	colorWhite  = "\033[37m"
)

type BilingualExample struct {
	En string `json:"en"`
	Vi string `json:"vi"`
}

type WordFamilyMember struct {
	Pos  string `json:"pos"`
	Word string `json:"word"`
}

func main() {
	searchFlag := flag.String("s", "", "Search words matching prefix in SQLite database")
	searchLong := flag.String("search", "", "Search words matching prefix in SQLite database")
	jsonFlag := flag.Bool("json", false, "Output result as raw JSON")
	obsidianFlag := flag.Bool("o", false, "Sync word card to Obsidian Vault")
	obsidianLong := flag.Bool("obsidian", false, "Sync word card to Obsidian Vault")
	flag.Parse()

	args := flag.Args()

	searchQuery := *searchFlag
	if searchQuery == "" {
		searchQuery = *searchLong
	}

	saveToObsidian := *obsidianFlag || *obsidianLong
	outputJSON := *jsonFlag

	var cleanedWords []string
	for _, arg := range args {
		if arg == "--json" {
			outputJSON = true
		} else if arg == "-o" || arg == "--obsidian" {
			saveToObsidian = true
		} else if strings.HasPrefix(arg, "-") {
			// skip unknown flags
		} else {
			cleanedWords = append(cleanedWords, arg)
		}
	}

	// 1. Initialize SQLite Database (auto-unpacks embedded DB if needed)
	db, err := backend.InitDB()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error initializing VaultLingo database: %v\n", err)
		os.Exit(1)
	}
	defer db.Close()

	// 2. Handle Prefix Search
	if searchQuery != "" {
		handleSearch(searchQuery, outputJSON)
		return
	}

	if len(cleanedWords) == 0 {
		printHelp()
		return
	}

	wordQuery := strings.TrimSpace(strings.Join(cleanedWords, " "))
	if wordQuery == "" {
		printHelp()
		return
	}

	// 3. Handle Dictionary Word Lookup
	handleLookup(wordQuery, outputJSON, saveToObsidian)
}

func handleSearch(query string, isJSON bool) {
	words, err := backend.SearchWordsInDB(query, 12)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Search error: %v\n", err)
		os.Exit(1)
	}

	if isJSON {
		out, _ := json.MarshalIndent(words, "", "  ")
		fmt.Println(string(out))
		return
	}

	if len(words) == 0 {
		fmt.Printf("No matching words found for '%s'.\n", query)
		return
	}

	fmt.Printf("%sVaultLingo Search Suggestions for '%s':%s\n", colorBold, query, colorReset)
	for _, w := range words {
		posStr := ""
		if w.POS != "" {
			posStr = fmt.Sprintf("[%s]", w.POS)
		}
		levelStr := ""
		if w.Level != "" {
			levelStr = fmt.Sprintf("(%s)", w.Level)
		}
		fmt.Printf("  • %s%-16s%s %s%-8s%s %s%-10s%s %s%s%s\n",
			colorBold+colorCyan, w.Word, colorReset,
			colorGreen, posStr, colorReset,
			colorDim, levelStr, colorReset,
			colorWhite, w.DefinitionVi, colorReset,
		)
	}
}

func handleLookup(query string, isJSON bool, saveObsidian bool) {
	startTime := time.Now()

	// 1. Check local SQLite DB
	w, err := backend.LookupWordInDB(query)
	isFromAI := false

	if err != nil || w == nil || w.DefinitionEn == "" {
		// Word MISS in SQLite -> Try synthesising via AI
		w, err = synthesizeWordAI(query)
		if err != nil || w == nil {
			fmt.Printf("Word '%s' not found in local database and AI synthesis is unavailable.\n", query)
			fmt.Printf("Tip: Check spelling or configure AI provider in ~/.config/VaultLingo/config.json\n")
			return
		}
		isFromAI = true
		_ = backend.SaveWordToDB(*w)
	}

	elapsedMs := time.Since(startTime).Milliseconds()

	// Handle JSON Output
	if isJSON {
		out, _ := json.MarshalIndent(w, "", "  ")
		fmt.Println(string(out))
		return
	}

	// Handle Obsidian Sync
	if saveObsidian {
		cfg := backend.LoadConfig()
		if cfg.ObsidianVaultPath != "" {
			_, _ = backend.SaveWordToObsidian(*w, cfg.ObsidianVaultPath)
			fmt.Printf("%s✔ Synced to Obsidian Vault: %s%s\n\n", colorGreen, cfg.ObsidianVaultPath, colorReset)
		} else {
			fmt.Printf("%s⚠ Obsidian Vault path is not set in config. Use GUI Settings to configure.%s\n\n", colorYellow, colorReset)
		}
	}

	// 2. Render 6-Block Terminal Output
	renderWordTerminal(w, elapsedMs, isFromAI)
}

func renderWordTerminal(w *backend.Word, elapsedMs int64, isFromAI bool) {
	badgeSource := fmt.Sprintf("%s⚡ %dms (SQLite HIT)%s", colorGreen, elapsedMs, colorReset)
	if isFromAI {
		badgeSource = fmt.Sprintf("%s✨ %dms (AI Generated & Saved)%s", colorPurple, elapsedMs, colorReset)
	}

	// Header line
	fmt.Printf("\n%s%s%s  %s[%s]%s  %s[%s]%s  •  %s%s%s  (%s)\n\n",
		colorBold+colorCyan, strings.ToUpper(w.Word), colorReset,
		colorGreen, w.POS, colorReset,
		colorYellow, w.Level, colorReset,
		colorWhite, w.Phonetic, colorReset,
		badgeSource,
	)

	// Block 1: English Definition & Vietnamese Meaning
	if w.DefinitionEn != "" {
		fmt.Printf("%s[ENGLISH DEFINITION]%s\n%s\n\n", colorBold+colorBlue, colorReset, w.DefinitionEn)
	}
	if w.DefinitionVi != "" {
		fmt.Printf("%s[VIETNAMESE MEANING]%s\n%s\n\n", colorBold+colorGreen, colorReset, w.DefinitionVi)
	}

	// Block 2: Word Family
	if w.WordFamilyJSON != "" && w.WordFamilyJSON != "[]" {
		var members []WordFamilyMember
		if err := json.Unmarshal([]byte(w.WordFamilyJSON), &members); err == nil && len(members) > 0 {
			fmt.Printf("%s[WORD FAMILY]%s\n", colorBold+colorPurple, colorReset)
			for _, m := range members {
				fmt.Printf("  • %s%-10s%s: %s%s%s\n", colorDim, m.Pos, colorReset, colorBold, m.Word, colorReset)
			}
			fmt.Println()
		}
	}

	// Block 3: Etymology
	if w.Etymology != "" {
		fmt.Printf("%s[ETYMOLOGY & ROOT]%s\n%s\n\n", colorBold+colorYellow, colorReset, w.Etymology)
	}

	// Block 4: Examples
	var examples []BilingualExample
	if w.ExamplesJSON != "" && w.ExamplesJSON != "[]" {
		_ = json.Unmarshal([]byte(w.ExamplesJSON), &examples)
	}
	if len(examples) == 0 && w.ExampleEn != "" {
		examples = append(examples, BilingualExample{En: w.ExampleEn, Vi: w.ExampleVi})
	}

	if len(examples) > 0 {
		fmt.Printf("%s[REAL-WORLD EXAMPLES]%s\n", colorBold+colorWhite, colorReset)
		for i, ex := range examples {
			fmt.Printf("  %d. \"%s%s%s\"\n", i+1, colorBold, ex.En, colorReset)
			if ex.Vi != "" {
				fmt.Printf("     %s➔ %s%s\n", colorDim, ex.Vi, colorReset)
			}
		}
		fmt.Println()
	}

	// Block 5: Synonyms, Antonyms, Collocations
	var syns, ants, colls []string
	if w.SynonymsJSON != "" && w.SynonymsJSON != "[]" {
		_ = json.Unmarshal([]byte(w.SynonymsJSON), &syns)
	}
	if w.AntonymsJSON != "" && w.AntonymsJSON != "[]" {
		_ = json.Unmarshal([]byte(w.AntonymsJSON), &ants)
	}
	if w.CollocationsJSON != "" && w.CollocationsJSON != "[]" {
		_ = json.Unmarshal([]byte(w.CollocationsJSON), &colls)
	}

	if len(syns) > 0 || len(ants) > 0 {
		fmt.Printf("%s[SYNONYMS & ANTONYMS]%s\n", colorBold+colorCyan, colorReset)
		if len(syns) > 0 {
			fmt.Printf("  • %sSynonyms:%s %s\n", colorDim, colorReset, strings.Join(syns, ", "))
		}
		if len(ants) > 0 {
			fmt.Printf("  • %sAntonyms:%s %s\n", colorDim, colorReset, strings.Join(ants, ", "))
		}
		fmt.Println()
	}

	if len(colls) > 0 {
		fmt.Printf("%s[HIGH-YIELD COLLOCATIONS]%s\n", colorBold+colorYellow, colorReset)
		for _, c := range colls {
			fmt.Printf("  ⚡ %s\n", c)
		}
		fmt.Println()
	}

	// Block 6: Memory Hook & Nuance Tips
	if w.MnemonicHook != "" || w.NuanceTips != "" {
		fmt.Printf("%s[MEMORY HOOK & IELTS NUANCE]%s\n", colorBold+colorPurple, colorReset)
		if w.MnemonicHook != "" {
			fmt.Printf("  💡 %sMemory Hook:%s %s\n", colorBold, colorReset, w.MnemonicHook)
		}
		if w.NuanceTips != "" {
			fmt.Printf("  🎯 %sIELTS Tip:%s   %s\n", colorBold, colorReset, w.NuanceTips)
		}
		fmt.Println()
	}
}

func synthesizeWordAI(word string) (*backend.Word, error) {
	cfg := backend.LoadConfig()

	prompt := fmt.Sprintf(`You are an Oxford lexicographer and English-Vietnamese linguist.
Create an authentic Oxford dictionary entry for the English word: "%s".

Return ONLY raw valid JSON (no markdown fences, no backticks) matching this schema:
{
  "word": "%s",
  "pos": "Noun | Verb | Adjective | Adverb",
  "phonetic": "/IPA/",
  "definition_en": "Clear English definition",
  "definition_vi": "Nghĩa tiếng Việt chuẩn mực, tự nhiên",
  "word_family": [
    { "pos": "Noun", "word": "..." },
    { "pos": "Verb", "word": "..." }
  ],
  "etymology": "Latin/Greek root origin",
  "examples": [
    { "en": "Example sentence 1.", "vi": "Dịch ví dụ 1." },
    { "en": "Example sentence 2.", "vi": "Dịch ví dụ 2." }
  ],
  "synonyms": ["syn1", "syn2", "syn3"],
  "antonyms": ["ant1", "ant2"],
  "collocations": ["collocation 1", "collocation 2"],
  "mnemonic_hook": "Clever memory hook in Vietnamese",
  "nuance_tips": "IELTS usage tip",
  "level": "B2",
  "topic": "vocabulary"
}`, word, word)

	systemPrompt := "You are a distinguished Oxford lexicographer. Return ONLY valid JSON."
	rawResp, err := backend.CallAI(systemPrompt, prompt, cfg)
	if err != nil {
		return nil, err
	}

	cleanJson := strings.TrimSpace(rawResp)
	re := regexp.MustCompile("(?s)```(?:json)?(.*?)```")
	matches := re.FindStringSubmatch(cleanJson)
	if len(matches) > 1 {
		cleanJson = strings.TrimSpace(matches[1])
	}

	firstBrace := strings.Index(cleanJson, "{")
	lastBrace := strings.LastIndex(cleanJson, "}")
	if firstBrace != -1 && lastBrace != -1 && lastBrace > firstBrace {
		cleanJson = cleanJson[firstBrace : lastBrace+1]
	}

	var data struct {
		Word         string               `json:"word"`
		POS          string               `json:"pos"`
		Phonetic     string               `json:"phonetic"`
		DefinitionEn string               `json:"definition_en"`
		DefinitionVi string               `json:"definition_vi"`
		WordFamily   []WordFamilyMember   `json:"word_family"`
		Etymology    string               `json:"etymology"`
		Examples     []BilingualExample   `json:"examples"`
		Synonyms     []string             `json:"synonyms"`
		Antonyms     []string             `json:"antonyms"`
		Collocations []string             `json:"collocations"`
		MnemonicHook string               `json:"mnemonic_hook"`
		NuanceTips   string               `json:"nuance_tips"`
		Level        string               `json:"level"`
		Topic        string               `json:"topic"`
	}

	if err := json.Unmarshal([]byte(cleanJson), &data); err != nil {
		return nil, err
	}

	synsBytes, _ := json.Marshal(data.Synonyms)
	antsBytes, _ := json.Marshal(data.Antonyms)
	collsBytes, _ := json.Marshal(data.Collocations)
	wfBytes, _ := json.Marshal(data.WordFamily)
	exBytes, _ := json.Marshal(data.Examples)

	exEn := ""
	exVi := ""
	if len(data.Examples) > 0 {
		exEn = data.Examples[0].En
		exVi = data.Examples[0].Vi
	}

	return &backend.Word{
		Word:             data.Word,
		POS:              data.POS,
		Phonetic:         data.Phonetic,
		DefinitionEn:     data.DefinitionEn,
		DefinitionVi:     data.DefinitionVi,
		ExampleEn:        exEn,
		ExampleVi:        exVi,
		Level:            data.Level,
		Topic:            data.Topic,
		SynonymsJSON:     string(synsBytes),
		AntonymsJSON:     string(antsBytes),
		CollocationsJSON: string(collsBytes),
		WordFamilyJSON:   string(wfBytes),
		Etymology:        data.Etymology,
		MnemonicHook:     data.MnemonicHook,
		NuanceTips:       data.NuanceTips,
		ExamplesJSON:     string(exBytes),
	}, nil
}

func printHelp() {
	fmt.Println(`VaultLingo CLI (vl) - Instant 0ms English Dictionary & Lexicon Engine

USAGE:
  vl <word>                Lookup word in local SQLite database (Instant 0ms)
  vl -s <query>            Autocomplete & search word suggestions
  vl <word> --json         Output full 6-block dictionary data as JSON
  vl <word> -o             Lookup and automatically sync word card to Obsidian Vault
  vl -h, --help            Show this help message

EXAMPLES:
  vl compare
  vl resilience
  vl -s comp
  vl serendipity --json
  vl bandwidth -o`)
}
