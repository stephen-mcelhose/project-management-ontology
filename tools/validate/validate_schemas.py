#!/usr/bin/env python3
"""
Validate all instructions.yaml files against tools/schemas/instructions-schema.json.

Exits 0 if every file is valid, 1 if any file fails.
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "tools" / "schemas" / "instructions-schema.json"
TEMPLATES_DIR = REPO_ROOT / "templates"


def load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


def validate_all(schema: dict) -> tuple[int, int]:
    validator = jsonschema.Draft7Validator(schema)
    files = sorted(TEMPLATES_DIR.rglob("instructions.yaml"))

    if not files:
        print("No instructions.yaml files found.", file=sys.stderr)
        sys.exit(1)

    passed = 0
    failed = 0

    for path in files:
        rel = path.relative_to(REPO_ROOT)
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            print(f"  ✗ {rel}  YAML parse error: {exc}", file=sys.stderr)
            failed += 1
            continue

        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))

        # ── Cross-reference checks ────────────────────────────────────────────
        # JSON Schema draft-07 cannot assert uniqueness across array items or
        # validate that one array's values exist in another array — both require
        # knowledge of the whole document at once. These checks fill that gap.
        # They are intentional behaviour of this tool, not schema limitations.
        cross_ref_errors: list[str] = []

        gate_ids = [g["id"] for g in doc.get("gates", []) if isinstance(g, dict) and "id" in g]

        # 1. Duplicate gate ids within the file.
        seen: set[str] = set()
        for gid in gate_ids:
            if gid in seen:
                cross_ref_errors.append(f"gates: duplicate id '{gid}'")
            seen.add(gid)

        # 2. Every required_gates entry must name a real gate id.
        required_gates = doc.get("completion", {}).get("required_gates", [])
        for ref in required_gates:
            if ref not in seen:
                cross_ref_errors.append(
                    f"completion.required_gates: '{ref}' does not match any gate id"
                )
        # ─────────────────────────────────────────────────────────────────────

        all_errors = bool(errors) or bool(cross_ref_errors)
        if all_errors:
            print(f"  ✗ {rel}", file=sys.stderr)
            for err in errors:
                path_str = " → ".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"      {path_str}: {err.message}", file=sys.stderr)
            for msg in cross_ref_errors:
                print(f"      {msg}", file=sys.stderr)
            failed += 1
        else:
            print(f"  ✓ {rel}")
            passed += 1

    return passed, failed


def main() -> None:
    schema = load_schema()

    files = sorted(TEMPLATES_DIR.rglob("instructions.yaml"))
    print(f"── Schema validation ({len(files)} files) ───────────────────────────")

    passed, failed = validate_all(schema)
    print(f"\n  {passed}/{passed + failed} passed\n")

    if failed:
        print(f"  {failed} file(s) failed validation. Fix before proceeding.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
