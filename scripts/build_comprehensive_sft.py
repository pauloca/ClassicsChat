import json
import re
import os

OUTPUT_FILE = "data/processed/sft_classics_master.jsonl"
os.makedirs("data/processed", exist_ok=True)

all_sft_pairs = []

# =========================================================================
# 1. GRAMMARS: ALLEN & GREENOUGH (Latin) & HERBERT WEIR SMYTH (Greek)
# =========================================================================
ag_file = "data/processed/sft_allen_greenough.jsonl"
if os.path.exists(ag_file):
    with open(ag_file, "r", encoding="utf-8") as f:
        for line in f:
            all_sft_pairs.append(json.loads(line))
print(f"[1/7] Allen & Greenough Grammar: {len(all_sft_pairs)} pairs.")

smyth_file = "data/processed/sft_smyth_greek_grammar.jsonl"
if os.path.exists(smyth_file):
    cnt = len(all_sft_pairs)
    with open(smyth_file, "r", encoding="utf-8") as f:
        for line in f:
            all_sft_pairs.append(json.loads(line))
    print(f"[2/7] Smyth Greek Grammar: {len(all_sft_pairs) - cnt} pairs.")

# =========================================================================
# 2. PHRASEBOOKS & IDIOMS: MEISSNER (Latin) + COMPLETED ARNOLD (Greek & Latin)
# =========================================================================
meiss_file = "data/processed/sft_meissner_phrasebook.jsonl"
if os.path.exists(meiss_file):
    cnt = len(all_sft_pairs)
    with open(meiss_file, "r", encoding="utf-8") as f:
        for line in f:
            all_sft_pairs.append(json.loads(line))
    print(f"[3/7] Meissner Latin Phrase-Book: {len(all_sft_pairs) - cnt} pairs.")

# Completed Arnold Greek Idioms
arnold_greek_file = "OCR/ArnoldGreekIdiom/arnold_greek_table_of_idioms_completed.json"
if os.path.exists(arnold_greek_file):
    cnt = len(all_sft_pairs)
    data = json.load(open(arnold_greek_file, encoding="utf-8"))
    for item in data.get("idioms", []):
        for ex in item.get("examples", []):
            eng = ex.get("english")
            grk = ex.get("greek")
            lit = ex.get("literal_or_explanation", "")
            if eng and grk:
                all_sft_pairs.append({
                    "system": "You are an expert Classical philologist and Ancient Greek tutor. Provide the authentic, idiomatic Classical Greek translation.",
                    "instruction": f"How do you authentically say in Ancient Greek: \"{eng}\"?",
                    "response": f"In Classical Greek: **{grk}**" + (f" (Literal: {lit})" if lit else "")
                })
                all_sft_pairs.append({
                    "system": "You are an expert Classical philologist and Ancient Greek tutor. Translate and explain the Greek idiom.",
                    "instruction": f"Translate and explain the Greek idiom: \"{grk}\".",
                    "response": f"The Greek expression \"{grk}\" means: **{eng}**" + (f" (Literal explanation: {lit})" if lit else "")
                })
    print(f"[4/7] Arnold Greek Table of Idioms (OCR Completed): {len(all_sft_pairs) - cnt} pairs.")

# Completed Arnold Latin Idioms
arnold_latin_file = "OCR/ArnoldLatinIdiom/arnold_latin_table_of_idioms_completed.json"
if os.path.exists(arnold_latin_file):
    cnt = len(all_sft_pairs)
    data = json.load(open(arnold_latin_file, encoding="utf-8"))
    for item in data.get("idioms", []):
        for ex in item.get("examples", []):
            eng = ex.get("english")
            lat = ex.get("latin")
            lit = ex.get("literal_or_explanation", "")
            if eng and lat:
                all_sft_pairs.append({
                    "system": "You are an expert Classical Latin tutor and philologist. Provide the authentic, idiomatic Classical Latin translation.",
                    "instruction": f"How do you authentically express in Classical Latin: \"{eng}\"?",
                    "response": f"In Classical Latin: **{lat}**" + (f" (Literal: {lit})" if lit else "")
                })
                all_sft_pairs.append({
                    "system": "You are an expert Classical Latin scholar. Translate and explain the Latin idiom.",
                    "instruction": f"Translate and explain the Latin idiom: \"{lat}\".",
                    "response": f"The Latin expression \"{lat}\" means: **{eng}**" + (f" (Literal explanation: {lit})" if lit else "")
                })
    print(f"[5/7] Arnold Latin Table of Idioms (OCR Completed): {len(all_sft_pairs) - cnt} pairs.")

# =========================================================================
# 3. GREEK DIALOGUES & COMEDY: ALL PLATO, ALL 87 LUCIAN, ALL XENOPHON, ALL 8 ARISTOPHANES
# =========================================================================
print("Extracting ALL Greek Dialogues (Plato, 87 Lucian, Xenophon) & ALL 8 Aristophanes Comedies...")
cnt = len(all_sft_pairs)
greek_file = "data/processed/perseus_ancient_greek.jsonl"

