"""Tests for typed check."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from pyvelocity.checks.typed import Typed
from pyvelocity.checks.typed import TypingClassifierValidator
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles

if TYPE_CHECKING:
    from pyvelocity.checks import Result
    from pyvelocity.configurations.files.py_project_toml import PyProjectToml


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
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration\n'
                'Missing "Typing :: Typed" classifier in pyproject.toml',
                False,
            ),
            # Wrong package-data config
            (
                ["pyproject_typed_wrong_package_data.toml", "setup_success.cfg"],
                ["testpackage"],
                ["testpackage/py.typed"],
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration\n'
                'Missing "Typing :: Typed" classifier in pyproject.toml',
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
            # Non-dict package-data config
            (
                ["pyproject_typed_non_dict_package_data.toml", "setup_success.cfg"],
                ["testpackage"],
                ["testpackage/py.typed"],
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration\n'
                'Missing "Typing :: Typed" classifier in pyproject.toml',
                False,
            ),
            # Missing typing classifier
            (
                ["pyproject_typed_missing_classifier.toml", "setup_success.cfg"],
                ["testpackage"],
                ["testpackage/py.typed"],
                'Missing "Typing :: Typed" classifier in pyproject.toml',
                False,
            ),
            # Both config and files missing
            (
                ["pyproject_typed_missing_package_data.toml", "setup_success.cfg"],
                ["testpackage"],
                [],
                'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration\n'
                "Missing py.typed files in package directories\n"
                'Missing "Typing :: Typed" classifier in pyproject.toml',
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
    def test_no_pyproject_toml(configuration_files: ConfigurationFiles, configurations: Configurations) -> None:
        """Tests case when no pyproject.toml exists."""
        with patch("pyvelocity.checks.typed.Setuptools") as mock_setuptools:
            mock_instance = mock_setuptools.return_value
            mock_instance.packages = ["testpackage"]
            typed_check = Typed(configuration_files, configurations)
            result = typed_check.execute()
            assert 'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration' in result.message
            assert result.is_ok is False

    @staticmethod
    def test_package_discovery_failure(
        configuration_files: ConfigurationFiles,
        configurations: Configurations,
    ) -> None:
        """Tests case when package discovery fails."""
        with patch("pyvelocity.checks.typed.Setuptools", side_effect=RuntimeError("Discovery failed")):
            typed_check = Typed(configuration_files, configurations)
            result = typed_check.execute()
            # Should fail due to package discovery failure
            assert "Missing py.typed files in package directories" in result.message
            assert result.is_ok is False


class TestTypingClassifierValidator:
    """Test the TypingClassifierValidator class using pytest fixtures."""

    @staticmethod
    def test_no_pyproject_toml() -> None:
        """Test validator when no pyproject.toml exists."""
        validator = TypingClassifierValidator(None)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_no_project_section(mock_py_project_toml_no_project: PyProjectToml) -> None:
        """Test validator when project section is missing."""
        validator = TypingClassifierValidator(mock_py_project_toml_no_project)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_no_classifiers_field(mock_py_project_toml_no_classifiers: PyProjectToml) -> None:
        """Test validator when classifiers field is missing."""
        validator = TypingClassifierValidator(mock_py_project_toml_no_classifiers)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_classifiers_value_none(mock_py_project_toml_no_classifiers: PyProjectToml) -> None:
        """Test validator when classifiers field has None value."""
        validator = TypingClassifierValidator(mock_py_project_toml_no_classifiers)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_classifiers_not_list(mock_py_project_toml_non_list_classifiers: PyProjectToml) -> None:
        """Test validator when classifiers is not a list."""
        validator = TypingClassifierValidator(mock_py_project_toml_non_list_classifiers)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_typing_classifier_present(mock_py_project_toml_with_typing_classifier: PyProjectToml) -> None:
        """Test validator when 'Typing :: Typed' classifier is present."""
        validator = TypingClassifierValidator(mock_py_project_toml_with_typing_classifier)
        assert validator.is_typing_classifier_present() is True

    @staticmethod
    def test_typing_classifier_missing(mock_py_project_toml_without_typing_classifier: PyProjectToml) -> None:
        """Test validator when 'Typing :: Typed' classifier is not present."""
        validator = TypingClassifierValidator(mock_py_project_toml_without_typing_classifier)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_empty_classifiers_list(mock_py_project_toml_empty_classifiers: PyProjectToml) -> None:
        """Test validator when classifiers list is empty."""
        validator = TypingClassifierValidator(mock_py_project_toml_empty_classifiers)
        assert validator.is_typing_classifier_present() is False

    @staticmethod
    def test_extract_classifiers_value_py_project_toml_none() -> None:
        """Test classifiers_value when py_project_toml is None."""
        validator = TypingClassifierValidator(None)
        assert validator.classifiers_value is None

    @staticmethod
    def test_extract_classifiers_value_project_none(mock_py_project_toml_no_project: PyProjectToml) -> None:
        """Test classifiers_value when project is None."""
        validator = TypingClassifierValidator(mock_py_project_toml_no_project)
        assert validator.classifiers_value is None

    @staticmethod
    def test_extract_classifiers_value_classifiers_none(mock_py_project_toml_no_classifiers: PyProjectToml) -> None:
        """Test classifiers_value when classifiers is None."""
        validator = TypingClassifierValidator(mock_py_project_toml_no_classifiers)
        assert validator.classifiers_value is None
