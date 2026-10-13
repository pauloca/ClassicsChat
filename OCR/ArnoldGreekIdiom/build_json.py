import json
import unicodedata
from pathlib import Path

idioms_data = [
    {
        "id": 1,
        "page": 123,
        "examples": [
            {
                "english": "The beauty of virtue.",
                "greek": None,
                "literal_or_explanation": "The beauty of the virtue (§ 5 (2)); (or) The of the virtue beauty (§ 9 (2) b).",
                "section_ref": "§ 5 (2); § 9 (2) b"
            }
        ]
    },
    {
        "id": 2,
        "page": 123,
        "examples": [
            {
                "english": "The road leading into the city.",
                "greek": None,
                "literal_or_explanation": "The into the city leading road.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 3,
        "page": 123,
        "examples": [
            {
                "english": "A slave.",
                "greek": "δοῦλός τις",
                "literal_or_explanation": "A certain slave (δοῦλός τις) (§ 1 (2)).",
                "section_ref": "§ 1 (2)"
            },
            {
                "english": "A Phenician.",
                "greek": None,
                "literal_or_explanation": "A man a Phenician.",
                "section_ref": None
            },
            {
                "english": "Thrice a day.",
                "greek": None,
                "literal_or_explanation": "Thrice the day.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 4,
        "page": 123,
        "examples": [
            {
                "english": "The dog has a long tail.",
                "greek": None,
                "literal_or_explanation": "The dog has the tail long (§ 2).",
                "section_ref": "§ 2"
            },
            {
                "english": "He rejoiced that the citizens were rich.",
                "greek": None,
                "literal_or_explanation": "He rejoiced at rich the citizens.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 5,
        "page": 123,
        "examples": [
            {
                "english": "Beautiful women.",
                "greek": None,
                "literal_or_explanation": "The beautiful women (§ 3).",
                "section_ref": "§ 3"
            },
            {
                "english": "The rest.",
                "greek": "οἱ ἄλλοι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Others.",
                "greek": "ἄλλοι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "The multitude.",
                "greek": "οἱ πολλοί.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Many.",
                "greek": "πολλοί.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "The whole city.",
                "greek": "ἡ πᾶσα πόλις.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Every city.",
                "greek": "πᾶσα πόλις.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Beautiful things. / What is beautiful.",
                "greek": "τὰ καλά.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 6,
        "page": 123,
        "examples": [
            {
                "english": "Socrates.",
                "greek": None,
                "literal_or_explanation": "The Socrates (§ 4).",
                "section_ref": "§ 4"
            },
            {
                "english": "The river Euphrates.",
                "greek": None,
                "literal_or_explanation": "The Euphrates river ; (or) The river the Euphrates.",
                "section_ref": None
            },
            {
                "english": "The city Mende.",
                "greek": None,
                "literal_or_explanation": "The Mende city ; (or) The city the Mende.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 7,
        "page": 123,
        "examples": [
            {
                "english": "My slave.",
                "greek": None,
                "literal_or_explanation": "The my slave (§ 6 (1)).",
                "section_ref": "§ 6 (1)"
            },
            {
                "english": "Your slave, &c.",
                "greek": None,
                "literal_or_explanation": "The your slave.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 8,
        "page": 123,
        "examples": [
            {
                "english": "Virtue, justice.",
                "greek": None,
                "literal_or_explanation": "The virtue, the justice (§ 5 (2)).",
                "section_ref": "§ 5 (2)"
            },
            {
                "english": "Gold, silver.",
                "greek": None,
                "literal_or_explanation": "The gold, the silver.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 9,
        "page": 123,
        "examples": [
            {
                "english": "I have a pain in my head.",
                "greek": None,
                "literal_or_explanation": "I have a pain in the head (§ 5).",
                "section_ref": "§ 5"
            },
            {
                "english": "He lost his dog.",
                "greek": None,
                "literal_or_explanation": "He lost the dog.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 10,
        "page": 123,
        "examples": [
            {
                "english": "This city.",
                "greek": "ἥδε ἡ πόλις",
                "literal_or_explanation": "This the city (ἥδε ἡ πόλις) (§ 6 (2)).",
                "section_ref": "§ 6 (2)"
            },
            {
                "english": "This great city.",
                "greek": None,
                "literal_or_explanation": "This the great city.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 11,
        "page": "123-124",
        "examples": [
            {
                "english": "He who does.",
                "greek": "ὁ πράττων",
                "literal_or_explanation": None,
                "section_ref": "§ 7"
            },
            {
                "english": "Those who do.",
                "greek": "οἱ πράττοντες.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He who does not do.",
                "greek": "ὁ μὴ πράττων, &c.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 12,
        "page": 124,
        "examples": [
            {
                "english": "Talking.",
                "greek": None,
                "literal_or_explanation": "The to talk (infinitive).",
                "section_ref": None
            },
            {
                "english": "Doing good to everybody.",
                "greek": "τὸ πάντας εὖ ποιεῖν",
                "literal_or_explanation": "The to-do good to all (τὸ πάντας εὖ ποιεῖν).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 13,
        "page": 124,
        "examples": [
            {
                "english": "Beauty.",
                "greek": "τὸ καλόν",
                "literal_or_explanation": "The beautiful (τὸ καλόν) (§ 8).",
                "section_ref": "§ 8"
            },
            {
                "english": "Honour.",
                "greek": "τὸ καλόν",
                "literal_or_explanation": "The honourable (τὸ καλόν).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 14,
        "page": 124,
        "examples": [
            {
                "english": "The people in the city.",
                "greek": "οἱ ἐν ἄστει",
                "literal_or_explanation": "The in city (οἱ ἐν ἄστει).",
                "section_ref": None
            },
            {
                "english": "The disciples of Plato.",
                "greek": "οἱ περὶ Πλάτωνα",
                "literal_or_explanation": "The round Plato (οἱ περὶ Πλάτωνα).",
                "section_ref": None
            },
            {
                "english": "The men of old.",
                "greek": "οἱ πάλαι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "The interval (of time).",
                "greek": "ὁ μεταξὺ χρόνος.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "The facts.",
                "greek": "τὰ πεπραγμένα. / τὰ γενόμενα.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 15,
        "page": 124,
        "examples": [
            {
                "english": "The affairs of the city.",
                "greek": None,
                "literal_or_explanation": "The (neut. pl.) of the city.",
                "section_ref": None
            },
            {
                "english": "What comes from the gods.",
                "greek": "τὰ ἐκ θεῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Alexander, the son of Philip.",
                "greek": None,
                "literal_or_explanation": "Alexander the of Philip (§ 9).",
                "section_ref": "§ 9"
            },
            {
                "english": "His dog and his brother's.",
                "greek": None,
                "literal_or_explanation": "The dog of him, and the of the brother.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 16,
        "page": 124,
        "examples": [
            {
                "english": "The good man.",
                "greek": None,
                "literal_or_explanation": "The good man ; (or) The man the good.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 17,
        "page": 124,
        "examples": [
            {
                "english": "Doing this.",
                "greek": None,
                "literal_or_explanation": "The this (these things) to do.",
                "section_ref": None
            },
            {
                "english": "(Such conduct.)",
                "greek": "τὸ ταῦτα πράττειν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Such a person.",
                "greek": "ὁ τοιοῦτος.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 18,
        "page": 124,
        "examples": [
            {
                "english": "The city.",
                "greek": None,
                "literal_or_explanation": "City (§ 10).",
                "section_ref": "§ 10"
            },
            {
                "english": "The king.",
                "greek": None,
                "literal_or_explanation": "King.",
                "section_ref": None
            },
            {
                "english": "The largest and the smallest.",
                "greek": None,
                "literal_or_explanation": "The largest and smallest.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 19,
        "page": 124,
        "examples": [
            {
                "english": "The one — the other.",
                "greek": "ὁ μὲν — ὁ δέ",
                "literal_or_explanation": None,
                "section_ref": "§ 11"
            },
            {
                "english": "Some — others.",
                "greek": "οἱ μὲν — οἱ δέ.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "But he.",
                "greek": "ὁ δέ.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "And he.",
                "greek": "καὶ ὅς.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 20,
        "page": 124,
        "examples": [
            {
                "english": "He came of his own accord.",
                "greek": "αὐτὸς ἦλθεν",
                "literal_or_explanation": None,
                "section_ref": "§ 12"
            },
            {
                "english": "We are alone.",
                "greek": "αὐτοί ἐσμεν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 21,
        "page": 124,
        "examples": [
            {
                "english": "I saw him.",
                "greek": "εἶδον αὐτόν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I saw the man himself.",
                "greek": "αὐτὸν εἶδον.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 22,
        "page": 124,
        "examples": [
            {
                "english": "The ships and their crews.",
                "greek": "αἱ νῆες αὐτοῖς τοῖς ἀνδράσιν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Pericles with nine others.",
                "greek": "Περικλῆς δέκατος αὐτός.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 23,
        "page": 124,
        "examples": [
            {
                "english": "I did it myself.",
                "greek": "αὐτὸς ἐποίησα.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I pricked myself.",
                "greek": "ἔνυξα ἐμαυτόν",
                "literal_or_explanation": None,
                "section_ref": "§ 14"
            },
            {
                "english": "I pricked myself.",
                "greek": "αὐτὸν ἐμὲ ἔνυξα.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 24,
        "page": 124,
        "examples": [
            {
                "english": "He said that he did it himself.",
                "greek": "ἔφη αὐτὸς ποιῆσαι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He said that another did it, not himself.",
                "greek": "ἔφη ἄλλον τινά, καὶ οὐκ αὐτὸς ποιῆσαι.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 25,
        "page": 124,
        "examples": [
            {
                "english": "The opposite party.",
                "greek": "οἱ ἕτεροι",
                "literal_or_explanation": None,
                "section_ref": "§ 15"
            },
            {
                "english": "A different cup.",
                "greek": "ἕτερον ποτήριον.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "One cup more.",
                "greek": "ἄλλο ποτήριον.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "No grass, nor yet any tree.",
                "greek": None,
                "literal_or_explanation": "No grass nor any other tree.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 26,
        "page": "124-125",
        "examples": [
            {
                "english": "You say right, true, &c.",
                "greek": "δίκαια, ἀληθῆ",
                "literal_or_explanation": "You say right, true (things) (δίκαια, ἀληθῆ) (§ 16).",
                "section_ref": "§ 16"
            },
            {
                "english": "What comes from the gods.",
                "greek": "τὰ ἐκ θεῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Fortune.",
                "greek": "τὰ τῆς τύχης.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 27,
        "page": 125,
        "examples": [
            {
                "english": "To render many services.",
                "greek": "πολλὰ ὑπηρετεῖν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "To render many great services.",
                "greek": "πολλὰ καὶ μεγάλα ὑπηρετεῖν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 28,
        "page": 125,
        "examples": [
            {
                "english": "Virtue is praiseworthy.",
                "greek": None,
                "literal_or_explanation": "The virtue is a praiseworthy thing (neut. sing.).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 29,
        "page": 125,
        "examples": [
            {
                "english": "Half the land.",
                "greek": None,
                "literal_or_explanation": "The half (adj.) of the land (§ 16 (5)).",
                "section_ref": "§ 16 (5)"
            },
            {
                "english": "Half the time.",
                "greek": None,
                "literal_or_explanation": "The half (adj.) of the time (§ 16 (5)).",
                "section_ref": "§ 16 (5)"
            },
            {
                "english": "Most men.",
                "greek": "οἱ πολλοὶ τῶν ἀνθρώπων.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Sensible men.",
                "greek": "οἱ φρόνιμοι τῶν ἀνθρώπων.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 30,
        "page": 125,
        "examples": [
            {
                "english": "Animals run.",
                "greek": "τὰ ζῷα τρέχει",
                "literal_or_explanation": "The animals runs (τὰ ζῷα τρέχει).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 31,
        "page": 125,
        "examples": [
            {
                "english": "So to say.",
                "greek": "ὡς εἰπεῖν. / ὡς ἔπος εἰπεῖν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 32,
        "page": 125,
        "examples": [
            {
                "english": "To be well off.",
                "greek": "εὖ πράττειν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "To be in a good state.",
                "greek": "εὖ διακεῖσθαι.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 33,
        "page": 125,
        "examples": [
            {
                "english": "Do not steal.",
                "greek": "μὴ κλέψῃς",
                "literal_or_explanation": "μὴ κλέψῃς (of a single act).",
                "section_ref": None
            },
            {
                "english": "Do not be a thief.",
                "greek": "μὴ κλέπτε",
                "literal_or_explanation": "μὴ κλέπτε (of a habit).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 34,
        "page": 125,
        "examples": [
            {
                "english": "On his arrival he saw.",
                "greek": None,
                "literal_or_explanation": "Having come he saw (§ 18).",
                "section_ref": "§ 18"
            },
            {
                "english": "It was kind of you to come.",
                "greek": None,
                "literal_or_explanation": "You did well having come (§ 18).",
                "section_ref": "§ 18"
            }
        ]
    },
    {
        "id": 35,
        "page": 125,
        "examples": [
            {
                "english": "To say that.",
                "greek": "φάναι, followed by acc. and inf. / λέγειν, followed by acc. and inf. or ὅτι (ὡς). / εἰπεῖν, followed by ὅτι (ὡς).",
                "literal_or_explanation": "φάναι, followed by acc. and inf.\nλέγειν, followed by acc. and inf. or ὅτι (ὡς).\nεἰπεῖν, followed by ὅτι (ὡς).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 36,
        "page": 125,
        "category": "Modes of expressing a wish",
        "category_ref": "§ 62 (5)",
        "examples": [
            {
                "english": "Would I were one of them.",
                "greek": "τούτων ἐγὼ εἴην.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "O that you might wish it.",
                "greek": "ἀλλὰ βουληθείης.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Heaven forbid.",
                "greek": "μὴ γένοιτο.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "O that I were there.",
                "greek": "ἐκεῖ γενοίμην.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Would that you were our friend.",
                "greek": "εἴθε συ φίλος ἡμῖν γένοιο.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "O that I might perish.",
                "greek": "πῶς ἂν ὀλοίμην;",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Would I had been with you then.",
                "greek": "εἴθε σοι τότε συνεγενόμην.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Would that they were able.",
                "greek": "εἰ γὰρ ὤφελον οἷοί τε εἶναι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Would I had never left Scyrus.",
                "greek": "μήποτ' ὤφελον λιπεῖν τὴν Σκῦρον.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 37,
        "page": 125,
        "examples": [
            {
                "english": "What am I to say ?",
                "greek": "τί φῶ;",
                "literal_or_explanation": None,
                "section_ref": "§ 20 (3)"
            },
            {
                "english": "Shall we stay ?",
                "greek": "βούλει μένωμεν;",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 38,
        "page": 125,
        "category": "Sequence—Sentences of purpose",
        "category_ref": "§ 21",
        "examples": [
            {
                "english": "I am here to see.",
                "greek": "πάρειμι ἵνα (ὡς, ὅπως) ἴδω.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I was there to see.",
                "greek": "παρῆν ἵνα ἴδοιμι.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 39,
        "page": "125-126",
        "category": "Indirect questions",
        "category_ref": "§ 21",
        "examples": [
            {
                "english": "Whence am I come, do you ask ?",
                "greek": "πόθεν ἥκω, ἔρει;",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He asked whence he was come.",
                "greek": "πόθεν ἥκοι, ἤρετο.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I am at a loss what to say.",
                "greek": "τί φῶ, ἀπορῶ.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He was at a loss what to do.",
                "greek": "τί δρῴη, ἠπόρει.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He asked if (whether) this was true.",
                "greek": "ἤρετο εἰ τοῦτ' ἀληθὲς εἴη.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 40,
        "page": 126,
        "category": "Conditional Sentences",
        "category_ref": "§ 22 ff.",
        "examples": [
            {
                "english": "If it thunders, it also lightens.",
                "greek": "εἰ βροντεῖ, καὶ ἀστράπτει.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "If it thundered, it also lightened.",
                "greek": "εἰ ἐβρόντησε, καὶ ἤστραψε.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "If we have anything, we will give it.",
                "greek": "ἐάν τι ἔχωμεν, δώσομεν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "If we should have anything, we would give it.",
                "greek": "εἴ τι ἔχοιμεν, διδοίημεν ἄν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "If he had anything, he would give it.",
                "greek": "εἴ τι εἶχον, ἐδίδου ἄν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "If he had had anything, he would have given it.",
                "greek": "εἴ τι ἔσχεν, ἔδωκεν ἄν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He said that if he had anything, he would give it.",
                "greek": "ἔφη εἴ τι ἔχοι διδόναι ἄν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He said that if he had had anything, he would have given it.",
                "greek": "ἔφη εἴ τι ἔσχεν δοῦναι ἄν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 41,
        "page": 126,
        "examples": [
            {
                "english": "Every one denied.",
                "greek": None,
                "literal_or_explanation": "No one said.",
                "section_ref": None
            },
            {
                "english": "No one either saw or heard.",
                "greek": "οὐδεὶς οὔτ' εἶδεν, οὔτ' ἤκουσεν",
                "literal_or_explanation": None,
                "section_ref": "§ 26"
            },
            {
                "english": "He went away that no one might either hear or see.",
                "greek": "ἀπῆλθεν ἵνα μηδεὶς μήτε ἴδοι μήτε ἀκούσαι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "No one ever saw him anywhere.",
                "greek": None,
                "literal_or_explanation": "No one never saw him nowhere.",
                "section_ref": None
            },
            {
                "english": "He who does not do.",
                "greek": "ὁ μὴ ποιῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "What is not honourable.",
                "greek": "τὰ μὴ καλά.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 42,
        "page": 126,
        "examples": [
            {
                "english": "This will not happen.",
                "greek": "οὐ μὴ γένηται τοῦτο",
                "literal_or_explanation": None,
                "section_ref": "§ 28"
            },
            {
                "english": "Don't talk.",
                "greek": "οὐ μὴ λαλήσεις;",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 43,
        "page": 126,
        "examples": [
            {
                "english": "Vereor ne morior.",
                "greek": "φοβοῦμαι μὴ θάνω.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Vereor ut morior.",
                "greek": "φοβοῦμαι μὴ οὐ θάνω.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 44,
        "page": 126,
        "examples": [
            {
                "english": "Clever at finding.",
                "greek": None,
                "literal_or_explanation": "Clever to find.",
                "section_ref": None
            },
            {
                "english": "I offer myself to be questioned.",
                "greek": None,
                "literal_or_explanation": "I offer myself to question (act.).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 45,
        "page": 126,
        "examples": [
            {
                "english": "Alexander said that he was the son of Zeus.",
                "greek": "Ἀλέξανδρος ἔφασκεν εἶναι Διὸς υἱός",
                "literal_or_explanation": None,
                "section_ref": "§ 31"
            },
            {
                "english": "They besought him to be zealous.",
                "greek": "ἐδέοντο αὐτοῦ εἶναι προθύμου.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "It is possible for me to become happy.",
                "greek": "ἔξεστί μοι γενέσθαι εὐδαίμονι.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 46,
        "page": 126,
        "examples": [
            {
                "english": "Nothing was done because he was not present.",
                "greek": "διὰ τὸ μὴ παρεῖναι ἐκεῖνον",
                "literal_or_explanation": "Nothing was done owing to the him not being present (διὰ τὸ μὴ παρεῖναι ἐκεῖνον).",
                "section_ref": None
            },
            {
                "english": "They live with a view to self-interest, because they are lovers of themselves.",
                "greek": "διὰ τὸ φίλαυτοι εἶναι",
                "literal_or_explanation": "They live towards the advantageous, owing to the being self-lovers (διὰ τὸ φίλαυτοι εἶναι).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 47,
        "page": "126-127",
        "examples": [
            {
                "english": "He went off with.",
                "greek": "λαβὼν ἀπῴχετο",
                "literal_or_explanation": "Having taken, he went off (λαβὼν ἀπῴχετο).",
                "section_ref": None
            },
            {
                "english": "After doing this, he went away.",
                "greek": "ταῦτα πράξας ἀπῴχετο",
                "literal_or_explanation": None,
                "section_ref": "§ 34"
            },
            {
                "english": "He who did this, went away. / The guilty person went away.",
                "greek": "ὁ ταῦτα πράξας, ἀπῴχετο.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 48,
        "page": 127,
        "examples": [
            {
                "english": "I am here to help you.",
                "greek": "πάρειμι ἐπικουρήσων",
                "literal_or_explanation": None,
                "section_ref": "§ 35"
            },
            {
                "english": "He sends men to do this.",
                "greek": "πέμπει ἄνδρας τοῦτο ποιήσοντας.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 49,
        "page": 127,
        "examples": [
            {
                "english": "He continues to do this.",
                "greek": None,
                "literal_or_explanation": "He continues doing this.",
                "section_ref": None
            },
            {
                "english": "He happened to be present.",
                "greek": None,
                "literal_or_explanation": "He happened being present.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 50,
        "page": 127,
        "examples": [
            {
                "english": "I do it unconsciously. / I do it secretly.",
                "greek": "λανθάνω ποιῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I arrived before them.",
                "greek": "ἔφθην ἀφικόμενος",
                "literal_or_explanation": "I was before them in arriving (ἔφθην ἀφικόμενος) (§ 35 (2)).",
                "section_ref": "§ 35 (2)"
            },
            {
                "english": "You cannot do it too soon.",
                "greek": "οὐκ ἂν φθάνοις ποιήσας.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Do it, and be quick.",
                "greek": "πρᾶττε ἀνύσας τι.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 51,
        "page": 127,
        "examples": [
            {
                "english": "I forgot that I had done this.",
                "greek": "ἐλαθόμην τοῦτο ποιήσας",
                "literal_or_explanation": "I forgot having done this (ἐλαθόμην τοῦτο ποιήσας).",
                "section_ref": None
            },
            {
                "english": "I knew that he was dead.",
                "greek": "ᾔδειν αὐτὸν τεθνηκότα",
                "literal_or_explanation": "I knew of him being dead (ᾔδειν αὐτὸν τεθνηκότα).",
                "section_ref": None
            },
            {
                "english": "They announced that he was dead.",
                "greek": "ἤγγειλαν αὐτὸν τεθνηκότα",
                "literal_or_explanation": "They announced him having died (ἤγγειλαν αὐτὸν τεθνηκότα).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 52,
        "page": 127,
        "examples": [
            {
                "english": "He was convicted of crime.",
                "greek": "ἀδικήσας",
                "literal_or_explanation": "He was convicted having done wrong (ἀδικήσας).",
                "section_ref": None
            },
            {
                "english": "He perceived that he had fallen into the ditch.",
                "greek": "ᾔσθετο εἰς τὴν τάφρον πεσών",
                "literal_or_explanation": "He perceived having fallen into the ditch (ᾔσθετο εἰς τὴν τάφρον πεσών, sensit medios delapsus in hostes).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 53,
        "page": 127,
        "examples": [
            {
                "english": "I am ashamed while I speak.",
                "greek": "αἰσχύνομαι λέγων",
                "literal_or_explanation": None,
                "section_ref": "§ 35 (3)"
            },
            {
                "english": "I am ashamed to speak.",
                "greek": "αἰσχύνομαι λέγειν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I obviously do.",
                "greek": "φαίνομαι ποιῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "I seem to do.",
                "greek": "φαίνομαι ποιεῖν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 54,
        "page": 127,
        "examples": [
            {
                "english": "It was clear that he did.",
                "greek": "δῆλος ἦν ποιῶν. / φανερὸς ἦν ποιῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 55,
        "page": 127,
        "examples": [
            {
                "english": "This being the case.",
                "greek": "τούτων οὕτως ἐχόντων",
                "literal_or_explanation": None,
                "section_ref": "§ 37"
            },
            {
                "english": "Without your orders.",
                "greek": "ὑμῶν μὴ κελευσάντων.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "When you ought —.",
                "greek": "δέον.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "When you can —.",
                "greek": "ἐξόν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 56,
        "page": 127,
        "examples": [
            {
                "english": "I have a little difficulty.",
                "greek": "σμικρόν τι ἀπορῶ",
                "literal_or_explanation": "I am at a loss in a little degree (σμικρόν τι ἀπορῶ).",
                "section_ref": None
            },
            {
                "english": "I make a moderate request of you.",
                "greek": "δέομαι μέτρια ὑμῶν.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 57,
        "page": 127,
        "examples": [
            {
                "english": "Many great sights.",
                "greek": None,
                "literal_or_explanation": "Many and great sights.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 58,
        "page": 127,
        "examples": [
            {
                "english": "What impudence !",
                "greek": None,
                "literal_or_explanation": "The impudence (gen.) (§ 41).",
                "section_ref": "§ 41"
            },
            {
                "english": "No Greek.",
                "greek": None,
                "literal_or_explanation": "No one of (the) Greeks.",
                "section_ref": None
            },
            {
                "english": "I gave you some money.",
                "greek": None,
                "literal_or_explanation": "I gave you of money.",
                "section_ref": None
            },
            {
                "english": "My property, unhappy me !",
                "greek": "τἀμὰ τοῦ κακοδαίμονος.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 59,
        "page": 127,
        "examples": [
            {
                "english": "It is not like an honest man to do such things.",
                "greek": None,
                "literal_or_explanation": "It is not of an honest (man) to do such things.",
                "section_ref": None
            },
            {
                "english": "In favour of the rich.",
                "greek": "πρὸς τῶν ἐχόντων.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 60,
        "page": 128,
        "examples": [
            {
                "english": "To indict a person for cowardice.",
                "greek": "γράφεσθαι τινα δειλίας",
                "literal_or_explanation": None,
                "section_ref": "§ 43 (4)"
            },
            {
                "english": "To be indicted for cowardice. / To be on one's trial for cowardice.",
                "greek": None,
                "literal_or_explanation": "To fly of cowardice.",
                "section_ref": None
            },
            {
                "english": "To charge a person with folly.",
                "greek": "κατηγορεῖν μωρίαν τινός.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 61,
        "page": 128,
        "examples": [
            {
                "english": "I have not practised for many days.",
                "greek": None,
                "literal_or_explanation": "I have not practised of many days (gen.).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 62,
        "page": 128,
        "examples": [
            {
                "english": "Too great for tears.",
                "greek": "μεῖζον ἢ κατὰ δάκρυα",
                "literal_or_explanation": None,
                "section_ref": "§ 46 (3)"
            },
            {
                "english": "Of superhuman size.",
                "greek": "μείζων ἢ κατ' ἄνθρωπον.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Too young to know.",
                "greek": "νεώτεροι ἢ ὥστε εἰδέναι.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 63,
        "page": 128,
        "examples": [
            {
                "english": "Greater than ever.",
                "greek": "αὐτοὶ ἑαυτῶν",
                "literal_or_explanation": "Greater themselves than themselves (αὐτοὶ ἑαυτῶν) (§ 47).",
                "section_ref": "§ 47"
            },
            {
                "english": "More honest than rich.",
                "greek": None,
                "literal_or_explanation": "More honest than more rich.",
                "section_ref": None
            },
            {
                "english": "He has a larger house than mine.",
                "greek": None,
                "literal_or_explanation": "He has a house larger than me.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 64,
        "page": 128,
        "examples": [
            {
                "english": "As — as possible.",
                "greek": "ὡς, ὅσος, with superlative; ὡς τάχιστα, ὅσοι πλεῖστοι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "More painful than any other.",
                "greek": None,
                "literal_or_explanation": "Most painful if any other (§ 48).",
                "section_ref": "§ 48"
            },
            {
                "english": "You have remarkably black hair.",
                "greek": None,
                "literal_or_explanation": "You have the hair black, if any other person (has).",
                "section_ref": None
            },
            {
                "english": "Fairer than any before.",
                "greek": None,
                "literal_or_explanation": "Fairest of all before.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 65,
        "page": 128,
        "examples": [
            {
                "english": "We have no ships.",
                "greek": None,
                "literal_or_explanation": "There are not ships to us.",
                "section_ref": None
            },
            {
                "english": "What have I to do with you ?",
                "greek": None,
                "literal_or_explanation": "What (is there) to me and to you ?",
                "section_ref": None
            }
        ]
    },
    {
        "id": 66,
        "page": 128,
        "examples": [
            {
                "english": "You act strangely in giving us nothing.",
                "greek": None,
                "literal_or_explanation": "You do a strange (thing), who give us nothing (§ 51).",
                "section_ref": "§ 51"
            },
            {
                "english": "They pitied the mother for being deprived of such children.",
                "greek": None,
                "literal_or_explanation": "They pitied the mother, of what children she had been deprived.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 67,
        "page": 128,
        "examples": [
            {
                "english": "I enjoy the goods I have.",
                "greek": "ἀπολαύω ὧν ἔχω ἀγαθῶν",
                "literal_or_explanation": "I enjoy of what goods I have (ἀπολαύω ὧν ἔχω ἀγαθῶν).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 68,
        "page": 128,
        "examples": [
            {
                "english": "Some say.",
                "greek": "ἔστιν οἳ λέγουσι",
                "literal_or_explanation": None,
                "section_ref": "§ 52"
            },
            {
                "english": "Sometimes.",
                "greek": "ἔστιν ὅτε.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Somewhere.",
                "greek": "ἔστιν ὅπου.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Is there any one who ?",
                "greek": "ἔστιν ὅστις;",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 69,
        "page": 128,
        "examples": [
            {
                "english": "All who do not say.",
                "greek": "ὅσοι μὴ λέγουσι.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "All who deny.",
                "greek": "ὅσοι οὐ φασί.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 70,
        "page": 128,
        "examples": [
            {
                "english": "I will tell you on condition that you will hold your tongue.",
                "greek": "λέξω σοι ἐφ' ᾧ σιγήσει; (or) ἐφ' ᾧ σιγῆσαι",
                "literal_or_explanation": "λέξω σοι ἐφ' ᾧ σιγήσει; (or) ἐφ' ᾧ σιγῆσαι (infinitive).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 71,
        "page": 128,
        "examples": [
            {
                "english": "No one who.",
                "greek": "οὐδεὶς ὅστις.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "No one whom.",
                "greek": "οὐδένα ὅντινα",
                "literal_or_explanation": None,
                "section_ref": "§ 53"
            },
            {
                "english": "Such a man as you.",
                "greek": "οἷος σὺ ἀνήρ.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "Of such a man as you.",
                "greek": "οἵου σοῦ ἀνδρός.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "He made astonishing progress.",
                "greek": "θαυμαστὸν ὅσον προὐχώρησε.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 72,
        "page": 128,
        "examples": [
            {
                "english": "What induced you to do this ?",
                "greek": "τί παθών / τί μαθών",
                "literal_or_explanation": "Having suffered what (τί παθών) — Having learnt what (τί μαθών) — did you do this ? (§ 55).",
                "section_ref": "§ 55"
            }
        ]
    },
    {
        "id": 73,
        "page": 128,
        "examples": [
            {
                "english": "I wonder that.",
                "greek": "εἰ",
                "literal_or_explanation": "I wonder if (εἰ).",
                "section_ref": None
            }
        ]
    },
    {
        "id": 74,
        "page": "128-129",
        "examples": [
            {
                "english": "What must they do to recover ?",
                "greek": None,
                "literal_or_explanation": "By doing what would they recover ?",
                "section_ref": None
            },
            {
                "english": "Who are these strangers whom I behold ?",
                "greek": "τίνας τούσδ' ὁρῶ ξένους ;",
                "literal_or_explanation": "What strangers do I behold here ? (τίνας τούσδ' ὁρῶ ξένους ;)",
                "section_ref": None
            }
        ]
    },
    {
        "id": 75,
        "page": 129,
        "examples": [
            {
                "english": "It is well.",
                "greek": None,
                "literal_or_explanation": "It has well.",
                "section_ref": None
            },
            {
                "english": "How are we off for money ?",
                "greek": "πῶς ἔχομεν χρημάτων ;",
                "literal_or_explanation": "How have we of money ? (πῶς ἔχομεν χρημάτων ;)",
                "section_ref": None
            }
        ]
    },
    {
        "id": 76,
        "page": 129,
        "examples": [
            {
                "english": "To be ashamed. / To be shameful.",
                "greek": None,
                "literal_or_explanation": "To have shame (§ 59).",
                "section_ref": "§ 59"
            },
            {
                "english": "To be blameable.",
                "greek": None,
                "literal_or_explanation": "To have blame.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 77,
        "page": 129,
        "examples": [
            {
                "english": "Why do you go on talking nonsense ?",
                "greek": "τί ληρεῖς ἔχων ;",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "To come with.",
                "greek": None,
                "literal_or_explanation": "To come having.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 78,
        "page": 129,
        "examples": [
            {
                "english": "To make much of.",
                "greek": "ποιεῖσθαι",
                "literal_or_explanation": "To make (ποιεῖσθαι) about much (§ 60).",
                "section_ref": "§ 60"
            },
            {
                "english": "To grieve.",
                "greek": "λύπην ποιεῖσθαι",
                "literal_or_explanation": "To make grief (λύπην ποιεῖσθαι).",
                "section_ref": None
            },
            {
                "english": "You are deservedly prosperous.",
                "greek": "καλῶς ποιοῦντες εὖ πράττετε.",
                "literal_or_explanation": None,
                "section_ref": None
            }
        ]
    },
    {
        "id": 79,
        "page": 129,
        "examples": [
            {
                "english": "It is not agreeable to me. / I am not pleased with.",
                "greek": None,
                "literal_or_explanation": "It is not to me wishing.",
                "section_ref": None
            }
        ]
    },
    {
        "id": 80,
        "page": 129,
        "examples": [
            {
                "english": "We ought to desire virtue.",
                "greek": "ἐπιθυμητέον ἐστὶ τῆς ἀρετῆς",
                "literal_or_explanation": None,
                "section_ref": "§ 63"
            },
            {
                "english": "We must persuade him.",
                "greek": "πειστέον ἐστὶν αὐτόν.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "We must obey him.",
                "greek": "πειστέον ἐστὶν αὐτῷ.",
                "literal_or_explanation": None,
                "section_ref": None
            },
            {
                "english": "We ought to set about the work.",
                "greek": None,
                "literal_or_explanation": "The work must be set about.",
                "section_ref": None
            }
        ]
    }
]

def normalize_obj(o):
    if isinstance(o, str):
        return unicodedata.normalize('NFC', o)
    elif isinstance(o, list):
        return [normalize_obj(x) for x in o]
    elif isinstance(o, dict):
        return {k: normalize_obj(v) for k, v in o.items()}
    return o

doc = {
    "title": "Table of Idioms",
    "author": "Thomas Kerchever Arnold",
    "work": "A Practical Introduction to Greek Prose Composition (Part I)",
    "pages": "123-129",
    "total_idioms": len(idioms_data),
    "idioms": normalize_obj(idioms_data)
}

output_path = Path("OCR/ArnoldGreekIdiom/arnold_greek_table_of_idioms.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

print(f"Successfully exported {len(idioms_data)} idioms to {output_path}")
