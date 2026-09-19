from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import yaml

from .models import Rule, Settings


VALID_ACTIONS = {"alias", "mask", "redact", "drop", "keep"}


DEFAULT_RULES = (
    Rule(("full_name", "fullname", "person_name", "姓名", "名字", "联系人"), "person", "alias"),
    Rule(("mobile", "phone", "telephone", "tel", "手机号", "手机号码", "电话", "联系方式"), "phone", "mask"),
    Rule(("id_card", "identity_number", "national_id", "身份证", "身份证号", "证件号码"), "national_id", "alias"),
    Rule(("bank_card", "card_number", "account_number", "银行卡", "银行卡号", "银行账号"), "bank_card", "alias"),
    Rule(("email", "e-mail", "邮箱", "电子邮件"), "email", "alias"),
    Rule(("address", "home_address", "住址", "地址", "居住地址"), "address", "alias"),
)


def normalize_header(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).strip().casefold()
    return re.sub(r"[\s\-_/\\.]+", "", text)


def match_rule(header: str, settings: Settings) -> Rule | None:
    normalized = normalize_header(header)
    for rule in settings.rules:
        for candidate in rule.columns:
            token = normalize_header(candidate)
            if normalized == token or (len(token) >= 3 and token in normalized):
                return rule
    return None


def _parse_rule(raw: object, index: int) -> Rule:
    if not isinstance(raw, dict):
        raise ValueError(f"Rule {index} must be a mapping")
    columns = raw.get("columns")
    entity = raw.get("entity")
    action = raw.get("action")
    if not isinstance(columns, list) or not columns or not all(isinstance(item, str) for item in columns):
        raise ValueError(f"Rule {index}.columns must be a non-empty list of strings")
    if not isinstance(entity, str) or not entity.strip():
        raise ValueError(f"Rule {index}.entity must be a non-empty string")
    if action not in VALID_ACTIONS:
        raise ValueError(f"Rule {index}.action must be one of: {', '.join(sorted(VALID_ACTIONS))}")
    return Rule(tuple(columns), entity.strip(), action)


def load_settings(path: str | Path | None = None) -> Settings:
    if path is None:
        return Settings(DEFAULT_RULES)

    config_path = Path(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("Configuration root must be a mapping")
    rules_raw = raw.get("rules", [])
    if not isinstance(rules_raw, list) or not rules_raw:
        raise ValueError("Configuration must contain at least one rule")
    rules = tuple(_parse_rule(item, index) for index, item in enumerate(rules_raw, start=1))
    secret_env = raw.get("secret_env", "CROSSMASK_SECRET")
    if not isinstance(secret_env, str) or not secret_env.strip():
        raise ValueError("secret_env must be a non-empty string")
    return Settings(rules=rules, secret_env=secret_env.strip())
