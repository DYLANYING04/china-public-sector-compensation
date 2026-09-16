#!/usr/bin/env python3
"""Recalculate the expert compensation formulas from sourced JSON inputs."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


TWO_THIRDS = Decimal(2) / Decimal(3)
ONE_HALF = Decimal(1) / Decimal(2)
WAN_TO_YUAN = Decimal(10000)
VALID_INPUT_UNITS = {"元", "万元", "亿元"}
VALID_BASES = {"预算", "决算"}
VALID_HEADCOUNT_BASES = {
    "annual_average_actual",
    "year_end_actual",
    "point_in_time_actual",
    "registered_total",
    "establishment",
    "other",
}
VALID_TRI_STATE = {"yes", "no", "unknown"}
VALID_RECONCILIATION_STATES = {"matched", "partial", "not_available"}
VALID_INFERENCE_CONFIDENCE = {"low", "medium", "high"}
ROUTE_ALIASES = {
    "local_public_institution": "local_two_thirds",
    "public_welfare_i": "direct_per_capita",
    "enterprise_managed": "leadership_skew_half",
}
ROUTE_FACTORS = {
    "local_two_thirds": TWO_THIRDS,
    "direct_per_capita": Decimal(1),
    "leadership_skew_half": ONE_HALF,
}
REQUIRED_SOURCE_FIELDS = {
    "title",
    "url",
    "publisher",
    "publication_date",
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
    if not result.is_finite():
        raise ValueError(f"{field} must be a finite number")
    if result < 0:
        raise ValueError(f"{field} must not be negative")
    return result


def positive_number(value: Any, field: str) -> Decimal:
    result = number(value, field)
    if result == 0:
        raise ValueError(f"{field} must be greater than zero")
    return result


def named_values(
    data: dict[str, Any], named_field: str, legacy_field: str
) -> tuple[dict[str, Decimal], bool]:
    """Return named amounts while keeping legacy list inputs compatible."""

    named = data.get(named_field)
    legacy = data.get(legacy_field)
    if named is not None and legacy is not None:
        raise ValueError(f"provide {named_field} or {legacy_field}, not both")
    if named is not None:
        if not isinstance(named, dict) or not named:
            raise ValueError(f"{named_field} must be a non-empty object")
        result: dict[str, Decimal] = {}
        for label, value in named.items():
            if not isinstance(label, str) or not label.strip():
                raise ValueError(f"{named_field} labels must be non-empty strings")
            result[label.strip()] = number(value, f"{named_field}.{label}")
        return result, False
    values = data.get(legacy_field)
    if not isinstance(values, list) or not values:
        raise ValueError(f"{named_field} must be a non-empty object")
    return {
        f"legacy_component_{index}": number(value, legacy_field)
        for index, value in enumerate(values, start=1)
    }, True


def optional_named_values(data: dict[str, Any], field: str) -> dict[str, Decimal]:
    values = data.get(field)
    if values is None:
        return {}
    if isinstance(values, list):
        return {
            f"legacy_award_{index}": number(value, field)
            for index, value in enumerate(values, start=1)
        }
    if not isinstance(values, dict):
        raise ValueError(f"{field} must be an object")
    result: dict[str, Decimal] = {}
    for label, value in values.items():
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"{field} labels must be non-empty strings")
        result[label.strip()] = number(value, f"{field}.{label}")
    return result


def expert_inferred_awards(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Read separately disclosed award-purpose judgments without treating them as facts."""

    values = data.get("expert_inferred_special_awards_wanyuan")
    if values is None:
        return {}
    if not isinstance(values, dict):
        raise ValueError("expert_inferred_special_awards_wanyuan must be an object")

    result: dict[str, dict[str, Any]] = {}
    for label, detail in values.items():
        if not isinstance(label, str) or not label.strip():
            raise ValueError(
                "expert_inferred_special_awards_wanyuan labels must be non-empty strings"
            )
        if not isinstance(detail, dict):
            raise ValueError(
                f"expert_inferred_special_awards_wanyuan.{label} must be an object"
            )
        amount = number(
            detail.get("amount"),
            f"expert_inferred_special_awards_wanyuan.{label}.amount",
        )
        basis = require_text(
            detail,
            "basis",
            f"expert_inferred_special_awards_wanyuan.{label}",
        )
        source_locator = require_text(
            detail,
            "source_locator",
            f"expert_inferred_special_awards_wanyuan.{label}",
        )
        confidence = require_text(
            detail,
            "confidence",
            f"expert_inferred_special_awards_wanyuan.{label}",
        )
        if confidence not in VALID_INFERENCE_CONFIDENCE:
            raise ValueError(
                f"expert_inferred_special_awards_wanyuan.{label}.confidence "
                "must be low, medium, or high"
            )
        result[label.strip()] = {
            "amount": amount,
            "basis": basis,
            "source_locator": source_locator,
            "confidence": confidence,
        }
    return result


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


