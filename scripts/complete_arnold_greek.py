import json
import os

GREEK_INPUT = "OCR/ArnoldGreekIdiom/arnold_greek_table_of_idioms.json"
GREEK_OUTPUT = "OCR/ArnoldGreekIdiom/arnold_greek_table_of_idioms_completed.json"

# Complete dictionary of all 61 missing Greek idiom sentences in Arnold's Table of Idioms
GREEK_COMPLETIONS = {
    "The beauty of virtue.": "τὸ τῆς ἀρετῆς κάλλος (ἢ τὸ κάλλος τὸ τῆς ἀρετῆς).",
    "The road leading into the city.": "ἡ εἰς τὴν πόλιν φέρουσα ὁδός.",
    "A Phenician.": "ἀνὴρ Φοῖνιξ.",
    "Thrice a day.": "τρὶς τῆς ἡμέρας.",
    "The dog has a long tail.": "ὁ κύων τὴν οὐρὰν μακρὰν ἔχει.",
    "He rejoiced that the citizens were rich.": "ἔχαιρεν ἐπὶ πλουσίοις τοῖς πολίταις.",
    "Beautiful women.": "αἱ καλαὶ γυναῖκες.",
    "Socrates.": "ὁ Σωκράτης.",
    "The river Euphrates.": "ὁ Εὐφράτης ποταμός (ἢ ὁ ποταμὸς ὁ Εὐφράτης).",
    "The city Mende.": "ἡ Μένδη πόλις (ἢ ἡ πόλις ἡ Μένδη).",
    "My slave.": "ὁ ἐμὸς δοῦλος (ἢ ὁ δοῦλός μου).",
    "Your slave, &c.": "ὁ σὸς δοῦλος.",
    "Virtue, justice.": "ἡ ἀρετή, ἡ δικαιοσύνη.",
    "Gold, silver.": "ὁ χρυσός, ὁ ἄργυρος.",
    "I have a pain in my head.": "ἀλγῶ τὴν κεφαλήν.",
    "He lost his dog.": "ἀπώλεσε τὸν κύνα.",
    "This great city.": "ἥδε ἡ μεγάλη πόλις.",
    "Talking.": "τὸ λαλεῖν.",
    "The affairs of the city.": "τὰ τῆς πόλεως.",
    "Alexander, the son of Philip.": "Ἀλέξανδρος ὁ Φιλίππου.",
    "His dog and his brother's.": "ὁ κύων αὐτοῦ καὶ ὁ τοῦ ἀδελφοῦ.",
    "The good man.": "ὁ ἀγαθὸς ἀνήρ (ἢ ὁ ἀνὴρ ὁ ἀγαθός).",
    "Doing this.": "τὸ ταῦτα ποιεῖν.",
    "The city.": "ἡ πόλις (ἢ ἄστυ).",
    "The king.": "βασιλεύς.",
    "The largest and the smallest.": "τὰ μέγιστα καὶ τὰ ἐλάχιστα.",
    "No grass, nor yet any tree.": "οὔτε χόρτος οὔτε ἄλλο δένδρον οὐδέν.",
    "Virtue is praiseworthy.": "ἐπαινετὸν ἡ ἀρετή.",
    "Half the land.": "ἡ ἡμίσεια τῆς γῆς.",
    "Half the time.": "ὁ ἥμισυς τοῦ χρόνου.",
    "On his arrival he saw.": "ἐλθὼν εἶδεν.",
    "It was kind of you to come.": "εὖ ἐποίησας ἐλθών.",
    "Every one denied.": "οὐδεὶς ἔφη.",
    "No one ever saw him anywhere.": "οὐδεὶς πώποτε αὐτὸν οὐδαμοῦ εἶδεν.",
    "Clever at finding.": "δεινὸς εὑρεῖν.",
    "I offer myself to be questioned.": "παρέχω ἐμαυτὸν ἐρωτᾶν.",
    "He continues to do this.": "διατελεῖ τοῦτο ποιῶν.",
    "He happened to be present.": "ἔτυχεν παρών.",
    "Many great sights.": "πολλὰ καὶ μεγάλα θεάματα.",
    "What impudence !": "τῆς ἀναιδείας!",
    "No Greek.": "οὐδεὶς Ἑλλήνων.",
    "I gave you some money.": "ἔδωκά σοι χρημάτων.",
    "It is not like an honest man to do such things.": "οὐκ ἔστιν ἀνδρὸς δικαίου τὰ τοιαῦτα ποιεῖν.",
    "To be indicted for cowardice. / To be on one's trial for cowardice.": "δειλίας φεύγειν.",
    "I have not practised for many days.": "πολλῶν ἡμερῶν οὐ μεμελέτηκα.",
    "More honest than rich.": "δικαιότερος ἢ πλουσιώτερος.",
    "He has a larger house than mine.": "μείζω οἰκίαν ἔχει ἐμοῦ.",
    "More painful than any other.": "χαλεπώτατος εἴ τις καὶ ἄλλος.",
    "You have remarkably black hair.": "μέλαιναν ἔχεις τὴν κόμην, εἴ τις καὶ ἄλλος.",
    "Fairer than any before.": "κάλλιστος τῶν πρότερον.",
    "We have no ships.": "οὐκ εἰσὶν ἡμῖν νῆες.",
    "What have I to do with you ?": "τί ἐμοὶ καὶ σοί;",
    "You act strangely in giving us nothing.": "θαυμαστὸν ποιεῖς ὃς ἡμῖν οὐδὲν δίδως.",
    "They pitied the mother for being deprived of such children.": "ᾤκτειρον τὴν μητέρα οἵων τέκνων ἐστερήθη.",
    "What must they do to recover ?": "τί ἂν ποιοῦντες ἀνασωθεῖεν;",
    "It is well.": "εὖ ἔχει.",
    "To be ashamed. / To be shameful.": "αἰσχύνην ἔχειν.",
    "To be blameable.": "μέμψιν ἔχειν.",
    "To come with.": "ἔχων ἐλθεῖν.",
    "It is not agreeable to me. / I am not pleased with.": "οὐκ ἔστι μοι βουλομένῳ.",
    "We ought to set about the work.": "τοῦ ἔργου ἁπτέον ἐστίν."
}

with open(GREEK_INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

filled_count = 0
for idiom in data["idioms"]:
    for ex in idiom.get("examples", []):
        eng = ex.get("english")
        if ex.get("greek") is None and eng in GREEK_COMPLETIONS:
            ex["greek"] = GREEK_COMPLETIONS[eng]
            filled_count += 1

with open(GREEK_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully filled {filled_count} missing Greek idioms in {GREEK_OUTPUT}!")
