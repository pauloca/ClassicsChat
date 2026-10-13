import re
import json
import os

OUTPUT_FILE = "data/processed/sft_meissner_phrasebook.jsonl"
os.makedirs("data/processed", exist_ok=True)

# Parse the Meissner JavaScript array x[...] directly
# In Meissner Unleashed:
# x[5]='^/rerum/ or /mundi universitas/^--the universe.';
# x[9]='^/deus mundum aedificavit, fabricatus est, effecit/ (not /creavit/)^{footnote}--God made the world.';

def clean_latin(text):
    # remove footnote references ^{...}
    text = re.sub(r"\^{[^}]*}", "", text)
    # remove citations #[^#]*#
    text = re.sub(r"#[^#]*#", "", text)
    # remove leading ^ and clean slashes indicating key terms
    text = text.strip("^").strip()
    text = text.replace("/", "")
    # clean macrons if represented as circumflex
    macrons = {'â': 'ā', 'ê': 'ē', 'î': 'ī', 'ô': 'ō', 'û': 'ū'}
    for circum, mac in macrons.items():
        text = text.replace(circum, mac)
    return text.strip()

def clean_english(text):
    text = re.sub(r"\^{[^}]*}", "", text)
    text = re.sub(r"#[^#]*#", "", text)
    text = text.replace("\\-\\--", "—").replace("\\-\\-", "—")
    text = text.replace("_", '"')
    return text.strip()

def parse_html_string(html_content):
    pairs = []
    # match patterns like x[123]='^...--...';
    pattern = re.compile(r"x\[\d+\]='(.*?)';", re.DOTALL)
    current_chapter = "General Classical Expressions"
    current_section = "General Idioms"

    for match in pattern.finditer(html_content):
        line = match.group(1).strip()
        if not line:
            continue
        
        # Check chapter header like +I. The World and Nature+
        if line.startswith("+") and line.endswith("+"):
            current_chapter = line.strip("+").strip()
            continue
        
        # Check section header like *1. The World\-\-Creation*
        if line.startswith("*") and line.endswith("*"):
            current_section = line.strip("*").replace("\\-\\--", "—").replace("\\-\\-", "—").strip()
            continue
        
        # Check entry line like ^/rerum/ or /mundi universitas/^--the universe.
        if line.startswith("^") and "--" in line:
            parts = line.split("--", 1)
            raw_lat = parts[0]
            raw_eng = parts[1]

            latin_phrase = clean_latin(raw_lat)
            english_meaning = clean_english(raw_eng)

            if latin_phrase and english_meaning:
                # Instruction 1: English -> Classical Latin Idiom (Anti-calque)
                pairs.append({
                    "system": "You are an expert Classical Latin tutor and philologist. Provide the authentic, idiomatic Classical Latin expression used by Cicero, Caesar, or Livy without modern English calques.",
                    "instruction": f"How do you authentically express in Classical Latin: \"{english_meaning}\" (Topic: {current_chapter} - {current_section})?",
                    "response": f"In authentic Classical Latin, this is expressed as: **{latin_phrase}**."
                })

                # Instruction 2: Classical Latin Idiom -> Meaning & Usage
                pairs.append({
                    "system": "You are an expert Classical Latin tutor and philologist. Translate and explain the authentic idiom from Classical literature.",
                    "instruction": f"What is the meaning and classical usage of the Latin phrase \"{latin_phrase}\"?",
                    "response": f"The phrase \"{latin_phrase}\" means: **{english_meaning}** (Category: {current_chapter} - {current_section})."
                })

    return pairs

