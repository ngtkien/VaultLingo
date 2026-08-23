package backend

import (
	"math"
	"regexp"
	"strings"
)

func GetDictationSentence(category string) (Dictation, error) {
	var d Dictation
	var query string
	var args []interface{}

	if category == "" || category == "all" {
		query = `
			SELECT id, level, level_color, category, category_icon, sentence, sentence_vi, hint
			FROM dictations
			ORDER BY RANDOM()
			LIMIT 1
		`
	} else {
		query = `
			SELECT id, level, level_color, category, category_icon, sentence, sentence_vi, hint
			FROM dictations
			WHERE category = ?
			ORDER BY RANDOM()
			LIMIT 1
		`
		args = append(args, category)
	}

	err := DB.QueryRow(query, args...).Scan(
		&d.ID, &d.Level, &d.LevelColor, &d.Category, &d.CategoryIcon,
		&d.Sentence, &d.SentenceVi, &d.Hint,
	)

	if err != nil {
		return Dictation{
			Level:        "B1 Workplace",
			LevelColor:   "#4caf50",
			Category:     "Team Collaboration",
			CategoryIcon: "🤝",
			Sentence:     "Please share your screen so that we can review the design mockup together.",
			SentenceVi:   "Làm ơn hãy chia sẻ màn hình để chúng ta cùng xem qua bản thiết kế.",
			Hint:         "Keywords: share screen, review, design mockup, together.",
		}, nil
	}

	return d, nil
}

func cleanWord(w string) string {
	reg := regexp.MustCompile(`[^a-zA-Z0-9']`)
	return strings.ToLower(reg.ReplaceAllString(w, ""))
}

func CheckDictation(targetSentence string, userInput string) DictationResult {
	targetTokens := strings.Fields(targetSentence)
	userTokens := strings.Fields(userInput)

	var diffs []DiffToken
	correctCount := 0

	// Dynamic programming / LCS based alignment or sequential matching
	tLen := len(targetTokens)
	uLen := len(userTokens)

	// Longest Common Subsequence of cleaned words
	dp := make([][]int, tLen+1)
	for i := range dp {
		dp[i] = make([]int, uLen+1)
	}

	for i := 1; i <= tLen; i++ {
		for j := 1; j <= uLen; j++ {
			if cleanWord(targetTokens[i-1]) == cleanWord(userTokens[j-1]) {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = int(math.Max(float64(dp[i-1][j]), float64(dp[i][j-1])))
			}
		}
	}

	// Backtrack to build diff tokens
	i, j := tLen, uLen
	var reversedDiffs []DiffToken

	for i > 0 || j > 0 {
		if i > 0 && j > 0 && cleanWord(targetTokens[i-1]) == cleanWord(userTokens[j-1]) {
			reversedDiffs = append(reversedDiffs, DiffToken{
				Type:  "correct",
				Word:  userTokens[j-1],
				Match: targetTokens[i-1],
			})
			correctCount++
			i--
			j--
		} else if j > 0 && (i == 0 || dp[i][j-1] >= dp[i-1][j]) {
			reversedDiffs = append(reversedDiffs, DiffToken{
				Type: "wrong",
				Word: userTokens[j-1],
			})
			j--
		} else if i > 0 && (j == 0 || dp[i][j-1] < dp[i-1][j]) {
			reversedDiffs = append(reversedDiffs, DiffToken{
				Type:  "missing",
				Word:  "_",
				Match: targetTokens[i-1],
			})
			i--
		}
	}

	// Reverse to normal order
	for k := len(reversedDiffs) - 1; k >= 0; k-- {
		diffs = append(diffs, reversedDiffs[k])
	}

	accuracy := 0
	if tLen > 0 {
		accuracy = int(math.Round(float64(correctCount) / float64(tLen) * 100.0))
		if accuracy > 100 {
			accuracy = 100
		}
	}

	return DictationResult{
		Accuracy: accuracy,
		Passed:   accuracy >= 85,
		Tokens:   diffs,
	}
}
