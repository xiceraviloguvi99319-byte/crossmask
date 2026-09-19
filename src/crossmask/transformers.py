from __future__ import annotations

import base64
import hashlib
import hmac
import re
import unicodedata
from typing import Any

from .models import Rule


PREFIXES = {
    "person": "Person",
    "phone": "Phone",
    "national_id": "ID",
    "bank_card": "Card",
    "email": "Email",
    "address": "Address",
}


def normalize_value(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value)).strip().casefold()


def stable_token(value: Any, entity: str, secret: str, length: int = 10) -> str:
    payload = f"{entity}\0{normalize_value(value)}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).digest()
    return base64.b32encode(digest).decode("ascii").rstrip("=")[:length]


def fingerprint(value: Any) -> str:
    return hashlib.sha256(normalize_value(value).encode("utf-8")).hexdigest()[:12]


def _mask_phone(value: Any, token: str) -> str:
    text = str(value).strip()
    digits = re.sub(r"\D", "", text)
    if 7 <= len(digits) <= 15:
        return f"{digits[:3]}****{digits[-4:]}"
    return f"Phone-{token}"


def transform_value(value: Any, rule: Rule, secret: str) -> Any:
    if value is None or str(value).strip() == "":
        return value
    if isinstance(value, str) and value.startswith("="):
        return value
    if rule.action == "keep":
        return value
    if rule.action == "drop":
        return ""
    if rule.action == "redact":
        return "[REDACTED]"

    token = stable_token(value, rule.entity, secret)
    if rule.action == "mask" and rule.entity == "phone":
        return _mask_phone(value, token)
    if rule.entity == "email":
        return f"user-{token.casefold()}@example.invalid"
    prefix = PREFIXES.get(rule.entity, rule.entity.replace("_", " ").title().replace(" ", ""))
    return f"{prefix}-{token}"
