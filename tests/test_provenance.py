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
        "provenance": {
            "entity_name": "示例事业单位",
            "route_basis": route_basis,
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


if __name__ == "__main__":
    unittest.main()
