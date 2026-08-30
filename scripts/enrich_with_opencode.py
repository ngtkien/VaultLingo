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

For EACH word, you MUST generate all 6 linguistic blocks:
1. Exact POS, IPA phonetic (/.../), Oxford English definition, natural Vietnamese translation.
2. Word Family members (Array of objects with "pos" and "word").
3. Etymology & Root Origin (Latin/Greek/Old English roots).
4. Real-world Contextual Examples (Array of 2 bilingual objects with "en" and "vi").
5. High-Yield Synonyms & Antonyms (Arrays of strings).
6. High-Yield Collocations (Array of strings like "demonstrate remarkable resilience", "conduct research").
7. Mnemonic Memory Hook & IELTS Nuance Tips.

Return ONLY a valid raw JSON Array (NO markdown codeblocks, NO backticks) strictly matching this schema for each word:
[
  {{
    "word": "word_lowercase",
    "pos": "Noun | Verb | Adjective | Adverb",
    "phonetic": "/IPA transcription/",
    "definition_en": "Accurate, clear English definition",
    "definition_vi": "Nghĩa tiếng Việt chuẩn mực, tự nhiên, giải thích rõ sắc thái",
    "word_family": [
      {{ "pos": "Noun", "word": "example_noun" }},
      {{ "pos": "Verb", "word": "example_verb" }},
      {{ "pos": "Adjective", "word": "example_adj" }}
    ],
    "etymology": "Concise historical root origin (e.g. From Latin '...').",
    "examples": [
      {{ "en": "Example sentence 1 in daily or academic context.", "vi": "Dịch câu 1 sang tiếng Việt." }},
      {{ "en": "Example sentence 2 in workplace or IELTS context.", "vi": "Dịch câu 2 sang tiếng Việt." }}
    ],
    "synonyms": ["synonym1", "synonym2", "synonym3"],
    "antonyms": ["antonym1", "antonym2"],
    "collocations": ["collocation phrase 1", "collocation phrase 2", "collocation phrase 3"],
    "mnemonic_hook": "A clever, memorable memory hook in Vietnamese/English",
    "nuance_tips": "Key usage tips or common errors to avoid in IELTS Speaking/Writing",
    "level": "A1 | A2 | B1 | B2 | C1 | C2",
    "topic": "topic_slug"
  }}
]
"""

def enrich_words_batch(words):
    prompt = SCHEMA_PROMPT_TEMPLATE.format(words_list=", ".join(f'"{w}"' for w in words))
    try:
        res = subprocess.run(["opencode", "run", prompt], capture_output=True, text=True, timeout=60)
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
        word = item.get("word", "").lower().strip()
        if not word or not item.get("definition_en"):
            continue
        
        examples = item.get("examples", [])
        ex_en = examples[0].get("en", "") if examples else item.get("example_en", "")
        ex_vi = examples[0].get("vi", "") if examples else item.get("example_vi", "")
        
        synonyms_json = json.dumps(item.get("synonyms", []), ensure_ascii=False)
        antonyms_json = json.dumps(item.get("antonyms", []), ensure_ascii=False)
        collocations_json = json.dumps(item.get("collocations", []), ensure_ascii=False)
        word_family_json = json.dumps(item.get("word_family", []), ensure_ascii=False)
        examples_json = json.dumps(examples, ensure_ascii=False)

        cur.execute("""
            INSERT INTO words (
                word, pos, phonetic, definition_en, definition_vi, 
                example_en, example_vi, level, topic, source,
                synonyms_json, antonyms_json, collocations_json, word_family_json,
                etymology, mnemonic_hook, nuance_tips, examples_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'opencode_full_6blocks', ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(word) DO UPDATE SET
                pos = excluded.pos,
                phonetic = excluded.phonetic,
                definition_en = excluded.definition_en,
                definition_vi = excluded.definition_vi,
                example_en = excluded.example_en,
                example_vi = excluded.example_vi,
                level = excluded.level,
                topic = excluded.topic,
                synonyms_json = excluded.synonyms_json,
                antonyms_json = excluded.antonyms_json,
                collocations_json = excluded.collocations_json,
                word_family_json = excluded.word_family_json,
                etymology = excluded.etymology,
                mnemonic_hook = excluded.mnemonic_hook,
                nuance_tips = excluded.nuance_tips,
                examples_json = excluded.examples_json;
        """, (
            word,
            item.get("pos", "Word"),
            item.get("phonetic", ""),
            item.get("definition_en", ""),
            item.get("definition_vi", ""),
            ex_en,
            ex_vi,
            item.get("level", "B2"),
            item.get("topic", "vocabulary"),
            synonyms_json,
            antonyms_json,
            collocations_json,
            word_family_json,
            item.get("etymology", ""),
            item.get("mnemonic_hook", ""),
            item.get("nuance_tips", ""),
            examples_json
        ))
        saved += 1
    conn.commit()
    conn.close()
    
    # Sync with repo database
    if os.path.exists(REPO_DB_PATH):
        import shutil
        shutil.copyfile(DB_PATH, REPO_DB_PATH)
    return saved


def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_words = sys.argv[1:]
    else:
        target_words = ["resilience", "bandwidth", "procrastinate", "influence", "serendipity", "ephemeral", "ubiquitous", "eloquent", "pragmatic"]
    
    print(f"🚀 Enriching {len(target_words)} words with OpenCode CLI (in micro-batches of 3)...")
    total_saved = 0
    for chunk in chunk_list(target_words, 3):
        print(f"👉 Processing batch: {chunk}...")
        entries = enrich_words_batch(chunk)
        if entries:
            saved = save_to_db(entries)
            total_saved += saved
            print(f"  ✅ Saved {saved} words to SQLite.")
        else:
            print(f"  ⚠️ Batch {chunk} failed.")
    print(f"🎉 Done! Total {total_saved} words enriched with ALL 6 blocks in {DB_PATH}!")