def is_greek(s):
    return any('\u0370' <= c <= '\u03ff' or '\u1f00' <= c <= '\u1fff' for c in s)

if os.path.exists(greek_file):
    with open(greek_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            meta = str(entry.get("metadata", {}))

            # Target Authors: Plato, Lucian, Xenophon, Aristophanes
            if any(k in meta for k in ["Plato", "Lucian", "Xenophon", "Aristophanes"]):
                # Split by lines or speaker paragraphs
                raw_text = entry["text"]
                lines = [l.strip() for l in raw_text.split("\n") if len(l.strip()) > 12 and is_greek(l)]

                # Extract paired turns across the entire work
                for i in range(0, len(lines) - 1, 2):
                    turn_a = lines[i]
                    turn_b = lines[i+1]
                    if len(turn_a) >= 15 and len(turn_b) >= 15:
                        if "Aristophanes" in meta:
                            role = "You are a witty, colloquial character in an authentic Attic comedy by Aristophanes. Respond in genuine Classical Attic Greek."
                        elif "Lucian" in meta:
                            role = "You are a satirical interlocutor in an authentic dialogue by Lucian of Samosata. Converse with sharp, refined Classical Greek wit."
                        elif "Xenophon" in meta:
                            role = "You are an interlocutor in an authentic Socratic dialogue by Xenophon. Speak in pure, graceful Classical Attic Greek."
                        else:
                            role = "You are an interlocutor in an authentic Platonic dialogue. Respond in classical Attic Greek using proper polytonic diacritics and conversational particles."

                        all_sft_pairs.append({
                            "system": role,
                            "instruction": turn_a,
                            "response": turn_b
                        })

print(f"[6/7] Comprehensive Greek Dialogues & Comedy (All Plato, Lucian, Xenophon, Aristophanes): {len(all_sft_pairs) - cnt} pairs.")

# =========================================================================
# 4. LATIN COMEDY, SATIRE & CONVERSATION: ALL 20 PLAUTUS, ALL 6 TERENCE, PETRONIUS, ERASMUS
# =========================================================================
print("Extracting ALL Latin Comedy (20 Plautus, 6 Terence), Petronius Satyricon, & Erasmus...")
cnt = len(all_sft_pairs)
latin_file = "data/processed/perseus_classical_latin.jsonl"

if os.path.exists(latin_file):
    with open(latin_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            meta = str(entry.get("metadata", {}))

            if "Plautus" in meta or "Terentius" in meta or "Terence" in meta:
                # ALL 20 Plautus and ALL 6 Terence plays completely extracted
                lines = [l.strip() for l in entry["text"].split("\n") if len(l.strip()) > 10]
                for i in range(0, len(lines) - 1, 2):
                    q = lines[i]
                    a = lines[i+1]
                    if len(q) > 15 and len(a) > 15:
                        all_sft_pairs.append({
                            "system": "You are a witty, authentic Classical Roman character in the comic tradition of Plautus and Terence. Converse naturally in genuine Latin without English calques.",
                            "instruction": q,
                            "response": a
                        })

            elif "Petronius" in meta:
                # Entire Satyricon dialogue turns
                paras = entry["text"].split("\n\n")
                for p in paras:
                    p = p.strip()
                    sentences = [s.strip() for s in re.split(r"[.?!;]", p) if len(s.strip()) > 15]
                    for i in range(0, len(sentences) - 1, 2):
                        all_sft_pairs.append({
                            "system": "You are a lively Roman speaker at Trimalchio's banquet in Petronius's Satyricon. Converse in vivid, authentic, everyday Classical Latin.",
                            "instruction": sentences[i] + ".",
                            "response": sentences[i+1] + "."
                        })

# Erasmus Colloquial Formulas & Dialogues
ext_latin = "data/processed/external_latin.jsonl"
if os.path.exists(ext_latin):
    with open(ext_latin, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            fname = entry.get("metadata", {}).get("filename", "")
            if "colloqui" in fname or "dialogus" in fname:
                paras = entry["text"].split("\n\n")
                for p in paras:
                    p = p.strip()
                    sents = [s.strip() for s in re.split(r"[.?!;]", p) if len(s.strip()) > 12]
                    for i in range(0, len(sents) - 1, 2):
                        all_sft_pairs.append({
                            "system": "You are a Renaissance humanist scholar conversing in pure Classical Latin. Greet and reply with authentic courtesy.",
                            "instruction": sents[i] + ".",
                            "response": sents[i+1] + "."
                        })

print(f"[7/7] Comprehensive Latin Comedy, Satire & Humanist Dialogue (All Plautus, Terence, Petronius, Erasmus): {len(all_sft_pairs) - cnt} pairs.")

# =========================================================================
# 5. WRITE EXPANDED MASTER SFT DATASET
# =========================================================================
print(f"\n==========================================")
print(f"Grand Total Comprehensive SFT Dataset Size: {len(all_sft_pairs)} instruction examples")
print(f"Writing to {OUTPUT_FILE}...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for pair in all_sft_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

sz = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"Done! Successfully wrote {len(all_sft_pairs)} instruction pairs ({sz:.2f} MB) to {OUTPUT_FILE}")
