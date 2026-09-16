import unittest

from scripts.calculate_compensation import validate_provenance


def valid_input(mode="structure"):
    route_basis = (
        "地方事业单位；按作者的地方单位人数路线计算"
        if mode == "headcount"
        else "未取得同口径人数；按作者的工资结构路线计算"
    )
    data = {
        "mode": mode,
        "route": "local_two_thirds" if mode == "headcount" else None,
        "provenance": {
            "entity_name": "示例事业单位",
            "official_institution_status": "事业单位；未取得公益分类批复",
            "analysis_route_reason": route_basis,
            "analysis_route": "local_two_thirds" if mode == "headcount" else "structure_ratio",
            "compensation_scope": "财政工资福利支出人均口径",
            "funding_scope": "一般公共预算财政拨款基本支出",
            "includes_employer_contributions": "yes",
            "row_reconciliation_status": "matched",
            "row_reconciliation_note": "301xx明细加总与301合计一致",
            "report_year": 2024,
            "basis": "决算",
            "input_amount_unit": "元",
            "normalized_amount_unit": "万元",
            "unit_conversion": "原表金额除以10000",
            "amount_scope_match_confirmed": True,
            "amount_scope_match_note": "决算封面和表内单位名称均指向该单位本级",
            "amount_source": {
                "title": "示例事业单位2024年度单位决算",
                "url": "https://example.gov.cn/2024.pdf",
                "publisher": "示例市财政局",
                "publication_date": "2025-08-20",
                "retrieved_date": "2026-09-16",
                "locator": "公开06表，第12页",
                "year": 2024,
                "entity_scope": "示例事业单位",
            },
        },
    }
    if mode == "headcount":
        data["provenance"].update(
            {
                "headcount_scope_match_confirmed": True,
                "headcount_scope_match_note": "年度报告法人名称与决算单位一致",
                "headcount_basis": "year_end_actual",
                "headcount_source": {
                    "title": "示例事业单位2024年度报告",
                    "url": "https://example.gov.cn/2024-report.pdf",
                    "publisher": "示例事业单位",
                    "publication_date": "2025-03-31",
                    "retrieved_date": "2026-09-16",
                    "locator": "人员情况，第3页",
                    "year": 2024,
                    "entity_scope": "示例事业单位",
                    "headcount_type": "年末实有人数",
                },
            }
        )
    return data


class ProvenanceValidationTests(unittest.TestCase):
    def test_structure_source_passes(self):
        result = validate_provenance(valid_input())
        self.assertEqual(result["basis"], "决算")

    def test_headcount_sources_pass_when_scope_and_year_match(self):
        result = validate_provenance(valid_input("headcount"))
        self.assertTrue(result["headcount_scope_match_confirmed"])

    def test_mismatched_year_is_rejected(self):
        data = valid_input()
        data["provenance"]["amount_source"]["year"] = 2023
        with self.assertRaisesRegex(ValueError, "year must equal"):
            validate_provenance(data)

    def test_different_scope_label_is_allowed_after_explicit_confirmation(self):
        data = valid_input("headcount")
        data["provenance"]["headcount_source"]["entity_scope"] = "示例事业单位本级"
        result = validate_provenance(data)
        self.assertTrue(result["headcount_scope_match_confirmed"])

    def test_headcount_requires_explicit_scope_confirmation(self):
        data = valid_input("headcount")
        data["provenance"]["headcount_scope_match_confirmed"] = False
        with self.assertRaisesRegex(ValueError, "must be true"):
            validate_provenance(data)

    def test_amount_scope_requires_explicit_confirmation(self):
        data = valid_input()
        data["provenance"]["amount_scope_match_confirmed"] = False
        with self.assertRaisesRegex(ValueError, "must be true"):
            validate_provenance(data)

    def test_source_requires_publication_date(self):
        data = valid_input()
        del data["provenance"]["amount_source"]["publication_date"]
        with self.assertRaisesRegex(ValueError, "publication_date"):
            validate_provenance(data)

    def test_invalid_source_date_is_rejected(self):
        data = valid_input()
        data["provenance"]["amount_source"]["retrieved_date"] = "16-09-2026"
        with self.assertRaisesRegex(ValueError, "ISO date"):
            validate_provenance(data)

    def test_retrieval_before_publication_is_rejected(self):
        data = valid_input()
        data["provenance"]["amount_source"]["retrieved_date"] = "2025-01-01"
        with self.assertRaisesRegex(ValueError, "must not precede"):
            validate_provenance(data)

    def test_headcount_basis_is_required(self):
        data = valid_input("headcount")
        del data["provenance"]["headcount_basis"]
        with self.assertRaisesRegex(ValueError, "headcount_basis"):
            validate_provenance(data)

    def test_employer_contribution_scope_is_explicit(self):
        data = valid_input()
        data["provenance"]["includes_employer_contributions"] = "maybe"
        with self.assertRaisesRegex(ValueError, "yes, no, or unknown"):
            validate_provenance(data)

    def test_analysis_route_must_match_calculator_route(self):
        data = valid_input("headcount")
        data["provenance"]["analysis_route"] = "direct_per_capita"
        with self.assertRaisesRegex(ValueError, "must match"):
            validate_provenance(data)

    def test_reconciliation_status_is_controlled(self):
        data = valid_input()
        data["provenance"]["row_reconciliation_status"] = "looks fine"
        with self.assertRaisesRegex(ValueError, "matched, partial, or not_available"):
            validate_provenance(data)


if __name__ == "__main__":
    unittest.main()
