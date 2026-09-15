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
        result = calculate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
