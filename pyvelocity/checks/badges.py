"""Implements badges check."""

from pathlib import Path

from pyvelocity.checks import Check
from pyvelocity.checks import Result
from pyvelocity.configurations.files.readme import ReadMe


class Badges(Check):
    """Checks that README.md contains expected badges."""

    ID = "badges"

    def execute(self) -> Result:
        readme_path = Path("README.md")
        if not readme_path.exists():
            return Result(self.ID, is_ok=False, message="README.md file not found")

        readme = ReadMe(readme_path)
        missing_badges = self._get_missing_badges(readme)

        if missing_badges:
            message = f"README.md is missing the following badges: {', '.join(missing_badges)}"
            return Result(self.ID, is_ok=False, message=message)

        return Result(self.ID, is_ok=True, message="")

    def _get_missing_badges(self, readme: ReadMe) -> list[str]:
        expected_badges = [
            ("Test badge", readme.has_test_badge()),
            ("CodeQL badge", readme.has_codeql_badge()),
            ("Code Coverage badge", readme.has_coverage_badge()),
            ("Maintainability badge", readme.has_maintainability_badge()),
            ("Dependabot badge", readme.has_dependabot_badge()),
            ("Python versions badge", readme.has_python_versions_badge()),
            ("Social badge", readme.has_social_badge()),
        ]

        missing_badges = []
        for badge_name, has_badge in expected_badges:
            if not has_badge:
                missing_badges.append(badge_name)

        return missing_badges
