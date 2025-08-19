"""Tests for readme check."""

import pytest

from pyvelocity.checks.readme import Readme
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestReadme:
    """Test for Readme check."""

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
                ["pyproject_readme_missing.toml", "setup_success.cfg"],
                "readme field is missing in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_readme_wrong.toml", "setup_success.cfg"],
                'readme should be "README.md", but found "README.rst" in [project] section of pyproject.toml',
                False,
            ),
            (
                ["pyproject_no_project.toml", "setup_success.cfg"],
                "Project section is missing in pyproject.toml",
                False,
            ),
        ],
    )
    def test_readme_check(expect_message: str, *, expect_is_ok: bool) -> None:
        """Tests readme check scenarios."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        readme_check = Readme(configuration_files, configurations)
        result = readme_check.execute()
        assert result.message == expect_message
        assert result.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_pyproject_toml() -> None:
        """Tests case when no pyproject.toml exists."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        readme_check = Readme(configuration_files, configurations)
        result = readme_check.execute()
        assert result.message == "pyproject.toml is required for readme check"
        assert result.is_ok is False
