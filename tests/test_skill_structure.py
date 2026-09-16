import json
import re
import unittest
from pathlib import Path

from scripts.calculate_compensation import calculate, validate_provenance


ROOT = Path(__file__).parents[1]


class SkillStructureTests(unittest.TestCase):
    def test_skill_frontmatter_has_required_fields(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: china-public-sector-compensation$")
        self.assertRegex(frontmatter, r"(?m)^description: .+public-sector.+$")

    def test_local_markdown_links_exist(self):
        missing = []
        for markdown in ROOT.rglob("*.md"):
            if ".learnings" in markdown.parts:
                continue
            text = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://", "#")):
                    continue
                relative_target = target.split("#", 1)[0]
                if not (markdown.parent / relative_target).resolve().exists():
                    missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [], "Missing local links: " + "; ".join(missing))

    def test_public_docs_do_not_leak_machine_specific_user_paths(self):
        offenders = []
        for markdown in ROOT.rglob("*.md"):
            if ".learnings" in markdown.parts:
                continue
            if re.search(r"(?i)[A-Z]:\\Users\\[^\\]+", markdown.read_text(encoding="utf-8")):
                offenders.append(str(markdown.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_default_prompt_names_the_skill(self):
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$china-public-sector-compensation", text)

    def test_documented_calculator_examples_are_executable(self):
        text = (ROOT / "references" / "expert-method.md").read_text(encoding="utf-8")
        examples = re.findall(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
        self.assertEqual(len(examples), 2)
        for example in examples:
            data = json.loads(example)
            validate_provenance(data)
            calculate(data)


if __name__ == "__main__":
    unittest.main()
