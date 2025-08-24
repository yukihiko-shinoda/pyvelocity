"""Test Project section functionality."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections.project import Project
from pyvelocity.configurations.files.sections.project import RequiresPythonAnalyzer


class TestProjectVersionLogic:
    """Test version parsing logic for Project."""

    @staticmethod
    @pytest.fixture
    def project(requires_python_value: str | None) -> Project:
        mock_where = Mock()
        mock_config_file = Mock()
        return Project(
            configuration_file=mock_config_file,
            readme=ConfigurationFileParameter(mock_where, "readme", None),
            requires_python=ConfigurationFileParameter(mock_where, "requires-python", requires_python_value),
            classifiers=ConfigurationFileParameter(mock_where, "classifiers", None),
        )

    @staticmethod
    @pytest.mark.parametrize(
        ("requires_python_value", "expected_versions"),
        [
            # Test version requirement parsing for Python 3.10 and above
            (">=3.10", {"3.10", "3.11", "3.12", "3.13"}),
            # Test version range with upper bound
            (">=3.8,<3.12", {"3.8", "3.9", "3.10", "3.11"}),
            # Test minimum version requirement including older versions
            (">=3.5", {"3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"}),
            # Test compatible release operator
            ("~=3.11", {"3.11"}),
            # Test exact version specification
            ("3.10", {"3.10"}),
        ],
    )
    def test_get_requires_python_supported_versions(project: Project, expected_versions: set[str]) -> None:
        """Test get_requires_python_supported_versions with various requires-python formats."""
        versions = project.get_requires_python_supported_versions(project)
        assert versions == expected_versions

    @staticmethod
    @pytest.mark.parametrize(
        ("version", "requirement", "expected"),
        [
            # Test minimum version requirements (>=)
            ("3.10", ">=3.8", True),
            ("3.8", ">=3.8", True),
            ("3.7", ">=3.8", False),
            ("3.11", ">=3.8", True),
            # Test version range requirements (>=,<)
            ("3.10", ">=3.8,<3.12", True),
            ("3.8", ">=3.8,<3.12", True),
            ("3.11", ">=3.8,<3.12", True),
            ("3.12", ">=3.8,<3.12", False),
            ("3.7", ">=3.8,<3.12", False),
            # Test compatible release requirements (~=)
            ("3.11", "~=3.11", True),
            ("3.10", "~=3.11", False),
            ("3.12", "~=3.11", False),
            # Test exact version requirements
            ("3.10", "3.10", True),
            ("3.11", "3.10", False),
            ("3.9", "3.10", False),
        ],
    )
    def test_version_satisfies_requirement(version: str, requirement: str, *, expected: bool) -> None:
        """Test version_satisfies_requirement logic with various scenarios."""
        analyzer = RequiresPythonAnalyzer(">=3.8")  # Analyzer instance for method access
        assert analyzer.version_satisfies_requirement(version, requirement) is expected

    @staticmethod
    @pytest.mark.parametrize(
        ("requires_python_value", "expected"),
        [
            (">=3.8", "3.8"),  # Test >=
            (">=3.6,<3.12", "3.6"),  # Test >=
            ("~=3.11", "3.11"),  # Test ~= compatible release
            ("3.10", "3.10"),  # Test exact version
            ("invalid", None),  # Test invalid format
            (None, None),  # Test None value
        ],
    )
    def test_requires_python_minimum_version(project: Project, expected: str) -> None:
        """Test requires_python_minimum_version extraction."""
        assert project.requires_python_minimum_version() == expected
