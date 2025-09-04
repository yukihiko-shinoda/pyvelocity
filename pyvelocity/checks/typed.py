"""Implements typed check."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from packagediscovery import Setuptools

from pyvelocity.checks import Check
from pyvelocity.checks import Result


class _HasClassifiersValue(Protocol):
    """Protocol for objects that have a classifiers value."""

    @property
    def value(self) -> object:
        """Get the classifiers value."""


class _HasClassifiers(Protocol):
    """Protocol for objects that have a classifiers attribute."""

    @property
    def classifiers(self) -> _HasClassifiersValue | None:
        """Get the classifiers configuration."""


class _HasProject(Protocol):
    """Protocol for objects that have a project attribute."""

    @property
    def project(self) -> _HasClassifiers | None:
        """Get the project configuration."""


class TypingClassifierValidator:
    """Validates the presence of 'Typing :: Typed' classifier in project metadata."""

    def __init__(self, py_project_toml: _HasProject | None) -> None:
        """Initialize with pyproject.toml configuration."""
        self.py_project_toml = py_project_toml

    def is_typing_classifier_present(self) -> bool:
        """Check if 'Typing :: Typed' classifier is present in pyproject.toml."""
        classifiers = self._get_classifiers_list()
        return classifiers is not None and "Typing :: Typed" in classifiers

    def _get_classifiers_list(self) -> list[str] | None:
        """Extract classifiers list from pyproject.toml, returning None if invalid."""
        if not self._has_valid_project_config():
            return None

        # _has_valid_project_config() guarantees these exist and are not None
        classifiers_value = self._extract_classifiers_value()
        return classifiers_value if isinstance(classifiers_value, list) else None

    def _extract_classifiers_value(self) -> object:
        """Extract classifiers value from validated project configuration."""
        # Type narrowing: _has_valid_project_config() guarantees these are not None
        if self.py_project_toml is None:
            msg = "py_project_toml is unexpectedly None"
            raise RuntimeError(msg)
        project = self.py_project_toml.project
        if project is None:
            msg = "project is unexpectedly None"
            raise RuntimeError(msg)
        classifiers = project.classifiers
        if classifiers is None:
            msg = "classifiers is unexpectedly None"
            raise RuntimeError(msg)
        return classifiers.value

    def _has_valid_project_config(self) -> bool:
        """Check if pyproject.toml has valid project and classifiers configuration."""
        return (
            self.py_project_toml is not None
            and self.py_project_toml.project is not None
            and self.py_project_toml.project.classifiers is not None
            and self.py_project_toml.project.classifiers.value is not None
        )


class Typed(Check):
    """Check about py.typed configuration and file presence."""

    ID = "typed"

    def execute(self) -> Result:
        """Execute the typed check."""
        check_results = self._perform_typed_checks()

        if all(check_results.values()):
            return Result(self.ID, is_ok=True, message="")

        error_messages = self._build_error_messages(check_results)
        return Result(self.ID, is_ok=False, message="\n".join(error_messages))

    def _perform_typed_checks(self) -> dict[str, bool]:
        """Perform all typed check validations and return results."""
        classifier_validator = TypingClassifierValidator(self.configuration_files.py_project_toml)
        return {
            "package_data_config": self._check_package_data_config(),
            "py_typed_files": self._check_py_typed_files(),
            "typing_classifier": classifier_validator.is_typing_classifier_present(),
        }

    def _build_error_messages(self, check_results: dict[str, bool]) -> list[str]:
        """Build error messages for failed checks."""
        messages = []
        if not check_results["package_data_config"]:
            messages.append('Missing tool.setuptools.package-data "*" = ["py.typed"] configuration')
        if not check_results["py_typed_files"]:
            messages.append("Missing py.typed files in package directories")
        if not check_results["typing_classifier"]:
            messages.append('Missing "Typing :: Typed" classifier in pyproject.toml')
        return messages

    def _check_package_data_config(self) -> bool:
        """Check if pyproject.toml has the correct package-data configuration."""
        package_data = self._get_package_data()
        if package_data is None:
            return False
        return self._has_py_typed_in_package_data(package_data)

    def _get_package_data(self) -> dict[str, list[str]] | None:
        """Extract package-data from pyproject.toml."""
        if self.configuration_files.py_project_toml is None:
            return None

        setuptools = self.configuration_files.py_project_toml.setuptools
        if setuptools is None or setuptools.package_data.value is None:
            return None

        package_data = setuptools.package_data.value
        if not isinstance(package_data, dict):
            return None

        return package_data

    def _has_py_typed_in_package_data(self, package_data: dict[str, list[str]]) -> bool:
        """Check if package-data contains py.typed for all packages."""
        return "*" in package_data and "py.typed" in package_data["*"]

    def _check_py_typed_files(self) -> bool:
        """Check if py.typed files exist in package directories."""
        try:
            package_list = self._discover_packages()
            if not package_list:
                return False
            return self._validate_py_typed_files(package_list)
        except (OSError, ImportError, RuntimeError):
            # If package discovery fails, we can't validate
            return False

    def _discover_packages(self) -> list[str]:
        """Discover all packages in the current directory."""
        setuptools = Setuptools()
        return setuptools.packages

    def _validate_py_typed_files(self, package_list: list[str]) -> bool:
        """Validate that py.typed files exist in top-level packages."""
        # Only check top-level packages (those without dots in the name)
        top_level_packages = [pkg for pkg in package_list if "." not in pkg]
        return all(self._py_typed_exists_for_package(package) for package in top_level_packages)

    def _py_typed_exists_for_package(self, package: str) -> bool:
        """Check if py.typed file exists for a specific package."""
        package_path = Path(package.replace(".", "/"))
        py_typed_path = package_path / "py.typed"
        return py_typed_path.exists()
