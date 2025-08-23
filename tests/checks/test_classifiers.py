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
                ["pyproject_classifier_missing_requires_python.toml", "setup_success.cfg"],
                "requires-python field is missing in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_classifier_mismatch_missing.toml", "setup_success.cfg"],
                "Python version classifiers don't match requires-python '>=3.10': missing classifiers: Programming Language :: Python :: 3.12, Programming Language :: Python :: 3.13",
                False,
            ),
            (
                ["pyproject_classifier_mismatch_extra.toml", "setup_success.cfg"],
                "Python version classifiers don't match requires-python '>=3.11': extra classifiers: Programming Language :: Python :: 3.9, Programming Language :: Python :: 3.10",
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


class TestClassifiersVersionLogic:
    """Test version parsing logic for Classifiers."""

    @staticmethod
    def test_get_supported_python_versions() -> None:
        """Test get_supported_python_versions with various requires-python formats."""
        classifiers_check = Classifiers(None, None)  # type: ignore[arg-type]

        # Test version requirement parsing for Python 3.10 and above
        versions = classifiers_check.get_supported_python_versions(">=3.10")
        expected = {"3.10", "3.11", "3.12", "3.13"}
        assert versions == expected

        # Test version range with upper bound
        versions = classifiers_check.get_supported_python_versions(">=3.8,<3.12")
        expected = {"3.8", "3.9", "3.10", "3.11"}
        assert versions == expected

        # Test minimum version requirement including older versions
        versions = classifiers_check.get_supported_python_versions(">=3.5")
        expected = {"3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"}
        assert versions == expected

        # Test compatible release operator
        versions = classifiers_check.get_supported_python_versions("~=3.11")
        expected = {"3.11"}
        assert versions == expected

        # Test exact version specification
        versions = classifiers_check.get_supported_python_versions("3.10")
        expected = {"3.10"}
        assert versions == expected

    @staticmethod
    def test_get_classifier_python_versions() -> None:
        """Test get_classifier_python_versions extracts correct versions."""
        classifiers_check = Classifiers(None, None)  # type: ignore[arg-type]

        classifiers = [
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Software Development",
        ]

        versions = classifiers_check.get_classifier_python_versions(classifiers)
        expected = {"3.10", "3.11", "3.12"}
        assert versions == expected

    @staticmethod
    def test_version_satisfies_requirement() -> None:
        """Test version_satisfies_requirement logic."""
        classifiers_check = Classifiers(None, None)  # type: ignore[arg-type]

        # Test minimum version requirements
        assert classifiers_check.version_satisfies_requirement("3.10", ">=3.8")
        assert classifiers_check.version_satisfies_requirement("3.8", ">=3.8")
        assert not classifiers_check.version_satisfies_requirement("3.7", ">=3.8")

        # Test version range requirements
        assert classifiers_check.version_satisfies_requirement("3.10", ">=3.8,<3.12")
        assert not classifiers_check.version_satisfies_requirement("3.12", ">=3.8,<3.12")
        assert not classifiers_check.version_satisfies_requirement("3.7", ">=3.8,<3.12")

        # Test compatible release operator
        assert classifiers_check.version_satisfies_requirement("3.11", "~=3.11")
        assert not classifiers_check.version_satisfies_requirement("3.12", "~=3.11")
        assert not classifiers_check.version_satisfies_requirement("3.10", "~=3.11")

        # Test exact version specification
        assert classifiers_check.version_satisfies_requirement("3.10", "3.10")
        assert not classifiers_check.version_satisfies_requirement("3.11", "3.10")
