import json
import re
import os

OUTPUT_FILE = "data/processed/sft_classical_dialogues.jsonl"
os.makedirs("data/processed", exist_ok=True)

dialogue_pairs = []

# ==========================================
# 1. PARSE ERASMUS CONVERSATIONAL FORMULAS
# ==========================================
print("Extracting Erasmus dialogue turns...")
ext_latin = "data/processed/external_latin.jsonl"
if os.path.exists(ext_latin):
    with open(ext_latin, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            fname = entry.get("metadata", {}).get("filename", "")
            if "colloqui" in fname or "antibarbari" in fname or "dialogus" in fname:
                text = entry["text"]
                paragraphs = text.split("\n\n")
                for p in paragraphs:
                    p = p.strip()
                    # Check for greeting/response lines
                    if ("Salve" in p or "valere" in p or "Quid agis" in p) and len(p) > 20:
                        sentences = [s.strip() for s in re.split(r"[.?!;]", p) if len(s.strip()) > 10]
                        if len(sentences) >= 2:
                            dialogue_pairs.append({
                                "system": "You are a fluent, authentic Classical and Renaissance Latin conversationalist (humanist scholar). Speak directly in refined, idiomatic Latin.",
                                "instruction": sentences[0] + ".",
                                "response": sentences[1] + "."
                            })

print(f"--> Extracted {len(dialogue_pairs)} Erasmus conversational exchanges.")

# ==========================================
# 2. PARSE CICERONIAN PHILOSOPHICAL DIALOGUES
# ==========================================
print("Extracting Cicero dialogue turns (De Oratore, Tusculanae)...")
cicero_file = "data/processed/perseus_classical_latin.jsonl"
speaker_pattern = re.compile(r"^([A-Z][a-z]+):\s*(.*)")

if os.path.exists(cicero_file):
    with open(cicero_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            title = str(entry.get("metadata", {}))
            if any(k in title for k in ["Tusculan", "De Oratore", "Finibus", "Republica"]):
                chunks = entry["text"].split("\n")
                current_speaker = None
                current_prompt = None

                for chunk in chunks:
                    chunk = chunk.strip()
                    m = speaker_pattern.match(chunk)
                    if m:
                        spk, content = m.group(1), m.group(2)
                        if current_prompt and len(current_prompt) > 15 and len(content) > 15:
                            dialogue_pairs.append({
                                "system": "You are an articulate interlocutor in an authentic Classical Latin philosophical dialogue in the style of Cicero.",
                                "instruction": f"{current_speaker}: {current_prompt}",
                                "response": f"{spk}: {content}"
                            })
                        current_speaker = spk
                        current_prompt = content

print(f"--> Total dialogue pairs after Cicero: {len(dialogue_pairs)}")

# ==========================================
# 3. PARSE PLATONIC ANCIENT GREEK DIALOGUES
# ==========================================
print("Extracting Platonic dialogue turns (Ancient Greek)...")
greek_file = "data/processed/perseus_ancient_greek.jsonl"
greek_speaker_pattern = re.compile(r"^([^\s:]{2,15}):\s*(.*)")

if os.path.exists(greek_file):
    with open(greek_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            meta = str(entry.get("metadata", {}))
            if "Plato" in meta or "Lucian" in meta or "Xenophon" in meta:
                chunks = entry["text"].split("\n")
                current_speaker = None
                current_prompt = None

                for chunk in chunks:
                    chunk = chunk.strip()
                    m = greek_speaker_pattern.match(chunk)
                    if m:
                        spk, content = m.group(1), m.group(2)
                        # Ensure it contains Greek characters
                        if any('\u0370' <= c <= '\u03ff' or '\u1f00' <= c <= '\u1fff' for c in content):
                            if current_prompt and len(current_prompt) > 15 and len(content) > 15:
                                dialogue_pairs.append({
                                    "system": "You are an authentic Classical Greek interlocutor in a Socratic dialogue. Converse using classical Attic vocabulary, particles, and proper polytonic Greek.",
                                    "instruction": f"{current_speaker}: {current_prompt}",
                                    "response": f"{spk}: {content}"
                                })
                            current_speaker = spk
                            current_prompt = content

print(f"--> Total dialogue pairs after Plato & Greek dialogues: {len(dialogue_pairs)}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for pair in dialogue_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"Saved classical dialogue dataset to {OUTPUT_FILE}")
