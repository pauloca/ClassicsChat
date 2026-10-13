# ClassicsChat

A defunct failed project that attempted to LoRA my way into a usable Latin and Ancient Greek chatbot.

All of the data is compiled from Perseus, thelatinlibrary.com, the Bibliotheca Augustana, the Alpheios Project, and OCR'd Archive.org books. I do believe this is one of the larger repositories of classical literature out there, but I own none of it and make no claim to it.

## Workspace Structure

```text
ClassicsChat/
├── data/
│   ├── raw/                  # Downloaded raw corpora (Perseus, First1KGreek)
│   ├── processed/            # Cleaned, normalized, metadata-tagged JSONL
│   ├── dpo/                  # Direct Preference Optimization pairs (Chosen vs Rejected calques)
│   └── external/             # User-procured corpora (PHI, TLG, custom colloquia)
│       ├── latin/            # phi/, colloquia/, comedy/, letters/, custom/
│       └── greek/            # tlg/, dialogues/, comedy_lucian/, direct_method/, custom/
├── ingestion/
│   ├── normalizer.py         # Latin & Polytonic Greek NFC normalizer (apparatus stripper)
│   ├── tei_parser.py         # TEI-XML parser extracting pure text & metadata
│   ├── download_open_corpora.py # Cloner for Perseus and First1KGreek
│   └── process_corpus.py     # Batch processing pipeline for all corpora
├── anti_anglicism/
│   ├── catalog.py            # Catalog of calques vs authentic classical expressions
│   ├── conversational_pragmatics.py # Turn-taking, greetings, assent/refusal formulas
│   └── dataset_builder.py    # DPO & SFT dataset generator
├── evaluation/
│   └── anglicism_detector.py # Purity score & particle density evaluator
├── training/
│   ├── dataset.py            # Dataset formatter for CPT and DPO
│   ├── dialogue_generator.py # SFT conversational dialogue builder
│   ├── cpt_train.py          # Continual pre-training script
│   └── dpo_train.py          # Anti-anglicism preference optimization script
├── app/
│   └── chat.py               # Interactive conversational CLI & persona tester
└── config.py                 # Central path and style configuration
```

---

## Quickstart

### 1. Ingesting Procured Files
Place any files you procure (PHI dumps, TLG texts, Erasmus/Plato texts) into the appropriate subdirectory under `data/external/`:
- Latin: `data/external/latin/`
- Greek: `data/external/greek/`

Then run the processor:
```bash
python ingestion/process_corpus.py
```

### 2. Downloading Open Scholarly Corpora
To download Perseus canonical texts or First1KGreek:
```bash
python ingestion/download_open_corpora.py --repo perseus_latin
python ingestion/download_open_corpora.py --repo first1k_greek
```

### 3. Generating Conversational SFT & DPO Data
```bash
python anti_anglicism/dataset_builder.py
python training/dialogue_generator.py
```

### 4. Running Idiomatic Purity & Anglicism Audit
```bash
python evaluation/anglicism_detector.py
```

### 5. Launching the Interactive Chat Engine
```bash
python app/chat.py
```
