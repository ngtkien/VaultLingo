package backend

import (
	"encoding/json"
	"fmt"
	"strings"
)

func GetGrammarCategories() ([]GrammarCategoryInfo, error) {
	rows, err := DB.Query(`
		SELECT tense_category, COALESCE(category_icon, '⚡'), type, COUNT(*) as count
		FROM grammar_drills
		WHERE tense_category IS NOT NULL AND tense_category != ''
		GROUP BY tense_category
		ORDER BY count DESC, tense_category ASC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var categories []GrammarCategoryInfo
	for rows.Next() {
		var cat GrammarCategoryInfo
		if err := rows.Scan(&cat.TenseCategory, &cat.CategoryIcon, &cat.Type, &cat.Count); err == nil {
			categories = append(categories, cat)
		}
	}
	return categories, nil
}

func GetGrammarDrill(tenseCategory string, drillType string, excludeIDs []int) (GrammarDrill, error) {
	var g GrammarDrill
	var conditions []string
	var args []interface{}

	if tenseCategory != "" && tenseCategory != "all" {
		conditions = append(conditions, "tense_category = ?")
		args = append(args, tenseCategory)
	}

	if drillType != "" && drillType != "all" {
		conditions = append(conditions, "type = ?")
		args = append(args, drillType)
	}

	if len(excludeIDs) > 0 {
		placeholders := make([]string, len(excludeIDs))
		for i, id := range excludeIDs {
			placeholders[i] = "?"
			args = append(args, id)
		}
		conditions = append(conditions, fmt.Sprintf("id NOT IN (%s)", strings.Join(placeholders, ",")))
	}

	whereClause := ""
	if len(conditions) > 0 {
		whereClause = "WHERE " + strings.Join(conditions, " AND ")
	}

	query := fmt.Sprintf(`
		SELECT id, type, tense_category, COALESCE(category_icon, '⚡'), level, prompt_context, prompt_vi, instruction, target_question, target_vi, quasm_breakdown, grammar_tip, COALESCE(scramble_words, '[]')
		FROM grammar_drills
		%s
		ORDER BY RANDOM()
		LIMIT 1
	`, whereClause)

	var scrambleJson string
	err := DB.QueryRow(query, args...).Scan(
		&g.ID, &g.Type, &g.TenseCategory, &g.CategoryIcon, &g.Level,
		&g.PromptContext, &g.PromptVi, &g.Instruction,
		&g.TargetQuestion, &g.TargetVi, &g.QuasmBreakdown, &g.GrammarTip,
		&scrambleJson,
	)

	// If no rows found due to exclude queue, cycle without excludeIDs
	if err != nil && len(excludeIDs) > 0 {
		return GetGrammarDrill(tenseCategory, drillType, nil)
	}

	if err != nil {
		// Fallback sample
		return GrammarDrill{
			ID:             1,
			Type:           "question_form",
			TenseCategory:  "Present Perfect",
			CategoryIcon:   "✨",
			Level:          "B1",
			PromptContext:  "They have deployed the application to AWS cloud infrastructure.",
			PromptVi:       "Họ đã triển khai ứng dụng lên hạ tầng đám mây AWS.",
			Instruction:    "Đặt câu hỏi với 'Where...?' để hỏi về vị trí triển khai.",
			TargetQuestion: "Where have they deployed the application?",
			TargetVi:       "Họ đã triển khai ứng dụng ở đâu?",
			QuasmBreakdown: "Qu: Where | Aux: have | Subj: they | Verb: deployed",
			GrammarTip:     "Hiện tại hoàn thành (Nghi vấn): Wh- + have/has + S + V3/ed? Dùng để hỏi về kết quả hành động liên hệ tới hiện tại.",
			ScrambleWords:  []string{"Where", "have", "they", "deployed", "the", "application", "?"},
		}, nil
	}

	// Parse scramble words JSON
	if scrambleJson != "" {
		_ = json.Unmarshal([]byte(scrambleJson), &g.ScrambleWords)
	}
	if len(g.ScrambleWords) == 0 && g.TargetQuestion != "" {
		// Auto-generate scramble tokens from target question
		tokens := strings.Fields(g.TargetQuestion)
		g.ScrambleWords = tokens
	}

	return g, nil
}

func CheckGrammarAnswer(targetQuestion, userInput string) DictationResult {
	return CheckDictation(targetQuestion, userInput)
}
