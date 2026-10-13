import re
import json
import os

INPUT_FILE = "data/raw/meissner_gutenberg.txt"
OUTPUT_FILE = "data/processed/sft_meissner_phrasebook.jsonl"
os.makedirs("data/processed", exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Trim Gutenberg header and footer
start_marker = "I. The World and Nature"
# Find the actual start of content after the table of contents
first_entry = "_rerum_ or _mundi universitas_"
start_pos = text.find(first_entry)
if start_pos == -1:
    start_pos = 0

end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
end_pos = text.find(end_marker)
if end_pos != -1:
    text = text[start_pos:end_pos]
else:
    text = text[start_pos:]

# Split text into paragraphs
paragraphs = text.split("\n\n")

instruction_pairs = []
current_chapter = "General Classical Expressions"
current_section = "General Idioms"

# Clean italics, brackets, footnote markers
def clean_str(s):
    # remove footnote references like [1], [2]
    s = re.sub(r"\[\d+\]", "", s)
    # remove Gutenberg underscores for italics
    s = s.replace("_", "")
    # normalize spaces and line breaks
    s = re.sub(r"\s+", " ", s).strip()
    return s

for p in paragraphs:
    p_clean = p.strip()
    if not p_clean:
        continue

    # Detect major Roman numeral chapters like: "I. The World and Nature"
    if re.match(r"^[I|V|X|L|C|D|M]+\.\s+[A-Za-z]", p_clean):
        current_chapter = clean_str(p_clean)
        continue

    # Detect numbered sections like: "1. The World—Creation"
    if re.match(r"^\d+\.\s+[A-Za-z]", p_clean):
        current_section = clean_str(p_clean)
        continue

    # Check for entries separated by emdash (\u2014)
    if "—" in p_clean:
        parts = p_clean.split("—", 1)
        lat_part = clean_str(parts[0])
        eng_part = clean_str(parts[1])

        # Filter out accidental non-phrase matches
        if len(lat_part) >= 3 and len(eng_part) >= 3:
            # Pair 1: English -> Authentic Classical Latin Idiom (Anti-calque instruction)
            instruction_pairs.append({
                "system": "You are an expert Classical Latin tutor and philologist. Provide the authentic, idiomatic Classical Latin expression used by Cicero, Caesar, or Livy without modern English calques or literal translations.",
                "instruction": f"How do you authentically express in Classical Latin: \"{eng_part}\"?",
                "response": f"In authentic Classical Latin, this is expressed as: **{lat_part}** (Usage domain: {current_chapter} - {current_section})."
            })

            # Pair 2: Classical Latin -> Idiomatic English Meaning & Context
            instruction_pairs.append({
                "system": "You are an expert Classical Latin scholar. Translate and explain the authentic idiom from Classical literature.",
                "instruction": f"What is the meaning and classical usage of the Latin expression: \"{lat_part}\"?",
                "response": f"The expression \"{lat_part}\" authentically means: **{eng_part}**."
            })

print(f"Parsed {len(instruction_pairs)} total Meissner SFT instruction pairs (bidirectional).")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for pair in instruction_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"Saved to {OUTPUT_FILE}")
