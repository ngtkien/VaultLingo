#!/usr/bin/env python3
import sqlite3
import subprocess
import json
import os
import re
import sys
import time

DB_PATH = os.path.expanduser("~/.local/share/VaultLingo/vocab.db")

def get_unenriched_words(limit=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Priority order: A1, A2, B1, B2
    query = """
        SELECT id, word, pos, level, topic, definition_en, definition_vi
        FROM words
        WHERE etymology = '' OR etymology IS NULL OR synonyms_json = '[]' OR synonyms_json IS NULL
        ORDER BY 
            CASE 
                WHEN level = 'A1' THEN 1
                WHEN level = 'A2' THEN 2
                WHEN level = 'B1' THEN 3
                WHEN level = 'B2' THEN 4
                ELSE 5
            END,
            id ASC
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def call_ai_batch(words_chunk):
    word_list_str = ", ".join([f'"{w[1]}"' for w in words_chunk])
    
    prompt = f"""You are an Oxford lexicographer and English-Vietnamese linguist.
Create authentic, rich Oxford dictionary 6-block entries for these English words: [{word_list_str}].

Return ONLY a raw valid JSON ARRAY of objects (no markdown fences, no backticks) strictly matching this schema:
[
  {{
    "word": "...",
    "pos": "Noun | Verb | Adjective | Adverb",
    "phonetic": "/IPA/",
    "definition_en": "Clear English definition",
    "definition_vi": "Nghĩa tiếng Việt chuẩn mực",
    "word_family": [
      {{ "pos": "Noun", "word": "..." }},
      {{ "pos": "Adjective", "word": "..." }}
    ],
    "etymology": "Latin/Greek origin root breakdown",
    "examples": [
      {{ "en": "Example sentence 1.", "vi": "Dịch ví dụ 1." }},
      {{ "en": "Example sentence 2.", "vi": "Dịch ví dụ 2." }}
    ],
    "synonyms": ["syn1", "syn2", "syn3"],
    "antonyms": ["ant1", "ant2"],
    "collocations": ["collocation 1", "collocation 2", "collocation 3"],
    "mnemonic_hook": "Clever memory hook in Vietnamese",
    "nuance_tips": "IELTS usage and nuance tip in Vietnamese",
    "level": "B1"
  }}
]"""

    # Try opencode first, fallback to agy
    try:
        proc = subprocess.run(
            ["opencode", "run", prompt],
            capture_output=True,
            text=True,
            timeout=45
        )
        raw_out = proc.stdout.strip()
        if not raw_out and proc.stderr:
            raw_out = proc.stderr.strip()
    except Exception as e:
        raw_out = ""

    if not raw_out or len(raw_out) < 20:
        # Fallback to agy CLI
        try:
            proc = subprocess.run(
                ["agy", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=45
            )
            raw_out = proc.stdout.strip()
        except Exception as e:
            return None

    # Clean JSON markdown blocks
    clean_json = raw_out
    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", clean_json)
    if code_match:
        clean_json = code_match.group(1).strip()

    first_bracket = clean_json.find("[")
    last_bracket = clean_json.rfind("]")
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        clean_json = clean_json[first_bracket : last_bracket + 1]

    try:
        items = json.loads(clean_json)
        if isinstance(items, list):
            return items
    except Exception as err:
        print(f"  ⚠️ JSON parse error: {err}")
        return None

    return None

def update_word_in_db(word_item):
    word_str = word_item.get("word", "").strip().lower()
    if not word_str:
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    syns = json.dumps(word_item.get("synonyms", []))
    ants = json.dumps(word_item.get("antonyms", []))
    colls = json.dumps(word_item.get("collocations", []))
    wf = json.dumps(word_item.get("word_family", []))
    exs = json.dumps(word_item.get("examples", []))
    etym = word_item.get("etymology", "")
    m_hook = word_item.get("mnemonic_hook", "")
    n_tips = word_item.get("nuance_tips", "")
    
    pos = word_item.get("pos", "")
    phonetic = word_item.get("phonetic", "")
    def_en = word_item.get("definition_en", "")
    def_vi = word_item.get("definition_vi", "")

    cursor.execute("""
        UPDATE words SET
            synonyms_json = ?,
            antonyms_json = ?,
            collocations_json = ?,
            word_family_json = ?,
            etymology = ?,
            mnemonic_hook = ?,
            nuance_tips = ?,
            examples_json = ?
        WHERE LOWER(word) = ?
    """, (syns, ants, colls, wf, etym, m_hook, n_tips, exs, word_str))

    # Also update pos, phonetic, definitions if provided and missing
    if pos or phonetic or def_en or def_vi:
        cursor.execute("""
            UPDATE words SET
                pos = CASE WHEN pos = '' OR pos IS NULL THEN ? ELSE pos END,
                phonetic = CASE WHEN phonetic = '' OR phonetic IS NULL THEN ? ELSE phonetic END,
                definition_en = CASE WHEN definition_en = '' OR definition_en IS NULL THEN ? ELSE definition_en END,
                definition_vi = CASE WHEN definition_vi = '' OR definition_vi IS NULL THEN ? ELSE definition_vi END
            WHERE LOWER(word) = ?
        """, (pos, phonetic, def_en, def_vi, word_str))

    conn.commit()
    conn.close()
    return True

def run_batch_enrichment(total_target=40, chunk_size=4):
    print(f"🚀 Starting batch enrichment pipeline for target: {total_target} words (chunk size: {chunk_size})...")
    
    enriched_count = 0
    while enriched_count < total_target:
        needed = min(chunk_size, total_target - enriched_count)
        words_chunk = get_unenriched_words(needed)
        if not words_chunk:
            print("🎉 No more unenriched words found in database!")
            break

        chunk_words = [w[1] for w in words_chunk]
        print(f"\n📦 Processing batch ({len(chunk_words)} words): {chunk_words}...")
        start_time = time.time()
        
        results = call_ai_batch(words_chunk)
        elapsed = round(time.time() - start_time, 2)

        if not results:
            print(f"  ❌ Failed to synthesize batch via AI ({elapsed}s). Retrying single items...")
            time.sleep(2)
            continue

        success_in_batch = 0
        for item in results:
            if update_word_in_db(item):
                success_in_batch += 1
                enriched_count += 1
                print(f"  ✅ Saved 6-block data for '{item.get('word')}'")

        print(f"  ⏱️ Batch completed in {elapsed}s. Total enriched so far: {enriched_count}/{total_target}")
        time.sleep(0.5)

    print(f"\n🎉 Finished batch enrichment run! Total newly enriched words: {enriched_count}")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    run_batch_enrichment(total_target=count, chunk_size=4)
