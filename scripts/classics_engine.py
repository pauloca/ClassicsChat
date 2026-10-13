import json
import re
import os
from typing import List, Dict, Any

class ClassicsKnowledgeEngine:
    def __init__(self, data_dir: str = "data/processed"):
        self.data_dir = data_dir
        self.latin_grammar: List[Dict[str, str]] = []
        self.greek_grammar: List[Dict[str, str]] = []
        self.latin_idioms: List[Dict[str, str]] = []
        self.greek_idioms: List[Dict[str, str]] = []
        self._load_knowledge_bases()

    def _load_knowledge_bases(self):
        # 1. Allen & Greenough Latin Grammar
        ag_path = os.path.join(self.data_dir, "sft_allen_greenough.jsonl")
        if os.path.exists(ag_path):
            with open(ag_path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line)
                    self.latin_grammar.append({
                        "topic": entry["instruction"].replace("According to Allen and Greenough's New Latin Grammar, explain the rule or usage concerning: ", ""),
                        "rule": entry["response"]
                    })

        # 2. Herbert Weir Smyth Greek Grammar
        smyth_path = os.path.join(self.data_dir, "sft_smyth_greek_grammar.jsonl")
        if os.path.exists(smyth_path):
            with open(smyth_path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line)
                    self.greek_grammar.append({
                        "topic": entry["instruction"].replace("According to Herbert Weir Smyth's Greek Grammar, explain the rule and usage regarding: ", ""),
                        "rule": entry["response"]
                    })

        # 3. Meissner Latin Phrase-Book
        meiss_path = os.path.join(self.data_dir, "sft_meissner_phrasebook.jsonl")
        if os.path.exists(meiss_path):
            with open(meiss_path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line)
                    # Extract pairs
                    inst = entry["instruction"]
                    resp = entry["response"]
                    if "express in Classical Latin:" in inst:
                        eng = inst.split('"', 1)[1].rsplit('"', 1)[0]
                        lat = resp.split("**", 1)[1].split("**")[0] if "**" in resp else resp
                        self.latin_idioms.append({"english": eng, "latin": lat, "source": "Meissner"})

        # 4. Completed Arnold Greek & Latin Idioms
        arnold_grk = "OCR/ArnoldGreekIdiom/arnold_greek_table_of_idioms_completed.json"
        if os.path.exists(arnold_grk):
            with open(arnold_grk, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("idioms", []):
                    for ex in item.get("examples", []):
                        if ex.get("english") and ex.get("greek"):
                            self.greek_idioms.append({
                                "english": ex["english"],
                                "greek": ex["greek"],
                                "literal": ex.get("literal_or_explanation", ""),
                                "source": "Arnold Greek Table of Idioms"
                            })

        arnold_lat = "OCR/ArnoldLatinIdiom/arnold_latin_table_of_idioms_completed.json"
        if os.path.exists(arnold_lat):
            with open(arnold_lat, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("idioms", []):
                    for ex in item.get("examples", []):
                        if ex.get("english") and ex.get("latin"):
                            self.latin_idioms.append({
                                "english": ex["english"],
                                "latin": ex["latin"],
                                "literal": ex.get("literal_or_explanation", ""),
                                "source": "Arnold Latin Table of Idioms"
                            })

    def search_latin_idiom(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        q_lower = query.lower()
        words = [w for w in re.findall(r"\w+", q_lower) if len(w) > 2]
        results = []
        for item in self.latin_idioms:
            eng_lower = item["english"].lower()
            lat_lower = item["latin"].lower()
            score = 0
            # Direct exact phrase match
            if q_lower in eng_lower or q_lower in lat_lower:
                score += 10
            # Keyword matches
            for w in words:
                if w in eng_lower:
                    score += 2
                if w in lat_lower:
                    score += 2
            if score > 0:
                results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def search_greek_idiom(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        q_lower = query.lower()
        words = [w for w in re.findall(r"\w+", q_lower) if len(w) > 2]
        results = []
        for item in self.greek_idioms:
            eng_lower = item["english"].lower()
            score = 0
            if q_lower in eng_lower:
                score += 10
            for w in words:
                if w in eng_lower:
                    score += 2
            if score > 0:
                results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def search_latin_grammar(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        q_lower = query.lower()
        words = [w for w in re.findall(r"\w+", q_lower) if len(w) > 2]
        results = []
        for item in self.latin_grammar:
            top_lower = item["topic"].lower()
            rule_lower = item["rule"].lower()
            score = 0
            if q_lower in top_lower:
                score += 15
            for w in words:
                if w in top_lower:
                    score += 4
                if w in rule_lower:
                    score += 1
            if score > 0:
                results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def search_greek_grammar(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        q_lower = query.lower()
        words = [w for w in re.findall(r"\w+", q_lower) if len(w) > 2]
        results = []
        for item in self.greek_grammar:
            top_lower = item["topic"].lower()
            rule_lower = item["rule"].lower()
            score = 0
            if q_lower in top_lower:
                score += 15
            for w in words:
                if w in top_lower:
                    score += 4
                if w in rule_lower:
                    score += 1
            if score > 0:
                results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

if __name__ == "__main__":
    engine = ClassicsKnowledgeEngine()
    print("Classics Knowledge Engine initialized!")
    print(f"Loaded {len(engine.latin_grammar)} Latin grammar rules.")
    print(f"Loaded {len(engine.greek_grammar)} Greek grammar rules.")
    print(f"Loaded {len(engine.latin_idioms)} Latin idioms.")
    print(f"Loaded {len(engine.greek_idioms)} Greek idioms.")
