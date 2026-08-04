import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_NAMES = (
    "amazon-analyse",
    "category-selection",
    "keyword-research",
    "review-analysis",
    "product-research",
    "product-planning",
)
MIRRORS = (
    Path("skills"),
    Path(".claude/skills"),
    Path("openclaw/skills"),
)


class ReportNamingContractTests(unittest.TestCase):
    def test_all_commands_require_title_based_main_report_names(self):
        for skill_name in SKILL_NAMES:
            with self.subTest(skill=skill_name):
                text = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("{REPORT_TITLE}.md", text)
                self.assertNotIn("/report.md", text)

    def test_distributed_skill_copies_match(self):
        for skill_name in SKILL_NAMES:
            canonical = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for mirror in MIRRORS[1:]:
                with self.subTest(skill=skill_name, mirror=str(mirror)):
                    mirrored = (ROOT / mirror / skill_name / "SKILL.md").read_text(
                        encoding="utf-8"
                    )
                    self.assertEqual(canonical, mirrored)


if __name__ == "__main__":
    unittest.main()
