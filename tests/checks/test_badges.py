"""Tests for badges check."""

from pathlib import Path

import pytest

from pyvelocity.checks.badges import Badges
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestBadges:
    """Test for Badges check."""

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_readme_file() -> None:
        """Tests case when README.md doesn't exist."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        badges_check = Badges(configuration_files, configurations)
        result = badges_check.execute()
        assert result.message == "README.md file not found"
        assert result.is_ok is False

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_all_badges_present() -> None:
        """Tests case when all badges are present in README.md."""
        readme_content = """
        # Project
        [![Test](https://github.com/user/repo/workflows/Test/badge.svg)](https://github.com/user/repo/actions?query=workflow%3ATest)
        [![CodeQL](https://github.com/user/repo/workflows/CodeQL/badge.svg)](https://github.com/user/repo/actions?query=workflow%3ACodeQL)
        [![Code Coverage](https://qlty.sh/gh/user/repo/projects/project123/coverage.svg)](https://qlty.sh/gh/user/repo/projects/project123)
        [![Maintainability](https://qlty.sh/gh/user/repo/projects/project123/maintainability.svg)](https://qlty.sh/gh/user/repo/projects/project123)
        [![Dependabot](https://flat.badgen.net/github/dependabot/user/repo?icon=dependabot)](https://github.com/user/repo/security/dependabot)
        [![Python versions](https://img.shields.io/pypi/pyversions/package.svg)](https://pypi.org/project/package/)
        [![X URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fuser%2Frepo)](https://x.com/intent/post?text=Check%20out%20this%20project&url=https%3A%2F%2Fpypi.org%2Fproject%2Fpackage%2F&hashtags=python)
        """
        Path("README.md").write_text(readme_content, encoding="utf-8")

        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        badges_check = Badges(configuration_files, configurations)
        result = badges_check.execute()
        assert result.message == ""
        assert result.is_ok is True
