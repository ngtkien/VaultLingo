export interface WritingCorrection {
  original: string;
  correction: string;
  reason?: string;
}

export interface WritingAlternative {
  style: string;
  text: string;
}

export interface WritingVocabHighlight {
  term: string;
  meaning?: string;
}

export interface AiFeedbackData {
  raw: string;
  isJson: boolean;
  score: number;
  scoreLabel: string;
  overallFeedback: string;
  promptAlignment?: string;
  corrections: WritingCorrection[];
  alternatives: WritingAlternative[];
  vocabularyHighlights: WritingVocabHighlight[];
}

/**
 * Robustly parses AI evaluation output, supporting both structured JSON and markdown fallbacks
 */
export function parseAiFeedback(rawText: string): AiFeedbackData {
  const clean = (rawText || '').trim();

  // Default fallback data
  const fallbackData: AiFeedbackData = {
    raw: clean,
    isJson: false,
    score: 7.5,
    scoreLabel: 'Good Effort',
    overallFeedback: '',
    promptAlignment: '',
    corrections: [],
    alternatives: [],
    vocabularyHighlights: []
  };

  if (!clean) return fallbackData;

  // 1. Try parsing as JSON
  try {
    let jsonStr = clean;
    const codeMatch = jsonStr.match(/```(?:json)?\s*([\s\S]*?)\s*```/i);
    if (codeMatch && codeMatch[1]) {
      jsonStr = codeMatch[1].trim();
    }

    const firstBrace = jsonStr.indexOf('{');
    const lastBrace = jsonStr.lastIndexOf('}');
    if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
      jsonStr = jsonStr.substring(firstBrace, lastBrace + 1);
    }

    // Clean trailing commas
    jsonStr = jsonStr.replace(/,\s*([}\]])/g, '$1');

    const data = JSON.parse(jsonStr);
    if (data && (data.score !== undefined || data.overall_feedback || data.corrections)) {
      const scoreNum = typeof data.score === 'number' ? data.score : parseFloat(String(data.score)) || 7.5;
      
      return {
        raw: clean,
        isJson: true,
        score: scoreNum,
        scoreLabel: data.score_label || getScoreLabel(scoreNum),
        overallFeedback: data.overall_feedback || 'AI Coach evaluation and feedback for your response.',
        promptAlignment: data.prompt_alignment || '',
        corrections: Array.isArray(data.corrections) ? data.corrections.map((c: any) => ({
          original: cleanMarkdownPunct(c.original || ''),
          correction: cleanMarkdownPunct(c.correction || ''),
          reason: c.reason || ''
        })) : [],
        alternatives: Array.isArray(data.alternatives) ? data.alternatives.map((a: any) => ({
          style: cleanMarkdownPunct(a.style || 'Alternative'),
          text: cleanMarkdownQuotes(a.text || '')
        })) : [],
        vocabularyHighlights: Array.isArray(data.vocabulary_highlights) ? data.vocabulary_highlights.map((v: any) => ({
          term: cleanMarkdownPunct(v.term || ''),
          meaning: v.meaning || ''
        })) : []
      };
    }
  } catch (jsonErr) {
    // If not valid JSON, proceed to Markdown parsing below
  }

  // 2. Parse from Markdown format
  return parseMarkdownFeedback(clean);
}

