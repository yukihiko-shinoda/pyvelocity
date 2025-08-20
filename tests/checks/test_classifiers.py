"""Tests for classifiers check."""

import pytest

from pyvelocity.checks.classifiers import Classifiers
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestClassifiers:
    """Test for Classifiers check."""

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize(
        ("files", "expect_message", "expect_is_ok"),
        [
            (
                ["pyproject_python_success.toml", "setup_success.cfg"],
                "",
                True,
            ),
            (
                ["pyproject_python_missing_classifiers.toml", "setup_success.cfg"],
                "classifiers field is missing in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_python_old_classifiers.toml", "setup_success.cfg"],
                "classifiers should include 'Programming Language :: Python :: 3.13' in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_no_project.toml", "setup_success.cfg"],
                "Project section is missing in pyproject.toml",
                False,
            ),
        ],
    )
    def test_classifiers_check(expect_message: str, *, expect_is_ok: bool) -> None:
        """Tests classifiers check scenarios."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        classifiers_check = Classifiers(configuration_files, configurations)
        result = classifiers_check.execute()
        assert result.message == expect_message
        assert result.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_pyproject_toml() -> None:
        """Tests case when no pyproject.toml exists."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        classifiers_check = Classifiers(configuration_files, configurations)
        result = classifiers_check.execute()
        assert result.message == "pyproject.toml is required for classifiers check"
        assert result.is_ok is False
