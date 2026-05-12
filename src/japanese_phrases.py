import json
import hashlib
from typing import List, Dict


def load_phrases(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_three_phrases(phrases: List[Dict], date_key: str) -> List[Dict]:
    if not phrases:
        return []
    seed = int(hashlib.sha256(date_key.encode("utf-8")).hexdigest(), 16)
    start = seed % len(phrases)
    selected = []
    for i in range(3):
        selected.append(phrases[(start + i) % len(phrases)])
    return selected