function parseMarkdownFeedback(md: string): AiFeedbackData {
  let score = 7.5;
  let scoreLabel = 'Good Effort';
  let overallFeedback = '';
  let promptAlignment = '';
  const corrections: WritingCorrection[] = [];
  const alternatives: WritingAlternative[] = [];
  const vocabularyHighlights: WritingVocabHighlight[] = [];

  // Extract score (e.g. 5.5 / 10 or 8.5/10)
  const scoreMatch = md.match(/(?:Score|Rating|Overall|Score:)\s*[:*]*\s*([0-9]+(?:\.[0-9]+)?)\s*\/\s*10/i);
  if (scoreMatch && scoreMatch[1]) {
    score = parseFloat(scoreMatch[1]);
    scoreLabel = getScoreLabel(score);
  }

  // Extract Overall Feedback lines
  const lines = md.split('\n');
  let currentSection = '';

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    // Detect section headers
    if (/###\s*1\.|\bOverall Rating\b/i.test(line)) {
      currentSection = 'overall';
      continue;
    } else if (/###\s*2\.|\bGrammar\b|\bSpelling Fixes\b/i.test(line)) {
      currentSection = 'grammar';
      continue;
    } else if (/###\s*3\.|\bNatural Phrasing\b|\bAlternatives\b/i.test(line)) {
      currentSection = 'alternatives';
      continue;
    } else if (/###\s*4\.|\bVocabulary Highlight\b|\bCollocation\b/i.test(line)) {
      currentSection = 'vocab';
      continue;
    }

    // Process section content
    if (currentSection === 'overall') {
      if (line.includes('Note on Prompt Alignment') || line.includes('Alignment:')) {
        promptAlignment += line.replace(/^[>*#\s]+/, '').trim() + ' ';
      } else if (!line.startsWith('|') && !line.startsWith('---') && !line.startsWith('###')) {
        const cleanedLine = line.replace(/^[>*#\s]+/, '').replace(/\*\*/g, '').trim();
        if (cleanedLine && !cleanedLine.includes('Overall Rating & Score')) {
          overallFeedback += (overallFeedback ? ' ' : '') + cleanedLine;
        }
      }
    } else if (currentSection === 'grammar') {
      // Parse markdown table rows: | Original | Error | Correction |
      if (line.startsWith('|') && !line.includes('---') && !line.toLowerCase().includes('original')) {
        const parts = line.split('|').map(s => s.trim()).filter(Boolean);
        if (parts.length >= 2) {
          const orig = cleanMarkdownQuotes(cleanMarkdownPunct(parts[0]));
          let reason = '';
          let corr = '';
          if (parts.length >= 3) {
            reason = parts[1];
            corr = cleanMarkdownQuotes(cleanMarkdownPunct(parts[2]));
          } else {
            corr = cleanMarkdownQuotes(cleanMarkdownPunct(parts[1]));
          }
          if (orig && corr && orig.toLowerCase() !== corr.toLowerCase()) {
            corrections.push({ original: orig, correction: corr, reason });
          }
        }
      } else if (line.startsWith('*') || line.startsWith('-')) {
        // Bullet style correction
        const bulletMatch = line.match(/[`"']?([^`"':]+)[`"']?\s*(?:➔|->|to|=>|:)\s*[`"']?([^`"':]+)[`"']?(?:\s*\((.*?)\))?/);
        if (bulletMatch && bulletMatch[1] && bulletMatch[2]) {
          corrections.push({
            original: cleanMarkdownPunct(bulletMatch[1].trim()),
            correction: cleanMarkdownPunct(bulletMatch[2].trim()),
            reason: bulletMatch[3] ? bulletMatch[3].trim() : ''
          });
        }
      }
    } else if (currentSection === 'alternatives') {
      if (line.includes('Professional') || line.includes('Formal')) {
        const textMatch = line.match(/(?:Professional|Formal)[^:]*:\s*[`"']?([^`"']+)`?'?/i) || lines[i+1]?.match(/[`"']?([^`"']+)`?'?/);
        const text = textMatch ? textMatch[1] : line.replace(/^[>*#\s]+/, '');
        alternatives.push({
          style: 'Professional (Workplace)',
          text: cleanMarkdownQuotes(cleanMarkdownPunct(text))
        });
      } else if (line.includes('Casual') || line.includes('Direct') || line.includes('Slack')) {
        const textMatch = line.match(/(?:Casual|Slack|Direct)[^:]*:\s*[`"']?([^`"']+)`?'?/i) || lines[i+1]?.match(/[`"']?([^`"']+)`?'?/);
        const text = textMatch ? textMatch[1] : line.replace(/^[>*#\s]+/, '');
        alternatives.push({
          style: 'Casual (Slack / Quick Chat)',
          text: cleanMarkdownQuotes(cleanMarkdownPunct(text))
        });
      }
    } else if (currentSection === 'vocab') {
      if (line.startsWith('*') || line.startsWith('-') || line.startsWith('•')) {
        const parts = line.replace(/^[*\-•\s]+/, '').split(/[:–—]/);
        if (parts.length >= 2) {
          vocabularyHighlights.push({
            term: cleanMarkdownPunct(parts[0].trim()),
            meaning: parts.slice(1).join(':').trim()
          });
        }
      }
    }
  }

  // If no overall feedback extracted, use first non-header lines
  if (!overallFeedback) {
    overallFeedback = md.slice(0, 150).replace(/[#*`|]/g, '').trim() + '...';
  }

  return {
    raw: md,
    isJson: false,
    score,
    scoreLabel,
    overallFeedback,
    promptAlignment: promptAlignment.trim(),
    corrections,
    alternatives,
    vocabularyHighlights
  };
}

function getScoreLabel(score: number): string {
  if (score >= 9.0) return 'Exceptional (Band 9.0)';
  if (score >= 8.0) return 'Excellent (Band 8.0)';
  if (score >= 7.0) return 'Good Effort (Band 7.0)';
  if (score >= 6.0) return 'Competent (Band 6.0)';
  if (score >= 5.0) return 'Modest (Band 5.0)';
  return 'Needs Improvement';
}

function cleanMarkdownPunct(text: string): string {
  return text.replace(/\*\*/g, '').replace(/`/g, '').trim();
}

function cleanMarkdownQuotes(text: string): string {
  let res = text.replace(/^>+\s*/, '').trim();
  res = res.replace(/^["']|["']$/g, '').trim();
  return res;
}
