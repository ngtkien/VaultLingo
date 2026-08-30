#!/usr/bin/env python3
"""
VaultLingo - Automated Oxford 6-Block Lexicon Batch Enrichment with OpenCode CLI
"""
import sqlite3
import subprocess
import json
import os
import sys
import re

DB_PATH = os.path.expanduser("~/.local/share/VaultLingo/vocab.db")
REPO_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/vocab.db"))

SCHEMA_PROMPT_TEMPLATE = """You are a distinguished Oxford lexicographer and English-Vietnamese linguist.
Create authentic, rich Oxford dictionary entries for the following English word(s): {words_list}.

Return ONLY a valid JSON Array (no markdown, no backticks, no markdown codeblock tags) strictly matching this schema for each word:
[
  {{
    "word": "word_lowercase",
    "pos": "Noun | Verb | Adjective | Adverb | Phrasal Verb | Idiom",
    "phonetic": "/IPA transcription/",
    "definition_en": "Accurate, clear English definition (Oxford/Cambridge standard)",
    "definition_vi": "Nghĩa tiếng Việt chuẩn mực, tự nhiên, giải thích rõ sắc thái",
    "example_en": "Natural authentic example sentence showcasing the word in context",
    "example_vi": "Bản dịch tiếng Việt tự nhiên của câu ví dụ",
    "level": "A1 | A2 | B1 | B2 | C1 | C2",
    "topic": "topic_slug"
  }}
]
"""

def enrich_words_batch(words):
    prompt = SCHEMA_PROMPT_TEMPLATE.format(words_list=", ".join(f'"{w}"' for w in words))
    try:
        res = subprocess.run(["opencode", "run", prompt], capture_output=True, text=True, timeout=30)
        output = res.stdout.strip()
        
        # Clean code fences
        if "```" in output:
            match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', output)
            if match:
                output = match.group(1).strip()
        
        first_bracket = output.find('[')
        last_bracket = output.rfind(']')
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            output = output[first_bracket:last_bracket+1]
        elif output.startswith('{') and output.endswith('}'):
            output = f"[{output}]"

        # Remove trailing commas
        output = re.sub(r',\s*([}\]])', r'\1', output)
        
        data = json.loads(output)
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception as e:
        print(f"Error enriching batch {words}: {e}")
        return []

def save_to_db(entries):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    saved = 0
    for item in entries:
        if not item.get("word") or not item.get("definition_en"):
            continue
        cur.execute("""
            INSERT INTO words (word, pos, phonetic, definition_en, definition_vi, example_en, example_vi, level, topic, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'opencode_enriched')
            ON CONFLICT(word) DO UPDATE SET
                pos = excluded.pos,
                phonetic = excluded.phonetic,
                definition_en = excluded.definition_en,
                definition_vi = excluded.definition_vi,
                example_en = excluded.example_en,
                example_vi = excluded.example_vi,
                level = excluded.level,
                topic = excluded.topic;
        """, (
            item["word"].lower().strip(),
            item.get("pos", "Word"),
            item.get("phonetic", ""),
            item.get("definition_en", ""),
            item.get("definition_vi", ""),
            item.get("example_en", ""),
            item.get("example_vi", ""),
            item.get("level", "B2"),
            item.get("topic", "vocabulary")
        ))
        saved += 1
    conn.commit()
    conn.close()
    
    # Sync with repo database
    if os.path.exists(REPO_DB_PATH):
        import shutil
        shutil.copyfile(DB_PATH, REPO_DB_PATH)
    return saved

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_words = sys.argv[1:]
    else:
        # Sample missing common words
        target_words = ["listen", "explain", "describe", "compare", "influence", "suggest", "opinion", "society", "tradition", "culture"]
    
    print(f"🚀 Enriching {len(target_words)} words with OpenCode CLI...")
    entries = enrich_words_batch(target_words)
    print(f"✅ Received {len(entries)} valid entries from OpenCode.")
    saved = save_to_db(entries)
    print(f"💾 Successfully saved {saved} words into SQLite database {DB_PATH}!")