def iso_date(container: dict[str, Any], field: str, prefix: str) -> date:
    value = require_text(container, field, prefix)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{prefix}.{field} must be an ISO date YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{prefix}.{field} must be an ISO date YYYY-MM-DD") from exc


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

    parsed_url = urlparse(source["url"])
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError(f"provenance.{field}.url must be an HTTP(S) URL")
    if (
        not isinstance(source["year"], int)
        or isinstance(source["year"], bool)
        or source["year"] != report_year
    ):
        raise ValueError(
            f"provenance.{field}.year must equal provenance.report_year"
        )
    published = iso_date(source, "publication_date", f"provenance.{field}")
    retrieved = iso_date(source, "retrieved_date", f"provenance.{field}")
    if retrieved < published:
        raise ValueError(
            f"provenance.{field}.retrieved_date must not precede publication_date"
        )
    return source


def validate_provenance(data: dict[str, Any]) -> dict[str, Any]:
    """Reject calculations whose amount and headcount evidence cannot be audited."""

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("provenance must be an object")

    entity_name = require_text(provenance, "entity_name")
    require_text(provenance, "official_institution_status")
    require_text(provenance, "analysis_route_reason")
    require_text(provenance, "compensation_scope")
    require_text(provenance, "funding_scope")
    employer_contributions = require_text(provenance, "includes_employer_contributions")
    if employer_contributions not in VALID_TRI_STATE:
        raise ValueError(
            "provenance.includes_employer_contributions must be yes, no, or unknown"
        )
    reconciliation = require_text(provenance, "row_reconciliation_status")
    if reconciliation not in VALID_RECONCILIATION_STATES:
        raise ValueError(
            "provenance.row_reconciliation_status must be matched, partial, or not_available"
        )
    require_text(provenance, "row_reconciliation_note")
    basis = require_text(provenance, "basis")
    if basis not in VALID_BASES:
        raise ValueError("provenance.basis must be 预算 or 决算")

    report_year = provenance.get("report_year")
    if not isinstance(report_year, int) or isinstance(report_year, bool):
        raise ValueError("provenance.report_year must be an integer")
    if not 2000 <= report_year <= 2100:
        raise ValueError("provenance.report_year must be between 2000 and 2100")

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
        route_input = data.get("route")
        expected_route = ROUTE_ALIASES.get(route_input, route_input)
        if expected_route not in ROUTE_FACTORS:
            raise ValueError(
                "route must be local_two_thirds, direct_per_capita, or leadership_skew_half"
            )
        if require_text(provenance, "analysis_route") != expected_route:
            raise ValueError(
                "provenance.analysis_route must match the canonical calculator route"
            )
        headcount_basis = require_text(provenance, "headcount_basis")
        if headcount_basis not in VALID_HEADCOUNT_BASES:
            raise ValueError(
                "provenance.headcount_basis must be annual_average_actual, "
                "year_end_actual, point_in_time_actual, registered_total, "
                "establishment, or other"
            )
        headcount_source = validate_source(
            provenance.get("headcount_source"), "headcount_source", report_year
        )
        require_text(headcount_source, "headcount_type", "provenance.headcount_source")
        if provenance.get("headcount_scope_match_confirmed") is not True:
            raise ValueError("provenance.headcount_scope_match_confirmed must be true")
        require_text(provenance, "headcount_scope_match_note")
    elif data.get("mode") == "structure":
        if require_text(provenance, "analysis_route") != "structure_ratio":
            raise ValueError(
                "provenance.analysis_route must be structure_ratio for structure mode"
            )
    else:
        raise ValueError("mode must be headcount or structure")

    return provenance


