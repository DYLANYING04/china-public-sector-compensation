import importlib.util
import json
import struct
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
BENCHMARK_SCRIPT = ROOT / "scripts" / "benchmark_summary.py"
SPEC = importlib.util.spec_from_file_location("benchmark_summary", BENCHMARK_SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError(f"{path.name} is not a PNG with an IHDR chunk")
    return struct.unpack(">II", data[16:24])


class LaunchPackTests(unittest.TestCase):
    def test_benchmark_has_30_unique_valid_cases(self):
        cases = MODULE.load_cases(ROOT / "benchmark" / "cases.json")
        self.assertEqual(len(cases), 30)
        self.assertEqual(len({case["name"] for case in cases}), 30)
        self.assertEqual(
            Counter(case["state"] for case in cases),
            Counter({
                "FULL": 2,
                "STRUCTURE_ONLY": 24,
                "BUDGET_ONLY": 2,
                "NO_USABLE_DATA": 2,
            }),
        )
        self.assertEqual(sum(case["usable_wage_breakdown"] for case in cases), 28)

        beijing = next(case for case in cases if case["name"] == "北京市投资促进服务中心（本级）")
        self.assertEqual(beijing["year"], 2022)
        self.assertEqual(beijing["state"], "FULL")

    def test_launch_assets_are_nonblank_and_fixed_size(self):
        launch = ROOT / "assets" / "launch-preview.png"
        case_card = ROOT / "assets" / "yangling-case-card.png"
        beijing_card = ROOT / "assets" / "beijing-investment-center-case-card.png"
        self.assertGreater(launch.stat().st_size, 10_000)
        self.assertGreater(case_card.stat().st_size, 10_000)
        self.assertGreater(beijing_card.stat().st_size, 10_000)
        self.assertEqual(png_dimensions(launch), (1280, 640))
        self.assertEqual(png_dimensions(case_card), (1200, 630))
        self.assertEqual(png_dimensions(beijing_card), (1200, 630))

    def test_community_health_documents_exist(self):
        for path in (
            ROOT / "LICENSE",
            ROOT / "CONTRIBUTING.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "SECURITY.md",
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "request-institution.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "data-correction.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "portal-pattern.yml",
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())

    def test_readmes_promote_one_command_install_and_cases(self):
        for filename in ("README.md", "README.en.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn("npx skills add DYLANYING04/china-public-sector-compensation -g", text)
                self.assertIn("https://skills.sh/b/DYLANYING04/china-public-sector-compensation", text)
                self.assertIn("assets/launch-preview.png", text)
                self.assertIn("benchmark/README.md", text)


if __name__ == "__main__":
    unittest.main()
