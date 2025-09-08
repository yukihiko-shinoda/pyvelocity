"""Tests for keywords check."""

import pytest

from pyvelocity.checks.keywords import Keywords
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestKeywords:
    """Test for Keywords check."""

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize(
        ("files", "expect_message", "expect_is_ok"),
        [
            (
                ["pyproject_success.toml", "setup_success.cfg"],
                "",
                True,
            ),
            (
                ["pyproject_keywords_missing.toml", "setup_success.cfg"],
                "keywords field is missing in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_keywords_empty.toml", "setup_success.cfg"],
                "At least one keyword must be defined in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_keywords_invalid_type.toml", "setup_success.cfg"],
                "keywords field must be a list in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_no_project.toml", "setup_success.cfg"],
                "Project section is missing in pyproject.toml",
                False,
            ),
        ],
    )
    def test_keywords_check(expect_message: str, *, expect_is_ok: bool) -> None:
        """Tests keywords check scenarios."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        keywords_check = Keywords(configuration_files, configurations)
        result = keywords_check.execute()
        assert result.message == expect_message
        assert result.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_pyproject_toml() -> None:
        """Tests case when no pyproject.toml exists."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        keywords_check = Keywords(configuration_files, configurations)
        result = keywords_check.execute()
        assert result.message == "pyproject.toml is required for keywords check"
        assert result.is_ok is False
