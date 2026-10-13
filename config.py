"""
Central configuration for ClassicsChat corpus ingestion, normalization, and training.
"""
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_LATIN_DIR = RAW_DIR / "latin"
RAW_GREEK_DIR = RAW_DIR / "greek"
EXTERNAL_DIR = DATA_DIR / "external"
PROCESSED_DIR = DATA_DIR / "processed"
DPO_DIR = DATA_DIR / "dpo"

# Classical Period and Style Metadata Tags
# Models conditioned on these tags will know which register and era to target.
LATIN_PERIODS = {
    "archaic": "Latin prior to ~80 BC (Ennius, Plautus, Terence)",
    "classical_golden": "Golden Age ~80 BC - 14 AD (Cicero, Caesar, Virgil, Horace, Ovid)",
    "classical_silver": "Silver Age ~14 AD - 150 AD (Seneca, Tacitus, Quintilian, Juvenal)",
    "late_antiquity": "Late Antique Latin ~150 - 600 AD (Apuleius, Augustine, Jerome, Boethius)",
    "medieval": "Medieval Latin ~600 - 1400 AD (Aquinas, Bede, Abelard)",
    "neo_latin": "Renaissance / Humanist Latin ~1400 - 1800 AD (Erasmus, More, Newton)",
}

GREEK_DIALECTS_AND_PERIODS = {
    "homeric_epic": "Epic / Homeric Greek (Iliad, Odyssey, Hesiod)",
    "classical_attic": "Classical Attic 5th - 4th c. BC (Plato, Thucydides, Xenophon, Lysias)",
    "classical_ionic": "Ionic prose and poetry (Herodotus, Hippocrates)",
    "classical_doric": "Doric (Theocritus, choral lyric)",
    "koine": "Hellenistic / Koine 3rd c. BC - 4th c. AD (Polybius, Plutarch, NT, Septuagint)",
    "byzantine": "Byzantine Greek ~5th - 15th c. AD (Procopius, Anna Komnene)",
}

# Normalization Settings
LATIN_NORM_DEFAULTS = {
    "harmonize_uv": True,         # 'v' -> 'u' or preserve classical distinction
    "harmonize_ij": True,         # 'j' -> 'i'
    "remove_macrons": False,      # Preserve long vowels if present in source
    "clean_brackets": True,       # Remove critical apparatus / editorial brackets [ ] < > { }
    "strip_line_numbers": True,
}

GREEK_NORM_DEFAULTS = {
    "unicode_form": "NFC",        # Standard NFC normalization for polytonic Greek
    "unify_coronis_smooth": True, # Unify coronis and smooth breathing
    "clean_brackets": True,
    "strip_line_numbers": True,
}
