"""Test Project section functionality."""

from unittest.mock import Mock

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections.project import Project
from pyvelocity.configurations.files.sections.project import RequiresPythonAnalyzer


class TestProjectVersionLogic:
    """Test version parsing logic for Project."""

    @staticmethod
    def test_get_requires_python_supported_versions() -> None:
        """Test get_requires_python_supported_versions with various requires-python formats."""
        # Create a mock Project instance with proper ConfigurationFileParameter
        mock_where = Mock()
        mock_config_file = Mock()
        project = Project(
            configuration_file=mock_config_file,
            readme=ConfigurationFileParameter(mock_where, "readme", None),
            requires_python=ConfigurationFileParameter(mock_where, "requires-python", ">=3.10"),
            classifiers=ConfigurationFileParameter(mock_where, "classifiers", None),
        )

        # Test version requirement parsing for Python 3.10 and above
        versions = project.get_requires_python_supported_versions(project)
        expected = {"3.10", "3.11", "3.12", "3.13"}
        assert versions == expected

        # Test version range with upper bound
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", ">=3.8,<3.12")
        versions = project.get_requires_python_supported_versions(project)
        expected = {"3.8", "3.9", "3.10", "3.11"}
        assert versions == expected

        # Test minimum version requirement including older versions
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", ">=3.5")
        versions = project.get_requires_python_supported_versions(project)
        expected = {"3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"}
        assert versions == expected

        # Test compatible release operator
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", "~=3.11")
        versions = project.get_requires_python_supported_versions(project)
        expected = {"3.11"}
        assert versions == expected

        # Test exact version specification
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", "3.10")
        versions = project.get_requires_python_supported_versions(project)
        expected = {"3.10"}
        assert versions == expected

    @staticmethod
    def test_version_satisfies_requirement() -> None:
        """Test version_satisfies_requirement logic."""
        # Test minimum version requirements
        analyzer = RequiresPythonAnalyzer(">=3.8")
        assert analyzer.version_satisfies_requirement("3.10", ">=3.8") is True
        assert analyzer.version_satisfies_requirement("3.7", ">=3.8") is False
        assert analyzer.version_satisfies_requirement("3.11", ">=3.8") is True

        # Test version range requirements
        assert analyzer.version_satisfies_requirement("3.10", ">=3.8,<3.12") is True
        assert analyzer.version_satisfies_requirement("3.12", ">=3.8,<3.12") is False
        assert analyzer.version_satisfies_requirement("3.7", ">=3.8,<3.12") is False

        # Test compatible release requirements
        assert analyzer.version_satisfies_requirement("3.11", "~=3.11") is True
        assert analyzer.version_satisfies_requirement("3.10", "~=3.11") is False
        assert analyzer.version_satisfies_requirement("3.12", "~=3.11") is False

        # Test exact version requirements
        assert analyzer.version_satisfies_requirement("3.10", "3.10") is True
        assert analyzer.version_satisfies_requirement("3.11", "3.10") is False

    @staticmethod
    def test_requires_python_minimum_version() -> None:
        """Test requires_python_minimum_version extraction."""
        mock_where = Mock()

        # Test >= version requirements
        mock_config_file = Mock()
        project = Project(
            configuration_file=mock_config_file,
            readme=ConfigurationFileParameter(mock_where, "readme", None),
            requires_python=ConfigurationFileParameter(mock_where, "requires-python", ">=3.8"),
            classifiers=ConfigurationFileParameter(mock_where, "classifiers", None),
        )
        assert project.requires_python_minimum_version() == "3.8"

        # Test ~= compatible release
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", "~=3.11")
        assert project.requires_python_minimum_version() == "3.11"

        # Test exact version
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", "3.10")
        assert project.requires_python_minimum_version() == "3.10"

        # Test invalid format
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", "invalid")
        assert project.requires_python_minimum_version() is None

        # Test None value
        project.requires_python = ConfigurationFileParameter(mock_where, "requires-python", None)
        assert project.requires_python_minimum_version() is None
