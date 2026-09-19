from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Rule:
    columns: tuple[str, ...]
    entity: str
    action: str


@dataclass(frozen=True)
class Settings:
    rules: tuple[Rule, ...]
    secret_env: str = "CROSSMASK_SECRET"


@dataclass
class Table:
    name: str
    headers: list[str]
    rows: list[list[Any]]


@dataclass(frozen=True)
class ScanItem:
    file: str
    sheet: str
    column: str
    entity: str
    suggested_action: str
    detection_source: str
    non_empty_cells: int
    pattern_matches: int


@dataclass
class TransformationStat:
    file: str
    sheet: str
    column: str
    entity: str
    action: str
    cells_changed: int = 0


@dataclass(frozen=True)
class VerificationFinding:
    file: str
    sheet: str
    row: int
    column: str
    entity: str
    fingerprint: str


@dataclass
class RunResult:
    output_dir: Path
    report_path: Path
    processed_files: list[Path] = field(default_factory=list)
    transformations: list[TransformationStat] = field(default_factory=list)
    verification_findings: list[VerificationFinding] = field(default_factory=list)
