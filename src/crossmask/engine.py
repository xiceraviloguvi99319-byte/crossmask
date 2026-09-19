from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .config import load_settings, match_rule
from .detectors import DEFAULT_ACTION, detect_entities, infer_entity
from .files import iter_supported_files, load_tables, write_tables
from .models import (
    RunResult,
    ScanItem,
    Settings,
    TransformationStat,
    VerificationFinding,
)
from .report import write_report
from .transformers import fingerprint, transform_value


def _column_values(rows: Iterable[list[object]], index: int) -> list[object]:
    return [row[index] for row in rows if index < len(row) and row[index] not in (None, "")]


def scan_path(source: str | Path, settings: Settings | None = None) -> list[ScanItem]:
    settings = settings or load_settings()
    findings: list[ScanItem] = []
    root = Path(source)
    for path in iter_supported_files(root):
        display_name = str(path.relative_to(root)) if root.is_dir() else path.name
        for table in load_tables(path):
            for index, header in enumerate(table.headers):
                values = _column_values(table.rows, index)
                rule = match_rule(header, settings)
                inferred_entity, pattern_count = infer_entity(values)
                if rule is None and inferred_entity is None:
                    continue
                entity = rule.entity if rule else str(inferred_entity)
                action = rule.action if rule else DEFAULT_ACTION[entity]
                findings.append(
                    ScanItem(
                        file=display_name,
                        sheet=table.name,
                        column=header,
                        entity=entity,
                        suggested_action=action,
                        detection_source="header" if rule else "value pattern",
                        non_empty_cells=len(values),
                        pattern_matches=pattern_count,
                    )
                )
    return findings


def verify_path(source: str | Path) -> list[VerificationFinding]:
    findings: list[VerificationFinding] = []
    root = Path(source)
    for path in iter_supported_files(root):
        if path.name == "crossmask_privacy_report.xlsx":
            continue
        display_name = str(path.relative_to(root)) if root.is_dir() else path.name
        for table in load_tables(path):
            for row_number, row in enumerate(table.rows, start=2):
                for index, value in enumerate(row):
                    for entity in sorted(detect_entities(value)):
                        column = table.headers[index] if index < len(table.headers) else f"column_{index + 1}"
                        findings.append(
                            VerificationFinding(
                                file=display_name,
                                sheet=table.name,
                                row=row_number,
                                column=column,
                                entity=entity,
                                fingerprint=fingerprint(value),
                            )
                        )
    return findings


def run_path(
    source: str | Path,
    output_dir: str | Path,
    secret: str,
    settings: Settings | None = None,
) -> RunResult:
    if len(secret) < 12:
        raise ValueError("Secret must be at least 12 characters long")
    settings = settings or load_settings()
    root = Path(source)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    result = RunResult(output_dir=output, report_path=output / "crossmask_privacy_report.xlsx")

    for path in iter_supported_files(root):
        relative = path.relative_to(root) if root.is_dir() else Path(path.name)
        destination = output / relative.parent / f"{path.stem}_sanitized{path.suffix.casefold()}"
        tables = load_tables(path)
        stats: dict[tuple[str, str, str, str, str], int] = defaultdict(int)

        for table in tables:
            rules_by_index = {index: match_rule(header, settings) for index, header in enumerate(table.headers)}
            for row in table.rows:
                for index, rule in rules_by_index.items():
                    if rule is None or index >= len(row) or row[index] in (None, ""):
                        continue
                    original = row[index]
                    transformed = transform_value(original, rule, secret)
                    row[index] = transformed
                    if transformed != original:
                        key = (str(relative), table.name, table.headers[index], rule.entity, rule.action)
                        stats[key] += 1

        write_tables(path, tables, destination)
        result.processed_files.append(destination)
        result.transformations.extend(
            TransformationStat(file=file, sheet=sheet, column=column, entity=entity, action=action, cells_changed=count)
            for (file, sheet, column, entity, action), count in sorted(stats.items())
        )

    result.verification_findings = verify_path(output)
    write_report(result)
    return result
