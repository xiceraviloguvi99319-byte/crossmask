# Architecture

CrossMask intentionally separates file handling, policy, transformation, and verification so that each part can be audited and extended independently.

## Components

1. `files.py` discovers and loads CSV/XLSX sources and writes sanitized copies.
2. `config.py` matches human-readable column rules from built-in or YAML configuration.
3. `transformers.py` applies deterministic HMAC aliases, masking, redaction, or removal.
4. `detectors.py` performs lightweight pattern checks without external services.
5. `engine.py` coordinates scan, transformation, and post-run verification.
6. `report.py` produces a raw-value-free Excel audit report.
7. `cli.py` exposes the scan, run, and verify workflows.

## Trust boundary

Input files, secrets, and transformed files remain on the operator's machine. The v0.1 core contains no network client. Future integrations that use external services must be optional, disabled by default, and documented with a clear data-flow warning.

## Extension direction

The planned detector interface will allow optional engines such as Microsoft Presidio while keeping the file orchestration and consistent alias layer independent.
