"""Implements README.md file."""

import re
from pathlib import Path

from pyvelocity.configurations.files import ConfigurationFile
from pyvelocity.regex.github import RegexPatternsGitHub
from pyvelocity.regex.pypi import RegexPatternsPyPI
from pyvelocity.regex.qlty import RegexPatternsQlty
from pyvelocity.regex.shieldsio import RegexPatternsShieldsIO

WHERE_README_MD = "README.md"


class ReadMe(ConfigurationFile):
    """README.md file."""

    def __init__(self, path_readme: Path) -> None:
        super().__init__()
        self.content = path_readme.read_text(encoding="utf-8") if path_readme.exists() else ""

    @property
    def name(self) -> str:
        return WHERE_README_MD

    def has_badge(self, badge_text: str) -> bool:
        """Check if README contains a specific badge text."""
        return badge_text in self.content

    def has_test_badge(self) -> bool:
        """Check if README contains Test badge with strict markdown format."""
        return bool(re.compile(RegexPatternsGitHub.workflow_badge("Test")).search(self.content))

    def has_codeql_badge(self) -> bool:
        """Check if README contains CodeQL badge with strict markdown format."""
        return bool(re.compile(RegexPatternsGitHub.workflow_badge("CodeQL")).search(self.content))

    def has_coverage_badge(self) -> bool:
        """Check if README contains Code Coverage badge with strict markdown format."""
        return bool(re.compile(RegexPatternsQlty.coverage_badge()).search(self.content))

    def has_maintainability_badge(self) -> bool:
        """Check if README contains Maintainability badge with strict markdown format."""
        return bool(re.compile(RegexPatternsQlty.maintainability_badge()).search(self.content))

    def has_dependabot_badge(self) -> bool:
        """Check if README contains Dependabot badge with strict markdown format."""
        return bool(re.compile(RegexPatternsGitHub.dependabot_badge()).search(self.content))

    def has_python_versions_badge(self) -> bool:
        """Check if README contains Python versions badge with strict markdown format."""
        return bool(re.compile(RegexPatternsPyPI.python_versions_badge()).search(self.content))

    def has_social_badge(self) -> bool:
        """Check if README contains social/sharing badge with strict markdown format."""
        return bool(re.compile(RegexPatternsShieldsIO.x_badge()).search(self.content))
