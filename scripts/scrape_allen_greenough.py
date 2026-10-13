import os
import json
import urllib.request
import re
from bs4 import BeautifulSoup

RAW_DIR = "data/raw/allen_greenough"
OUTPUT_FILE = "data/processed/sft_allen_greenough.jsonl"
TREE_URL = "https://api.github.com/repos/alpheios-project/grammar-allen-greenough/git/trees/master?recursive=1"
RAW_BASE = "https://raw.githubusercontent.com/alpheios-project/grammar-allen-greenough/master/"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

print("Fetching file list from GitHub...")
req = urllib.request.Request(TREE_URL, headers={"User-Agent": "ClassicsChat-Downloader"})
data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

htm_files = [t["path"] for t in data.get("tree", []) if t["path"].endswith(".htm")]
print(f"Found {len(htm_files)} HTML files in Allen & Greenough repository.")

# Step 1: Download all files
for i, filename in enumerate(htm_files, 1):
    local_path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(local_path):
        url = RAW_BASE + filename
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ClassicsChat-Downloader"})
            content = urllib.request.urlopen(req).read()
            with open(local_path, "wb") as f:
                f.write(content)
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
    if i % 15 == 0 or i == len(htm_files):
        print(f"Downloaded {i}/{len(htm_files)} files...")

# Step 2: Parse sections into Q&A Instruction pairs
print("\nParsing HTML files into instruction pairs...")
instruction_pairs = []

for filename in os.listdir(RAW_DIR):
    if not filename.endswith(".htm"):
        continue
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    page_wrapper = soup.find(id="page-wrapper") or soup.body
    if not page_wrapper:
        continue

    # Extract top-level headings to give context
    h2_tags = [h.get_text(strip=True) for h in page_wrapper.find_all("h2")]
    h3_tags = [h.get_text(strip=True) for h in page_wrapper.find_all("h3")]
    context_topic = " - ".join([h for h in (h2_tags + h3_tags) if h])
    if not context_topic:
        context_topic = filename.replace(".htm", "").replace("-", " ").title()

    # Find paragraphs that represent distinct numbered sections
    paragraphs = page_wrapper.find_all("p")
    current_section_title = context_topic
    current_text_blocks = []

    for p in paragraphs:
        text = p.get_text(" ", strip=True)
        if not text:
            continue

        # Check for section number anchors like <strong>338.</strong> or <strong>a.</strong>
        strong = p.find("strong")
        if strong and re.match(r"^\d+\.", strong.get_text(strip=True)):
            if current_text_blocks:
                full_body = "\n\n".join(current_text_blocks)
                if len(full_body) > 40:
                    instruction_pairs.append({
                        "system": "You are an expert Classical Latin grammarian and philologist. Provide rigorous, authentic grammatical explanations adhering to Classical Latin standards.",
                        "instruction": f"According to Allen and Greenough's New Latin Grammar, explain the rule or usage concerning: {current_section_title}.",
                        "response": full_body.strip()
                    })
                current_text_blocks = []
            current_section_title = f"{context_topic} (§{strong.get_text(strip=True)})"
        
        current_text_blocks.append(text)

    if current_text_blocks:
        full_body = "\n\n".join(current_text_blocks)
        if len(full_body) > 40:
            instruction_pairs.append({
                "system": "You are an expert Classical Latin grammarian and philologist. Provide rigorous, authentic grammatical explanations adhering to Classical Latin standards.",
                "instruction": f"According to Allen and Greenough's New Latin Grammar, explain the rule or usage concerning: {current_section_title}.",
                "response": full_body.strip()
            })

print(f"\nGenerated {len(instruction_pairs)} structured Allen & Greenough Q&A pairs.")

# Write to processed SFT file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for pair in instruction_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"Saved instruction dataset to {OUTPUT_FILE}")