def calculate_headcount(data: dict[str, Any]) -> dict[str, Any]:
    component_values, used_legacy_components = named_values(
        data,
        "wage_components_wanyuan",
        "comparable_wage_components_wanyuan",
    )
    components = sum(component_values.values(), Decimal(0))
    headcount = positive_number(data.get("headcount"), "headcount")
    special_award_values = optional_named_values(data, "special_awards_wanyuan")
    special_awards = sum(special_award_values.values(), Decimal(0))
    inferred_awards = expert_inferred_awards(data)
    inferred_award_total = sum(
        (detail["amount"] for detail in inferred_awards.values()), Decimal(0)
    )
    all_special_awards = special_awards + inferred_award_total

    route_input = data.get("route")
    route = ROUTE_ALIASES.get(route_input, route_input)
    if route not in ROUTE_FACTORS:
        raise ValueError(
            "route must be local_two_thirds, direct_per_capita, or leadership_skew_half"
        )

    factor = ROUTE_FACTORS[route]
    average = components / headcount
    ordinary = average * factor
    award_per_person = special_awards / headcount

    return {
        "route": route,
        "wage_components_wanyuan": {
            label: rounded(value) for label, value in component_values.items()
        },
        "used_legacy_component_list": used_legacy_components,
        "comparable_total_wanyuan": rounded(components),
        "special_awards_wanyuan": {
            label: rounded(value) for label, value in special_award_values.items()
        },
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
        "expert_inferred_special_awards_wanyuan": {
            label: {
                "amount_wanyuan": rounded(detail["amount"]),
                "basis": detail["basis"],
                "source_locator": detail["source_locator"],
                "confidence": detail["confidence"],
                "classification": "专家判断，非来源明示",
            }
            for label, detail in inferred_awards.items()
        },
        "expert_inferred_special_awards_total_wanyuan": rounded(inferred_award_total),
        "expert_inferred_special_award_wanyuan_per_person": rounded(
            inferred_award_total / headcount
        ),
        "comparable_plus_all_special_awards_total_wanyuan": rounded(
            components + all_special_awards
        ),
        "organization_average_including_all_special_awards_wanyuan_per_person_year": rounded(
            (components + all_special_awards) / headcount
        ),
    }


def calculate_structure(data: dict[str, Any]) -> dict[str, Any]:
    basic = positive_number(data.get("basic_wage_wanyuan"), "basic_wage_wanyuan")
    variable_values, used_legacy_components = named_values(
        data,
        "variable_components_wanyuan",
        "bonus_performance_allowance_wanyuan",
    )
    variable = sum(variable_values.values(), Decimal(0))
    multiple = variable / basic

    if multiple >= Decimal(4):
        judgment = "待遇不错"
    elif multiple < Decimal(3):
        judgment = "待遇较差"
    else:
        judgment = "中间区间，继续看公积金和职业年金比值"

    result: dict[str, Any] = {
        "route": "structure_ratio",
        "basic_wage_wanyuan": rounded(basic),
        "variable_components_wanyuan": {
            label: rounded(value) for label, value in variable_values.items()
        },
        "used_legacy_component_list": used_legacy_components,
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
        result["interpretation"] = {
            "label": "作者方法下年度/月度等效估算",
            "not_take_home_pay": True,
            "compensation_scope": provenance["compensation_scope"],
            "funding_scope": provenance["funding_scope"],
            "includes_employer_contributions": provenance[
                "includes_employer_contributions"
            ],
        }
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
