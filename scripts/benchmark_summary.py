#!/usr/bin/env python3
"""Validate and summarize the public-source launch benchmark."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


STATES = {"FULL", "STRUCTURE_ONLY", "BUDGET_ONLY", "NO_USABLE_DATA"}
REQUIRED_FIELDS = {
    "name",
    "year",
    "region",
    "portal",
    "source_url",
    "official_source_found",
    "usable_wage_breakdown",
    "state",
    "reason",
}


def load_cases(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("benchmark must be a non-empty JSON array")

    names: set[str] = set()
    for index, case in enumerate(data, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"case {index} must be an object")
        missing = REQUIRED_FIELDS - case.keys()
        if missing:
            raise ValueError(f"case {index} missing fields: {', '.join(sorted(missing))}")
        if case["name"] in names:
            raise ValueError(f"duplicate case name: {case['name']}")
        names.add(case["name"])
        if not isinstance(case["year"], int):
            raise ValueError(f"case {index} year must be an integer")
        if not isinstance(case["official_source_found"], bool):
            raise ValueError(f"case {index} official_source_found must be boolean")
        if not isinstance(case["usable_wage_breakdown"], bool):
            raise ValueError(f"case {index} usable_wage_breakdown must be boolean")
        if case["state"] not in STATES:
            raise ValueError(f"case {index} has unsupported state {case['state']}")
        parsed = urlparse(case["source_url"])
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"case {index} source_url must be an HTTPS URL")
        if case["state"] == "NO_USABLE_DATA" and case["usable_wage_breakdown"]:
            raise ValueError(f"case {index} cannot be NO_USABLE_DATA with a usable breakdown")
    return data


def percentage(count: int, total: int) -> str:
    return f"{count / total * 100:.1f}%"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to benchmark cases.json")
    args = parser.parse_args()

    try:
        cases = load_cases(args.input)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    total = len(cases)
    states = Counter(case["state"] for case in cases)
    sources = sum(case["official_source_found"] for case in cases)
    breakdowns = sum(case["usable_wage_breakdown"] for case in cases)

    print(f"Inputs: {total}")
    print(f"Official source found: {sources}/{total} ({percentage(sources, total)})")
    print(f"Usable wage breakdown: {breakdowns}/{total} ({percentage(breakdowns, total)})")
    for state in ("FULL", "STRUCTURE_ONLY", "BUDGET_ONLY", "NO_USABLE_DATA"):
        count = states[state]
        print(f"{state}: {count}/{total} ({percentage(count, total)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
