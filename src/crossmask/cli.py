from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .config import load_settings
from .engine import run_path, scan_path, verify_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crossmask",
        description="Consistently anonymize identities across linked Excel and CSV files.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Inspect files and suggest sensitive columns")
    scan.add_argument("input", type=Path)
    scan.add_argument("--config", type=Path)

    run = subparsers.add_parser("run", help="Create sanitized copies and an audit report")
    run.add_argument("input", type=Path)
    run.add_argument("--output", "-o", type=Path, required=True)
    run.add_argument("--config", type=Path)
    run.add_argument("--secret", help="Pseudonymization secret; prefer the CROSSMASK_SECRET environment variable")

    verify = subparsers.add_parser("verify", help="Check output files for common residual identifiers")
    verify.add_argument("input", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            settings = load_settings(args.config)
            items = scan_path(args.input, settings)
            if not items:
                print("No sensitive columns were identified.")
                return 0
            print("FILE\tSHEET\tCOLUMN\tENTITY\tACTION\tSOURCE\tNON_EMPTY\tPATTERN_MATCHES")
            for item in items:
                print(
                    f"{item.file}\t{item.sheet}\t{item.column}\t{item.entity}\t"
                    f"{item.suggested_action}\t{item.detection_source}\t"
                    f"{item.non_empty_cells}\t{item.pattern_matches}"
                )
            return 0

        if args.command == "run":
            settings = load_settings(args.config)
            secret = args.secret or os.getenv(settings.secret_env)
            if not secret:
                parser.error(f"Provide --secret or set the {settings.secret_env} environment variable")
            result = run_path(args.input, args.output, secret, settings)
            changed = sum(item.cells_changed for item in result.transformations)
            print(f"Processed {len(result.processed_files)} file(s); transformed {changed} cell(s).")
            print(f"Report: {result.report_path}")
            if result.verification_findings:
                print(f"Warning: {len(result.verification_findings)} residual finding(s) require review.")
                return 2
            print("Verification passed: no common raw identifier patterns found.")
            return 0

        findings = verify_path(args.input)
        if not findings:
            print("Verification passed: no common raw identifier patterns found.")
            return 0
        print("FILE\tSHEET\tROW\tCOLUMN\tENTITY\tFINGERPRINT")
        for item in findings:
            print(f"{item.file}\t{item.sheet}\t{item.row}\t{item.column}\t{item.entity}\t{item.fingerprint}")
        return 2
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
