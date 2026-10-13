import json
import os

LATIN_INPUT = "OCR/ArnoldLatinIdiom/arnold_latin_table_of_idioms.json"
LATIN_OUTPUT = "OCR/ArnoldLatinIdiom/arnold_latin_table_of_idioms_completed.json"

# Complete dictionary of all 36 missing Latin idiom sentences in Arnold's Table of Idioms
LATIN_COMPLETIONS = {
    "He promises to come.": "Pollicetur se venturum esse.",
    "He hopes to live.": "Sperat se victurum esse.",
    "He undertakes to do it.": "Recipit se facturum esse.",
    "He pretends to be mad (16).": "Simulat se insanire.",
    "He sends the most faithful slave he has.": "Mittit servum, quem fidelissimum habet.",
    "He was the first to do this, / (Or) He was the first who did this.": "Primus hoc fecit.",
    "Such is your temperance, / Or, With your usual temperance.": "Quae tua est temperantia (vel: Pro tua temperantia).",
    "To make the same boast.": "Idem gloriari.",
    "To make the same promise.": "Idem polliceri.",
    "To make many promises.": "Multa polliceri.",
    "To utter many falsehoods.": "Multa mentiri.",
    "The city of Rome, the island of Cyprus.": "Urbs Roma, insula Cyprus.",
    "He did this as (or when) Consul.": "Hoc consul fecit.",
    "Of whom there are few / very many.": "Qui pauci / permulti sunt.",
    "He was condemned in his absence.": "Absens damnatus est.",
    "It is characteristic of . . . / It is incumbent on . . . / It is for . . .": "Est (proprium) alicuius...",
    "It demands, or requires, firmness.": "Constantiae est.",
    "It shows, or betrays, weakness.": "Imbecillitatis est.",
    "Any man may do it.": "Cuiusvis hominis est hoc facere.",
    "It is wise.": "Sapientis est.",
    "He does it without robbing others.": "Hoc facit, non spoliando alios (vel: ita ut alios non spoliet).",
    "Henry, Charles, and John.": "Henricus, Carolus, Iohannes (vel: Henricus et Carolus et Iohannes).",
    "When I take my journey, I will come.": "Cum iter fecero, veniam.",
    "When I have performed this, I will come.": "Cum hoc perfecero, veniam.",
    "When he is come, he will tell us.": "Cum venerit, nobis narrabit.",
    "When you wish to play, remember to play fair.": "Cum ludere voles, memento aequo animo ludere.",
    "As you sow, so will you reap.": "Ut sementem feceris, ita metes.",
    "I will do it, if I can.": "Faciam, si potero.",
    "I have found scarcely any thing to censure.": "Vix quicquam repperi quod reprehendam.",
    "Men who abound in silver, in gold, in estates.": "Homines qui argento, qui auro, qui praediis abundant.",
    "Men who abound neither in silver, nor in gold, nor in estates.": "Homines qui nec argento nec auro nec praediis abundant.",
    "A pen to write with.": "Calamus quo scribatur.",
    "(5) He is not a proper person to be received.": "Non est idoneus qui recipiatur.",
    "(7) Of such a kind that we can neglect duties for their sake.": "Eiusmodi cuius causa officia neglegere possimus.",
    "(10) Who am I that my writings should be honoured thus ?": "Quis sum cuius scripta sic celebrentur?",
    "Who, as B. says, was killed.": "Quem B. dicit interfectum esse."
}

with open(LATIN_INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

filled_count = 0
for idiom in data["idioms"]:
    for ex in idiom.get("examples", []):
        eng = ex.get("english")
        if ex.get("latin") is None and eng in LATIN_COMPLETIONS:
            ex["latin"] = LATIN_COMPLETIONS[eng]
            filled_count += 1

with open(LATIN_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully filled {filled_count} missing Latin idioms in {LATIN_OUTPUT}!")
