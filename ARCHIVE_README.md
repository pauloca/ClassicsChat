# ClassicsChat Archive (October 2026)

This repository contains the complete dataset compilation, extraction scripts, and experimental records from the **ClassicsChat** research project.

## Archived Assets

### 1. Pretraining Corpus (28,735,303 Words)
- Location: `data/processed/classical_pretrain_chunks.jsonl` (250.2 MB)
- Ingested: Complete Perseus Ancient Greek, Perseus Classical Latin, The Latin Library (Justinian Digest, Augustine), and Erasmus humanist texts.

### 2. Master SFT Instruction Dataset (46,257 Examples)
- Location: `data/processed/sft_classics_master.jsonl` (31.18 MB)
- Ingested:
  - Allen & Greenough New Latin Grammar (772 pairs)
  - Herbert Weir Smyth Greek Grammar (810 pairs)
  - Carl Meissner Latin Phrase-Book (9,582 pairs)
  - Completed Arnold Greek & Latin Tables of Idioms (882 pairs)
  - Extant Greek Dialogues & Comedy: Plato, Lucian, Xenophon, Aristophanes (17,477 pairs)
  - Extant Latin Comedy & Satire: Plautus, Terence, Petronius, Erasmus (16,734 pairs)

### 3. Local Classics Knowledge Engine
- Location: `scripts/classics_engine.py`
- Fast, deterministic retrieval engine across all compiled grammars, idioms, and classical lexicons.

### 4. Completed OCR Idiom Tables
- `OCR/ArnoldGreekIdiom/arnold_greek_table_of_idioms_completed.json` (All 61 missing Greek translations completed)
- `OCR/ArnoldLatinIdiom/arnold_latin_table_of_idioms_completed.json` (All 36 missing Latin translations completed)

## Experimental Post-Mortem
For a full analysis of the training runs (Qwen 2.5 1.5B and 7B QLoRA) and the morphological failure modes of low-rank adaptation on ancient fusional languages, see the comprehensive [Archival Report](file:///C:/Users/Paulo/.gemini/antigravity/brain/9ebe634c-d25b-4358-9f1c-97128e55cc3b/archive_report.md).
