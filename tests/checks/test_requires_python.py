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
                (
                    "requires-python should support Python 3.13, "
                    'but found ">=3.14" in [project] section of pyproject.toml'
                ),
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
    @pytest.mark.parametrize(
        ("requires_python_spec", "expected_supports_latest"),
        [
            # Should support 3.13
            (">=3.8", True),
            (">=3.13", True),
            (">=3.8,<4.0", True),
            ("~=3.13", True),
            ("3.13", True),
            # Should not support 3.13
            (">=3.14", False),
            (">=3.8,<3.13", False),
            ("~=3.12", False),
            ("3.12", False),
            ("invalid", False),
        ],
    )
    def test_supports_latest_python_various_formats(
        requires_python_spec: str,
        *,
        expected_supports_latest: bool,
    ) -> None:
        """Test supports_latest_python with various version formats."""
        requires_python_check = RequiresPython(None, None)  # type: ignore[arg-type]
        assert requires_python_check.supports_latest_python(requires_python_spec) is expected_supports_latest

    @staticmethod
    @pytest.mark.parametrize(
        ("requires_python_spec", "expected_supports_latest"),
        [
            # Test case triggering line 58: >= present but regex doesn't match in _check_greater_equal_support
            (">=invalid", False),
            # Test case triggering line 73: no < match found in _check_upper_bound_support
            # Creates a spec with < but invalid format that doesn't match regex
            (">=3.8,<invalid", True),
            # Test case triggering line 82: ~= present but regex doesn't match in _check_compatible_release_support
            ("~=invalid", False),
        ],
    )
    def test_edge_cases_through_public_method(
        requires_python_spec: str,
        *,
        expected_supports_latest: bool,
    ) -> None:
        """Test edge cases by calling public method that triggers protected method paths."""
        requires_python_check = RequiresPython(None, None)  # type: ignore[arg-type]
        result = requires_python_check.supports_latest_python(requires_python_spec)
        assert result is expected_supports_latest
