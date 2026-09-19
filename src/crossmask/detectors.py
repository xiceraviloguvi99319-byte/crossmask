from __future__ import annotations

import re
from collections import Counter
from typing import Any, Iterable


PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "national_id": re.compile(r"(?<!\d)\d{17}[\dXx](?!\w)"),
    "phone": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "bank_card": re.compile(r"(?<!\d)\d{12,19}(?!\d)"),
}


DEFAULT_ACTION = {
    "email": "alias",
    "national_id": "alias",
    "phone": "mask",
    "bank_card": "alias",
}


def detect_entities(value: Any) -> set[str]:
    if value is None:
        return set()
    text = str(value)
    entities = {name for name, pattern in PATTERNS.items() if pattern.search(text)}
    if text.casefold().endswith("@example.invalid"):
        entities.discard("email")
    if "national_id" in entities:
        entities.discard("bank_card")
    return entities


def infer_entity(values: Iterable[Any]) -> tuple[str | None, int]:
    counts: Counter[str] = Counter()
    for value in values:
        counts.update(detect_entities(value))
    if not counts:
        return None, 0
    entity, count = counts.most_common(1)[0]
    return entity, count
