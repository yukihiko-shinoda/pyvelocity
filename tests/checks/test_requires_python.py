"""Tests for requires_python check."""

import pytest

from pyvelocity.checks.requires_python import RequiresPython
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestRequiresPython:
    """Test for RequiresPython check."""

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
                ["pyproject_python_missing_requires.toml", "setup_success.cfg"],
                "requires-python field is missing in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_python_old_requires.toml", "setup_success.cfg"],
                'requires-python should support Python 3.13, but found ">=3.14" in [project] section of pyproject.toml',
                False,
            ),
            (
                ["pyproject_no_project.toml", "setup_success.cfg"],
                "Project section is missing in pyproject.toml",
                False,
            ),
        ],
    )
    def test_requires_python_check(expect_message: str, *, expect_is_ok: bool) -> None:
        """Tests requires-python check scenarios."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        requires_python_check = RequiresPython(configuration_files, configurations)
        result = requires_python_check.execute()
        assert result.message == expect_message
        assert result.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_pyproject_toml() -> None:
        """Tests case when no pyproject.toml exists."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        requires_python_check = RequiresPython(configuration_files, configurations)
        result = requires_python_check.execute()
        assert result.message == "pyproject.toml is required for requires-python check"
        assert result.is_ok is False


class TestRequiresPythonVersionLogic:
    """Test version parsing logic for RequiresPython."""

    @staticmethod
    def test_supports_latest_python_various_formats() -> None:
        """Test _supports_latest_python with various version formats."""
        requires_python_check = RequiresPython(None, None)  # type: ignore[arg-type]

        # Should support 3.13
        assert requires_python_check.supports_latest_python(">=3.8")
        assert requires_python_check.supports_latest_python(">=3.13")
        assert requires_python_check.supports_latest_python(">=3.8,<4.0")
        assert requires_python_check.supports_latest_python("~=3.13")
        assert requires_python_check.supports_latest_python("3.13")

        # Should not support 3.13
        assert not requires_python_check.supports_latest_python(">=3.14")
        assert not requires_python_check.supports_latest_python(">=3.8,<3.13")
        assert not requires_python_check.supports_latest_python("~=3.12")
        assert not requires_python_check.supports_latest_python("3.12")
        assert not requires_python_check.supports_latest_python("invalid")
