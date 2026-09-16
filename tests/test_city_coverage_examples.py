import unittest

from scripts.calculate_compensation import calculate_headcount, calculate_structure


class CityCoverageExamplesTests(unittest.TestCase):
    CASES = (
        ("上海科技馆", "2144.89", ["261.69", "0", "8051.22"], "3.8757", "中间区间"),
        ("深圳市公共就业服务中心", "382.43", ["382.21", "0", "1194.54"], "4.1230", "待遇不错"),
        ("广州博物馆", "233.38", ["358.42", "385.78", "454.02"], "5.1342", "待遇不错"),
        ("武汉科学技术馆", "369.98", ["132.53", "0", "939.64"], "2.8979", "待遇较差"),
        ("杭州图书馆", "890.86", ["607.07", "488.40", "1893.84"], "3.3555", "中间区间"),
        ("烟台市公共就业和人才服务中心", "1461.64", ["1504.76", "268.50", "1229.81"], "2.0546", "待遇较差"),
        ("淄博市博物馆", "636.44", ["695.32", "234.69", "379.34"], "2.0573", "待遇较差"),
        ("合肥市科技馆（预算）", "141.81", ["18.84", "161.04", "122.45"], "2.1319", "待遇较差"),
        ("西安市科学技术馆（预算）", "99.04482", ["44.72134", "0", "234.57984"], "2.8199", "待遇较差"),
        ("陕西科学技术馆", "270.61", ["38.21", "0", "483.72"], "1.9287", "待遇较差"),
        ("漠河市融媒体中心", "261.11", ["278.80", "30.90", "0"], "1.1861", "待遇较差"),
    )

    def test_real_public_report_examples(self):
        for name, basic, variable, expected_multiple, judgment_fragment in self.CASES:
            with self.subTest(name=name):
                result = calculate_structure(
                    {
                        "basic_wage_wanyuan": basic,
                        "bonus_performance_allowance_wanyuan": variable,
                    }
                )
                self.assertEqual(result["structure_multiple"], expected_multiple)
                self.assertIn(judgment_fragment, result["expert_judgment"])

    def test_remote_county_unit_with_matched_staff_uses_two_thirds(self):
        result = calculate_headcount(
            {
                "route": "local_public_institution",
                "comparable_wage_components_wanyuan": [72.45, 8.99, 26.44, 82.57],
                "special_awards_wanyuan": [],
                "headcount": 11,
            }
        )
        self.assertEqual(result["comparable_total_wanyuan"], "190.4500")
        self.assertEqual(result["ordinary_estimate_wanyuan_per_year"], "11.5424")
        self.assertEqual(result["ordinary_estimate_yuan_per_month"], "9618.69")


if __name__ == "__main__":
    unittest.main()
