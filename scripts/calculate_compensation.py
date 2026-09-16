#!/usr/bin/env python3
"""Recalculate the expert compensation formulas from sourced JSON inputs."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any


TWO_THIRDS = Decimal(2) / Decimal(3)
ONE_HALF = Decimal(1) / Decimal(2)
WAN_TO_YUAN = Decimal(10000)
VALID_INPUT_UNITS = {"元", "万元", "亿元"}
VALID_BASES = {"预算", "决算"}
REQUIRED_SOURCE_FIELDS = {
    "title",
    "url",
    "publisher",
    "retrieved_date",
    "locator",
    "year",
    "entity_scope",
}


def number(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if result < 0:
        raise ValueError(f"{field} must not be negative")
    return result


def positive_number(value: Any, field: str) -> Decimal:
    result = number(value, field)
    if result == 0:
        raise ValueError(f"{field} must be greater than zero")
    return result


def sum_values(values: Any, field: str) -> Decimal:
    if not isinstance(values, list) or not values:
        raise ValueError(f"{field} must be a non-empty list")
    return sum((number(value, field) for value in values), Decimal(0))


def rounded(value: Decimal, places: str = "0.0001") -> str:
    return str(value.quantize(Decimal(places), rounding=ROUND_HALF_UP))


def annual_to_monthly_yuan(annual_wanyuan: Decimal) -> Decimal:
    return annual_wanyuan * WAN_TO_YUAN / Decimal(12)


def require_text(container: dict[str, Any], field: str, prefix: str = "") -> str:
    value = container.get(field)
    label = f"{prefix}.{field}" if prefix else field
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def validate_source(source: Any, field: str, report_year: int) -> dict[str, Any]:
    if not isinstance(source, dict):
        raise ValueError(f"provenance.{field} must be an object")

    missing = sorted(REQUIRED_SOURCE_FIELDS - source.keys())
    if missing:
        raise ValueError(
            f"provenance.{field} is missing required fields: {', '.join(missing)}"
        )

    for key in REQUIRED_SOURCE_FIELDS - {"year"}:
        require_text(source, key, f"provenance.{field}")

    if not source["url"].startswith(("https://", "http://")):
        raise ValueError(f"provenance.{field}.url must be an HTTP(S) URL")
    if source["year"] != report_year:
        raise ValueError(
            f"provenance.{field}.year must equal provenance.report_year"
        )
    return source


def validate_provenance(data: dict[str, Any]) -> dict[str, Any]:
    """Reject calculations whose amount and headcount evidence cannot be audited."""

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("provenance must be an object")

    entity_name = require_text(provenance, "entity_name")
    require_text(provenance, "route_basis")
    basis = require_text(provenance, "basis")
    if basis not in VALID_BASES:
        raise ValueError("provenance.basis must be 预算 or 决算")

    report_year = provenance.get("report_year")
    if not isinstance(report_year, int) or isinstance(report_year, bool):
        raise ValueError("provenance.report_year must be an integer")

    input_unit = require_text(provenance, "input_amount_unit")
    if input_unit not in VALID_INPUT_UNITS:
        raise ValueError("provenance.input_amount_unit must be 元, 万元, or 亿元")
    if require_text(provenance, "normalized_amount_unit") != "万元":
        raise ValueError("provenance.normalized_amount_unit must be 万元")
    require_text(provenance, "unit_conversion")

    amount_source = validate_source(
        provenance.get("amount_source"), "amount_source", report_year
    )
    if provenance.get("amount_scope_match_confirmed") is not True:
        raise ValueError("provenance.amount_scope_match_confirmed must be true")
    require_text(provenance, "amount_scope_match_note")

    if data.get("mode") == "headcount":
        headcount_source = validate_source(
            provenance.get("headcount_source"), "headcount_source", report_year
        )
        require_text(headcount_source, "headcount_type", "provenance.headcount_source")
        if provenance.get("headcount_scope_match_confirmed") is not True:
            raise ValueError("provenance.headcount_scope_match_confirmed must be true")
        require_text(provenance, "headcount_scope_match_note")

    return provenance


def calculate_headcount(data: dict[str, Any]) -> dict[str, Any]:
    components = sum_values(
        data.get("comparable_wage_components_wanyuan"),
        "comparable_wage_components_wanyuan",
    )
    headcount = positive_number(data.get("headcount"), "headcount")
    special_awards = sum(
        (
            number(value, "special_awards_wanyuan")
            for value in data.get("special_awards_wanyuan", [])
        ),
        Decimal(0),
    )

    route = data.get("route")
    factors = {
        "local_public_institution": TWO_THIRDS,
        "enterprise_managed": ONE_HALF,
        "public_welfare_i": Decimal(1),
    }
    if route not in factors:
        raise ValueError(
            "route must be local_public_institution, enterprise_managed, or public_welfare_i"
        )

    factor = factors[route]
    average = components / headcount
    ordinary = average * factor
    award_per_person = special_awards / headcount

    return {
        "route": route,
        "comparable_total_wanyuan": rounded(components),
        "special_awards_total_wanyuan": rounded(special_awards),
        "headcount": rounded(headcount, "0.0001"),
        "organization_average_wanyuan_per_person_year": rounded(average),
        "organization_average_yuan_per_person_month": rounded(
            annual_to_monthly_yuan(average), "0.01"
        ),
        "ordinary_factor": rounded(factor, "0.000001"),
        "ordinary_estimate_wanyuan_per_year": rounded(ordinary),
        "ordinary_estimate_yuan_per_month": rounded(
            annual_to_monthly_yuan(ordinary), "0.01"
        ),
        "special_award_wanyuan_per_person": rounded(award_per_person),
    }


def calculate_structure(data: dict[str, Any]) -> dict[str, Any]:
    basic = positive_number(data.get("basic_wage_wanyuan"), "basic_wage_wanyuan")
    variable = sum_values(
        data.get("bonus_performance_allowance_wanyuan"),
        "bonus_performance_allowance_wanyuan",
    )
    multiple = variable / basic

    if multiple >= Decimal(4):
        judgment = "待遇不错"
    elif multiple < Decimal(3):
        judgment = "待遇较差"
    else:
        judgment = "中间区间，继续看公积金和职业年金比值"

    result: dict[str, Any] = {
        "route": "public_welfare_ii",
        "basic_wage_wanyuan": rounded(basic),
        "bonus_performance_allowance_total_wanyuan": rounded(variable),
        "structure_multiple": rounded(multiple),
        "expert_judgment": judgment,
    }

    wage_base = data.get("ratio_wage_denominator_wanyuan")
    if wage_base is not None:
        denominator = positive_number(wage_base, "ratio_wage_denominator_wanyuan")
        for input_key, output_key in (
            ("housing_fund_wanyuan", "housing_fund_to_wage_ratio"),
            ("occupational_annuity_wanyuan", "occupational_annuity_to_wage_ratio"),
        ):
            if data.get(input_key) is not None:
                result[output_key] = rounded(number(data[input_key], input_key) / denominator)

    return result


def calculate(data: dict[str, Any]) -> dict[str, Any]:
    mode = data.get("mode")
    if mode == "headcount":
        return calculate_headcount(data)
    if mode == "structure":
        return calculate_structure(data)
    raise ValueError("mode must be headcount or structure")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate public-sector compensation using the expert method."
    )
    parser.add_argument("input", type=Path, help="Path to a UTF-8 JSON input file")
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        provenance = validate_provenance(data)
        result = calculate(data)
        result["provenance"] = provenance
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
