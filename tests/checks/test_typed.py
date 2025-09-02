"""Tests for typed check."""

from pathlib import Path
from unittest.mock import patch

import pytest

from pyvelocity.checks import Result
from pyvelocity.checks.typed import Typed
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestTyped:
    """Test for Typed check."""

    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize(
        ("files", "packages", "py_typed_files", "expect_message", "expect_is_ok"),
        [
            # Success case: both config and files exist
            (
                ["pyproject_typed_success.toml", "setup_success.cfg"],
                ["testpackage"],
                ["testpackage/py.typed"],
                "",
                True,
            ),
            # Missing package-data config
            (
                ["pyproject_typed_missing_package_data.toml", "setup_success.cfg"],
                ["testpackage"],
                ["testpackage/py.typed"],
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration',
                False,
            ),
            # Wrong package-data config
            (
                ["pyproject_typed_wrong_package_data.toml", "setup_success.cfg"],
                ["testpackage"],
                ["testpackage/py.typed"],
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration',
                False,
            ),
            # Missing py.typed files
            (
                ["pyproject_typed_success.toml", "setup_success.cfg"],
                ["testpackage"],
                [],
                "Missing py.typed files in package directories",
                False,
            ),
            # Both config and files missing
            (
                ["pyproject_typed_missing_package_data.toml", "setup_success.cfg"],
                ["testpackage"],
                [],
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration\n'
                "Missing py.typed files in package directories",
                False,
            ),
        ],
    )
    def test_typed_check(
        self,
        expect_message: str,
        packages: list[str],
        py_typed_files: list[str],
        *,
        expect_is_ok: bool,
    ) -> None:
        """Tests typed check scenarios."""
        self._create_test_files(py_typed_files)

        try:
            result = self._execute_typed_check_with_mock(packages)
            assert result.message == expect_message
            assert result.is_ok == expect_is_ok
        finally:
            self._cleanup_test_files(py_typed_files)

    def _create_test_files(self, py_typed_files: list[str]) -> None:
        """Create py.typed test files."""
        for py_typed_file in py_typed_files:
            file_path = Path(py_typed_file)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("", encoding="utf-8")

    def _execute_typed_check_with_mock(self, packages: list[str]) -> Result:
        """Execute typed check with mocked packages."""
        with patch("pyvelocity.checks.typed.Setuptools") as mock_setuptools:
            mock_instance = mock_setuptools.return_value
            mock_instance.packages = packages
            configuration_files = ConfigurationFiles()
            configurations = Configurations(configuration_files)
            typed_check = Typed(configuration_files, configurations)
            return typed_check.execute()

    def _cleanup_test_files(self, py_typed_files: list[str]) -> None:
        """Clean up created test files."""
        for py_typed_file in py_typed_files:
            file_path = Path(py_typed_file)
            if file_path.exists():
                file_path.unlink()
                # Remove directory if empty
                if file_path.parent.exists() and not any(file_path.parent.iterdir()):
                    file_path.parent.rmdir()

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_pyproject_toml() -> None:
        """Tests case when no pyproject.toml exists."""
        with patch("pyvelocity.checks.typed.Setuptools") as mock_setuptools:
            mock_instance = mock_setuptools.return_value
            mock_instance.packages = ["testpackage"]
            configuration_files = ConfigurationFiles()
            configurations = Configurations(configuration_files)
            typed_check = Typed(configuration_files, configurations)
            result = typed_check.execute()
            assert 'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration' in result.message
            assert result.is_ok is False

    @staticmethod
    def test_package_discovery_failure() -> None:
        """Tests case when package discovery fails."""
        with patch("pyvelocity.checks.typed.Setuptools", side_effect=RuntimeError("Discovery failed")):
            configuration_files = ConfigurationFiles()
            configurations = Configurations(configuration_files)
            typed_check = Typed(configuration_files, configurations)
            result = typed_check.execute()
            # Should fail due to package discovery failure
            assert "Missing py.typed files in package directories" in result.message
            assert result.is_ok is False
