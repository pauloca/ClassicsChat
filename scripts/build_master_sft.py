import json
import re
import os

OUTPUT_FILE = "data/processed/sft_classics_master.jsonl"
os.makedirs("data/processed", exist_ok=True)

all_sft_pairs = []

# ==========================================
# 1. LOAD ALLEN & GREENOUGH (772 pairs)
# ==========================================
ag_file = "data/processed/sft_allen_greenough.jsonl"
if os.path.exists(ag_file):
    with open(ag_file, "r", encoding="utf-8") as f:
        for line in f:
            all_sft_pairs.append(json.loads(line))
print(f"Loaded Allen & Greenough: {len(all_sft_pairs)} pairs.")

# ==========================================
# 2. LOAD MEISSNER LATIN PHRASE-BOOK (9,582 pairs)
# ==========================================
meiss_file = "data/processed/sft_meissner_phrasebook.jsonl"
if os.path.exists(meiss_file):
    count_before = len(all_sft_pairs)
    with open(meiss_file, "r", encoding="utf-8") as f:
        for line in f:
            all_sft_pairs.append(json.loads(line))
    print(f"Loaded Meissner: {len(all_sft_pairs) - count_before} pairs.")

# ==========================================
# 3. LOAD SMYTH GREEK GRAMMAR (810 pairs)
# ==========================================
smyth_file = "data/processed/sft_smyth_greek_grammar.jsonl"
if os.path.exists(smyth_file):
    count_before = len(all_sft_pairs)
    with open(smyth_file, "r", encoding="utf-8") as f:
        for line in f:
            all_sft_pairs.append(json.loads(line))
    print(f"Loaded Smyth Greek Grammar: {len(all_sft_pairs) - count_before} pairs.")

# ==========================================
# 4. EXTRACT PLATO SOCRATIC DIALOGUE TURNS
# ==========================================
print("Extracting Plato Greek Socratic dialogue exchanges...")
greek_file = "data/processed/perseus_ancient_greek.jsonl"
plato_turns = 0

# Matches Plato dialogue speaker codes like "ΣΩ.", "ΙΩΝ.", "ΜΕΝ.", "ΚΛ.", "ΦΑΙ.", "ΓΛ."
plato_spk_regex = re.compile(r"^([\u0370-\u03ff\u1f00-\u1fff]{2,5}\.)\s+(.*)")

if os.path.exists(greek_file):
    with open(greek_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if "Plato" in str(entry.get("metadata", {})):
                lines = entry["text"].split("\n")
                prev_spk = None
                prev_text = None

                for l in lines:
                    l = l.strip()
                    m = plato_spk_regex.match(l)
                    if m:
                        spk = m.group(1)
                        content = m.group(2).strip()
                        if prev_spk and prev_text and len(prev_text) >= 15 and len(content) >= 15:
                            all_sft_pairs.append({
                                "system": "You are Socrates or a Greek interlocutor in an authentic Platonic dialogue. Respond in classical Attic Greek using proper polytonic diacritics and conversational particles.",
                                "instruction": f"{prev_spk} {prev_text}",
                                "response": f"{spk} {content}"
                            })
                            plato_turns += 1
                        prev_spk = spk
                        prev_text = content

print(f"Added Plato dialogue turns: {plato_turns} pairs.")

# ==========================================
# 5. EXTRACT PLAUTUS & TERENCE LATIN DIALOGUE
# ==========================================
print("Extracting Plautus and Terence colloquial Latin dialogue...")
latin_file = "data/processed/perseus_classical_latin.jsonl"
comedy_turns = 0

if os.path.exists(latin_file):
    with open(latin_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            meta = str(entry.get("metadata", {}))
            if "Plautus" in meta or "Terentius" in meta or "Terence" in meta:
                # Comedies have verse dialogue turns
                lines = [l.strip() for l in entry["text"].split("\n") if len(l.strip()) > 10]
                for i in range(0, min(len(lines) - 1, 300), 2):
                    q = lines[i]
                    a = lines[i+1]
                    if len(q) > 15 and len(a) > 15:
                        all_sft_pairs.append({
                            "system": "You are a witty, authentic Classical Roman character in the comic tradition of Plautus and Terence. Converse naturally in genuine Latin without English calques.",
                            "instruction": q,
                            "response": a
                        })
                        comedy_turns += 1

print(f"Added Plautus & Terence comic dialogue turns: {comedy_turns} pairs.")

# ==========================================
# 6. EXTRACT ERASMUS COLLOQUIUM GREETINGS
# ==========================================
print("Extracting Erasmus Colloquial formulas...")
ext_latin = "data/processed/external_latin.jsonl"
erasmus_turns = 0

if os.path.exists(ext_latin):
    with open(ext_latin, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if "colloqui" in entry.get("metadata", {}).get("filename", ""):
                paras = entry["text"].split("\n\n")
                for p in paras:
                    p = p.strip()
                    if ("Salve" in p or "vale" in p or "Quid agis" in p) and len(p) > 25:
                        sents = [s.strip() for s in re.split(r"[.?!;]", p) if len(s.strip()) > 10]
                        if len(sents) >= 2:
                            all_sft_pairs.append({
                                "system": "You are a Renaissance humanist conversationalist conversing in pure Classical Latin. Greet and reply with authentic courtesy.",
                                "instruction": sents[0] + ".",
                                "response": sents[1] + "."
                            })
                            erasmus_turns += 1

print(f"Added Erasmus conversational pairs: {erasmus_turns} pairs.")

# ==========================================
# 7. SAVE UNIFIED MASTER SFT DATASET
# ==========================================
print(f"\n==========================================")
print(f"Total Unified SFT Dataset Size: {len(all_sft_pairs)} instruction examples")
print(f"Writing to {OUTPUT_FILE}...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for pair in all_sft_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"✅ Finished! Successfully wrote {len(all_sft_pairs)} pairs ({file_size_mb:.2f} MB) to {OUTPUT_FILE}")
