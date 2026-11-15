"""Fail closed unless every training source permits open-source weight release."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from kabyle_ai.release_policy import validate_release_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="training-manifest.json")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read release manifest: {exc}", file=sys.stderr)
        return 1
    if not isinstance(manifest, dict):
        print("ERROR: release manifest must be a JSON object", file=sys.stderr)
        return 1

    errors = validate_release_manifest(manifest)
    if errors:
        for error in errors:
            print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    print("Release rights gate passed. Complete the remaining checklist before publishing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
