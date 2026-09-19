"""CrossMask: local-first, cross-file tabular data anonymization."""

from .engine import run_path, scan_path, verify_path

__all__ = ["run_path", "scan_path", "verify_path"]
__version__ = "0.1.0"
