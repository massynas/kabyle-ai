"""Validate a native-speaker benchmark JSONL file."""
from __future__ import annotations

import argparse
import sys

from kabyle_ai.benchmark import validate_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="UTF-8 JSONL benchmark file")
    parser.add_argument(
        "--require-reviewed", action="store_true",
        help="fail if any record is not marked reviewed",
    )
    args = parser.parse_args()
    errors = validate_file(args.path, require_reviewed=args.require_reviewed)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Benchmark file is valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
