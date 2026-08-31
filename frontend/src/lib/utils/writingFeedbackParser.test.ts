import { describe, it, expect } from 'vitest';
import { parseAiFeedback } from './writingFeedbackParser';

describe('writingFeedbackParser', () => {
  it('should parse valid structured JSON correctly', () => {
    const rawJSON = JSON.stringify({
      score: 8.5,
      score_label: 'Excellent',
      overall_feedback: 'Clear, concise workplace communication.',
      prompt_alignment: 'Well aligned',
      corrections: [
        {
          original: 'I report my work today',
          correction: 'Here is my daily progress update',
          reason: 'More natural workplace opener.'
        }
      ],
      alternatives: [
        {
          style: 'Professional',
          text: "I've completed the core implementation and am currently running final tests."
        }
      ],
      vocabulary_highlights: [
        {
          term: 'streamline',
          meaning: 'To make an organization or system more efficient.'
        }
      ]
    });

    const parsed = parseAiFeedback(rawJSON);

    expect(parsed.isJson).toBe(true);
    expect(parsed.score).toBe(8.5);
    expect(parsed.scoreLabel).toBe('Excellent');
    expect(parsed.overallFeedback).toContain('Clear, concise');
    expect(parsed.corrections.length).toBe(1);
    expect(parsed.corrections[0].original).toBe('I report my work today');
    expect(parsed.corrections[0].correction).toBe('Here is my daily progress update');
    expect(parsed.alternatives.length).toBe(1);
    expect(parsed.alternatives[0].style).toBe('Professional');
    expect(parsed.vocabularyHighlights.length).toBe(1);
    expect(parsed.vocabularyHighlights[0].term).toBe('streamline');
  });

  it('should parse markdown block fallback correctly', () => {
    const rawMarkdown = `
### 1. Overall Rating & Score: **7.5 / 10**

> Great effort! Your message communicates the blocker effectively.
> Note on Prompt Alignment: Well aligned with the prompt.

### 2. Grammar & Spelling Fixes
| Original | Error / Issue | Correction / Reason |
| :--- | :--- | :--- |
| We face the problem | Tense error | We are facing an issue |

### 3. Natural Phrasing & Alternatives
* **Professional:** "Here is a quick update: we encountered an issue while porting the driver."
* **Casual:** "Quick heads up: hit a snag with the driver port, checking it now!"
`;

    const parsed = parseAiFeedback(rawMarkdown);

    expect(parsed.score).toBe(7.5);
    expect(parsed.corrections.length).toBeGreaterThan(0);
    expect(parsed.corrections[0].original).toBe('We face the problem');
    expect(parsed.corrections[0].correction).toBe('We are facing an issue');
    expect(parsed.alternatives.length).toBeGreaterThan(0);
  });

  it('should handle empty input safely with defaults', () => {
    const parsed = parseAiFeedback('');

    expect(parsed.score).toBe(7.5);
    expect(parsed.scoreLabel).toBe('Good Effort');
    expect(parsed.corrections).toEqual([]);
    expect(parsed.alternatives).toEqual([]);
  });
});
