# CrossMask

[![Tests](https://github.com/xiceraviloguvi99319-byte/crossmask/actions/workflows/test.yml/badge.svg)](https://github.com/xiceraviloguvi99319-byte/crossmask/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)

**Local-first, consistent pseudonymization for linked Excel and CSV files.**

[中文说明](README_zh.md)

CrossMask creates shareable copies of tabular datasets while preserving useful joins. If the same identity appears in different files or worksheets, the same secret produces the same pseudonym. Raw cell values stay on the local machine, and the generated audit report contains fingerprints and counts instead of source values.

> Status: v0.1.0 alpha. Review every output before sharing it. Automated de-identification cannot guarantee that a dataset is anonymous.

## Why CrossMask?

Removing a name from one spreadsheet is easy. Safely preparing a folder of linked spreadsheets is harder: inconsistent replacements break joins, copying mappings into reports leaks data, and overlooked identifiers remain in secondary worksheets.

CrossMask focuses on that workflow:

- processes `.xlsx` and `.csv` files in one run;
- applies deterministic HMAC-based aliases across files and sheets;
- recognizes common English and Chinese column names;
- supports person names, phone numbers, national IDs, bank cards, email addresses, and addresses;
- produces sanitized copies plus an Excel audit report;
- verifies outputs for common residual identifier patterns;
- never requires a network connection.

## Quick start

```bash
git clone https://github.com/xiceraviloguvi99319-byte/crossmask.git
cd crossmask
python -m venv .venv
```

Activate the environment, then install the project:

```bash
python -m pip install -e .
```

Scan the synthetic examples:

```bash
crossmask scan examples/input
```

Create sanitized copies and an audit report:

```bash
crossmask run examples/input --output demo-output --secret "replace-this-demo-secret"
```

Verify the output again:

```bash
crossmask verify demo-output
```

For normal use, keep the secret out of shell history:

```bash
export CROSSMASK_SECRET="a-long-random-secret-kept-out-of-git"
crossmask run ./input --output ./safe-output
```

Use the same secret when stable pseudonyms must remain consistent across separate runs. Never commit the secret or a reversible mapping table.

## Output

Given `people.csv` and `orders.xlsx`, CrossMask creates:

```text
safe-output/
├── people_sanitized.csv
├── orders_sanitized.xlsx
└── crossmask_privacy_report.xlsx
```

The report contains:

- a processing summary;
- transformation counts by file, sheet, and column;
- residual findings with row positions and one-way fingerprints;
- no copied raw values.

## Configuration

The built-in rules are intentionally small and auditable. Copy `crossmask.example.yaml`, adjust the column aliases, and pass it with `--config`:

```bash
crossmask run ./input \
  --output ./safe-output \
  --config crossmask.example.yaml
```

Supported actions are:

| Action | Behavior |
| --- | --- |
| `alias` | Replace with a deterministic HMAC-based token |
| `mask` | Preserve a small, non-sensitive portion where supported |
| `redact` | Replace with `[REDACTED]` |
| `drop` | Replace with an empty value |
| `keep` | Leave the value unchanged |

## Security model

- Processing is local and offline.
- Pseudonyms are keyed with HMAC-SHA-256.
- Reports do not include raw cell values.
- Example files contain synthetic identities only.
- The secret determines alias consistency and must not be committed.

See [Privacy model](docs/privacy-model.md) and [Security policy](SECURITY.md) before using CrossMask with sensitive data.

## Current limitations

- v0.1 rebuilds workbooks from cell values; advanced Excel formatting, macros, comments, and charts are not preserved.
- Header-based rules need customization for domain-specific schemas.
- Verification recognizes common patterns but cannot prove that an output is anonymous.
- Formulas are retained as formulas and are not rewritten.
- CrossMask does not yet implement statistical privacy models such as k-anonymity or differential privacy.

## Roadmap

- preserve workbook formatting while transforming cell values;
- optional Microsoft Presidio detector plugin;
- encrypted local mapping vault for approved reversible workflows;
- schema-only rule suggestions without sending raw cells;
- local graphical interface;
- configurable risk scoring and data-quality checks.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Contributions and reproducible bug reports are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
