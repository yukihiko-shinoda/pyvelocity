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
                "Python version classifiers don't match requires-python '>=3.10': missing classifiers: "
                "Programming Language :: Python :: 3.12, Programming Language :: Python :: 3.13",
                False,
            ),
            (
                ["pyproject_classifier_mismatch_extra.toml", "setup_success.cfg"],
                "Python version classifiers don't match requires-python '>=3.11': extra classifiers: "
                "Programming Language :: Python :: 3.9, Programming Language :: Python :: 3.10",
                False,
            ),
            (
                ["pyproject_no_project.toml", "setup_success.cfg"],
                "Project section is missing in pyproject.toml",
                False,
            ),
            (
                ["pyproject_classifier_non_list.toml", "setup_success.cfg"],
                "classifiers field must be a list in [project] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_classifier_invalid_requires_python.toml", "setup_success.cfg"],
                "Could not parse requires-python 'invalid-version' in [project] section of pyproject.toml",
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
