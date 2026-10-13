import os
import json
import urllib.request
import re
from bs4 import BeautifulSoup

RAW_DIR = "data/raw/smyth_greek_grammar"
OUTPUT_FILE = "data/processed/sft_smyth_greek_grammar.jsonl"
TREE_URL = "https://api.github.com/repos/PerseusDL/sg_reader/git/trees/master?recursive=1"
RAW_BASE = "https://raw.githubusercontent.com/PerseusDL/sg_reader/master/"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

print("Fetching file list from PerseusDL/sg_reader repository...")
req = urllib.request.Request(TREE_URL, headers={"User-Agent": "ClassicsChat-Downloader"})
data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

html_files = [t["path"] for t in data.get("tree", []) if t["path"].startswith("data/") and t["path"].endswith(".html")]
print(f"Found {len(html_files)} HTML files in Smyth Greek Grammar repository.")

# Step 1: Download all files
for i, path in enumerate(html_files, 1):
    local_name = os.path.basename(path)
    local_path = os.path.join(RAW_DIR, local_name)
    if not os.path.exists(local_path):
        url = RAW_BASE + path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ClassicsChat-Downloader"})
            content = urllib.request.urlopen(req).read()
            with open(local_path, "wb") as f:
                f.write(content)
        except Exception as e:
            print(f"Error downloading {path}: {e}")
    if i % 20 == 0 or i == len(html_files):
        print(f"Downloaded {i}/{len(html_files)} Smyth files...")

# Step 2: Parse sections into Q&A Instruction pairs
print("\nParsing Smyth Greek Grammar files into instruction pairs...")
instruction_pairs = []

for filename in os.listdir(RAW_DIR):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    doc_title = soup.title.string.strip() if soup.title and soup.title.string else "Ancient Greek Grammar"

    # Find section divisions and paragraphs
    # In Smyth TEI-HTML, sections are usually paragraphs with section anchors or headings
    headings = soup.find_all(["h2", "h3", "h4"])
    current_topic = doc_title
    
    # Process text chunks
    content_div = soup.find("body") or soup
    elements = content_div.find_all(["h2", "h3", "h4", "p"])
    
    current_section = doc_title
    buffer_text = []

    for el in elements:
        tag_text = el.get_text(" ", strip=True)
        if not tag_text:
            continue

        if el.name in ["h2", "h3", "h4"]:
            if buffer_text:
                full_body = "\n\n".join(buffer_text)
                if len(full_body) > 60:
                    instruction_pairs.append({
                        "system": "You are an expert Classical philologist and Ancient Greek grammarian. Provide authoritative explanations of Ancient Greek morphology, syntax, and dialects adhering to standard classical Attic and Homeric usage.",
                        "instruction": f"According to Herbert Weir Smyth's Greek Grammar, explain the rule and usage regarding: {current_section}.",
                        "response": full_body.strip()
                    })
                buffer_text = []
            current_section = f"{doc_title} — {tag_text}"
        else:
            # Paragraph
            # Check if paragraph starts with section number like "123. The vowel..."
            sec_match = re.match(r"^(\d+[a-zA-Z]?\.?)\s+", tag_text)
            if sec_match and len(buffer_text) > 2:
                full_body = "\n\n".join(buffer_text)
                if len(full_body) > 60:
                    instruction_pairs.append({
                        "system": "You are an expert Classical philologist and Ancient Greek grammarian. Provide authoritative explanations of Ancient Greek morphology, syntax, and dialects adhering to standard classical Attic and Homeric usage.",
                        "instruction": f"According to Herbert Weir Smyth's Greek Grammar, explain the rule and usage regarding: {current_section}.",
                        "response": full_body.strip()
                    })
                buffer_text = []
                current_section = f"{doc_title} (§{sec_match.group(1)})"

            buffer_text.append(tag_text)

    if buffer_text:
        full_body = "\n\n".join(buffer_text)
        if len(full_body) > 60:
            instruction_pairs.append({
                "system": "You are an expert Classical philologist and Ancient Greek grammarian. Provide authoritative explanations of Ancient Greek morphology, syntax, and dialects adhering to standard classical Attic and Homeric usage.",
                "instruction": f"According to Herbert Weir Smyth's Greek Grammar, explain the rule and usage regarding: {current_section}.",
                "response": full_body.strip()
            })

print(f"\nGenerated {len(instruction_pairs)} structured Smyth Greek Grammar Q&A pairs.")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for pair in instruction_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"Saved instruction dataset to {OUTPUT_FILE}")
