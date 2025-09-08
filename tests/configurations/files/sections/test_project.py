"""Test Project section functionality."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections import WhereToolDefault
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
            keywords=ConfigurationFileParameter(mock_where, "keywords", None),
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


class TestRequiresPythonAnalyzer:
    """Test internal analyzer logic for edge cases."""

    @staticmethod
    def test_handle_equals_or_greater_than_no_match() -> None:
        """Test handle_equals_or_greater_than when no match found (line 36)."""
        analyzer = RequiresPythonAnalyzer("invalid-spec")
        result = analyzer.handle_equals_or_greater_than()
        assert result is None

    @staticmethod
    def test_handle_same_major_version_no_match() -> None:
        """Test handle_same_major_version when no match found (line 43)."""
        analyzer = RequiresPythonAnalyzer(">=3.8")
        result = analyzer.handle_same_major_version()
        assert result is None

    @staticmethod
    def test_handle_exact_version_specifications_no_match() -> None:
        """Test handle_exact_version_specifications when no match found (line 56)."""
        analyzer = RequiresPythonAnalyzer(">=3.8")
        result = analyzer.handle_exact_version_specifications()
        assert result is None

    @staticmethod
    def test_version_satisfies_requirement_no_ge_pattern() -> None:
        """Test version_satisfies_requirement when >= path has no regex match (line 97)."""
        analyzer = RequiresPythonAnalyzer("invalid")
        # This triggers line 97: no >= match found in _check_greater_equal_requirement
        result = analyzer.version_satisfies_requirement("3.9", "invalid-ge-spec")
        assert result is False

    @staticmethod
    def test_version_satisfies_requirement_ge_triggers_97() -> None:
        """Test version_satisfies_requirement with >= that has malformed version to trigger line 97."""
        analyzer = RequiresPythonAnalyzer(">=3.8")
        # This should trigger the >= path but with malformed requirement to hit line 97
        result = analyzer.version_satisfies_requirement("3.9", ">=malformed")
        assert result is False

    @staticmethod
    def test_version_satisfies_requirement_invalid_upper_bound() -> None:
        """Test version_satisfies_requirement with invalid upper bound that triggers line 112."""
        analyzer = RequiresPythonAnalyzer(">=3.8")
        # This triggers line 112: < present but regex doesn't match in _check_upper_bound_constraint
        result = analyzer.version_satisfies_requirement("3.9", ">=3.8,<invalid")
        assert result is True  # Should return True because invalid < pattern is ignored

    @staticmethod
    def test_version_satisfies_requirement_no_compatible_release_match() -> None:
        """Test version_satisfies_requirement when ~= path has no regex match (line 121)."""
        analyzer = RequiresPythonAnalyzer("invalid")
        # This triggers line 121: no ~= match found in _check_compatible_release_requirement
        result = analyzer.version_satisfies_requirement("3.9", "invalid-compat-spec")
        assert result is False

    @staticmethod
    def test_version_satisfies_requirement_tilde_triggers_121() -> None:
        """Test version_satisfies_requirement with ~= that has malformed version to trigger line 121."""
        analyzer = RequiresPythonAnalyzer("~=3.8")
        # This should trigger the ~= path but with malformed requirement to hit line 121
        result = analyzer.version_satisfies_requirement("3.9", "~=malformed")
        assert result is False

    @staticmethod
    def test_version_satisfies_requirement_no_exact_version_match() -> None:
        """Test version_satisfies_requirement when exact version path has no regex match (line 130)."""
        analyzer = RequiresPythonAnalyzer("invalid")
        # This triggers line 130: no exact version match found in _check_exact_version_requirement
        result = analyzer.version_satisfies_requirement("3.9", "invalid-exact-spec")
        assert result is False

    @staticmethod
    def test_get_requires_python_supported_versions_none_value() -> None:
        """Test get_requires_python_supported_versions with None value (line 157)."""
        project = Project(
            configuration_file=Mock(),
            readme=Mock(),
            requires_python=ConfigurationFileParameter(WhereToolDefault(Mock()), "requires-python", None),
            classifiers=Mock(),
            keywords=Mock(),
        )

        result = project.get_requires_python_supported_versions(project)
        assert result == set()
