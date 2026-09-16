import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "calculate_compensation.py"
SPEC = importlib.util.spec_from_file_location("calculate_compensation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CalculationTests(unittest.TestCase):
    def test_local_screenshot_example(self):
        result = MODULE.calculate(
            {
                "mode": "headcount",
                "route": "local_two_thirds",
                "wage_components_wanyuan": {
                    "基本工资等可比项目": 503,
                    "奖金绩效津贴补贴": 1764,
                },
                "special_awards_wanyuan": {"招商引资任务奖": 196},
                "headcount": 88,
            }
        )
        self.assertEqual(result["organization_average_wanyuan_per_person_year"], "25.7614")
        self.assertEqual(result["ordinary_estimate_wanyuan_per_year"], "17.1742")
        self.assertEqual(result["ordinary_estimate_yuan_per_month"], "14311.87")
        self.assertEqual(result["special_award_wanyuan_per_person"], "2.2273")
        self.assertFalse(result["used_legacy_component_list"])
        self.assertEqual(result["route"], "local_two_thirds")

    def test_enterprise_managed_example(self):
        result = MODULE.calculate(
            {
                "mode": "headcount",
                "route": "leadership_skew_half",
                "wage_components_wanyuan": {"工资总额": 9600},
                "headcount": 200,
            }
        )
        self.assertEqual(result["organization_average_wanyuan_per_person_year"], "48.0000")
        self.assertEqual(result["ordinary_estimate_wanyuan_per_year"], "24.0000")
        self.assertEqual(result["ordinary_estimate_yuan_per_month"], "20000.00")

    def test_structure_thresholds_and_cross_checks(self):
        result = MODULE.calculate(
            {
                "mode": "structure",
                "basic_wage_wanyuan": 100,
                "variable_components_wanyuan": {
                    "奖金": 150,
                    "绩效工资": 200,
                    "津贴补贴": 50,
                },
                "ratio_wage_denominator_wanyuan": 500,
                "housing_fund_wanyuan": 60,
                "occupational_annuity_wanyuan": 40,
            }
        )
        self.assertEqual(result["structure_multiple"], "4.0000")
        self.assertEqual(result["expert_judgment"], "待遇不错")
        self.assertEqual(result["housing_fund_to_wage_ratio"], "0.1200")
        self.assertEqual(result["occupational_annuity_to_wage_ratio"], "0.0800")

    def test_rejects_zero_headcount(self):
        with self.assertRaises(ValueError):
            MODULE.calculate(
                {
                    "mode": "headcount",
                    "route": "local_two_thirds",
                    "wage_components_wanyuan": {"基本工资": 100},
                    "headcount": 0,
                }
            )

    def test_accepts_missing_special_awards_as_empty(self):
        result = MODULE.calculate(
            {
                "mode": "headcount",
                "route": "local_public_institution",
                "comparable_wage_components_wanyuan": [100],
                "headcount": 10,
                "special_awards_wanyuan": None,
            }
        )
        self.assertEqual(result["special_awards_total_wanyuan"], "0.0000")
        self.assertEqual(result["route"], "local_two_thirds")

    def test_rejects_non_finite_numbers(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            MODULE.calculate(
                {
                    "mode": "structure",
                    "basic_wage_wanyuan": "NaN",
                    "variable_components_wanyuan": {"奖金": 1},
                }
            )

    def test_rejects_named_and_legacy_components_together(self):
        with self.assertRaisesRegex(ValueError, "not both"):
            MODULE.calculate(
                {
                    "mode": "structure",
                    "basic_wage_wanyuan": 100,
                    "variable_components_wanyuan": {"奖金": 10},
                    "bonus_performance_allowance_wanyuan": [10],
                }
            )

    def test_named_components_remain_visible_in_result(self):
        result = MODULE.calculate(
            {
                "mode": "structure",
                "basic_wage_wanyuan": 100,
                "variable_components_wanyuan": {"奖金": 0, "绩效工资": 250},
            }
        )
        self.assertEqual(result["variable_components_wanyuan"]["奖金"], "0.0000")
        self.assertEqual(result["structure_multiple"], "2.5000")


if __name__ == "__main__":
    unittest.main()
