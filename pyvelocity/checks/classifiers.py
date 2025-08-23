"""Implements classifiers check."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from pyvelocity.checks import Check
from pyvelocity.checks import Result
from pyvelocity.constants import LATEST_PYTHON_VERSION

if TYPE_CHECKING:
    from pyvelocity.configurations.files.sections.project import Project


class Classifiers(Check):
    """Check that classifiers are consistent with requires-python."""

    ID = "classifiers"

    def execute(self) -> Result:
        if self.configuration_files.py_project_toml is None:
            return Result(self.ID, is_ok=False, message="pyproject.toml is required for classifiers check")

        if self.configuration_files.py_project_toml.project is None:
            return Result(self.ID, is_ok=False, message="Project section is missing in pyproject.toml")

        return self._check_classifiers(self.configuration_files.py_project_toml.project)

    def _check_classifiers(self, project: Project) -> Result:
        """Check that classifiers are consistent with requires-python."""
        classifiers_value = project.classifiers.value
        if classifiers_value is None:
            return Result(
                self.ID,
                is_ok=False,
                message="classifiers field is missing in [project] section of pyproject.toml",
            )

        if not isinstance(classifiers_value, list):
            return Result(
                self.ID,
                is_ok=False,
                message="classifiers field must be a list in [project] section of pyproject.toml",
            )

        requires_python_value = project.requires_python.value
        if requires_python_value is None:
            return Result(
                self.ID,
                is_ok=False,
                message="requires-python field is missing in [project] section of pyproject.toml",
            )

        # Extract supported Python versions from requires-python
        supported_versions = self.get_supported_python_versions(requires_python_value)
        if not supported_versions:
            return Result(
                self.ID,
                is_ok=False,
                message=f"Could not parse requires-python '{requires_python_value}' in [project] section of pyproject.toml",
            )

        # Extract Python version classifiers from classifiers list
        classifier_versions = self.get_classifier_python_versions(classifiers_value)

        # Find missing and extra versions
        missing_versions = supported_versions - classifier_versions
        extra_versions = classifier_versions - supported_versions

        if missing_versions or extra_versions:
            error_parts = []
            if missing_versions:
                # Sort versions numerically
                sorted_missing = sorted(missing_versions, key=lambda v: tuple(map(int, v.split("."))))
                missing_classifiers = [f"Programming Language :: Python :: {v}" for v in sorted_missing]
                error_parts.append(f"missing classifiers: {', '.join(missing_classifiers)}")
            if extra_versions:
                # Sort versions numerically
                sorted_extra = sorted(extra_versions, key=lambda v: tuple(map(int, v.split("."))))
                extra_classifiers = [f"Programming Language :: Python :: {v}" for v in sorted_extra]
                error_parts.append(f"extra classifiers: {', '.join(extra_classifiers)}")

            message = f"Python version classifiers don't match requires-python '{requires_python_value}': {'; '.join(error_parts)}"
            return Result(self.ID, is_ok=False, message=message)

        return Result(self.ID, is_ok=True, message="")

    def get_supported_python_versions(self, requires_python: str) -> set[str]:
        """Extract supported Python versions from requires-python specification."""
        # Determine the minimum version from requires-python
        min_version = self._extract_minimum_version(requires_python)
        if not min_version:
            return set()

        min_major, min_minor = map(int, min_version.split("."))
        latest_major, latest_minor = map(int, LATEST_PYTHON_VERSION.split("."))

        # Generate all versions from minimum to latest
        all_versions = []
        for major in range(min_major, latest_major + 1):
            start_minor = min_minor if major == min_major else 0
            for minor in range(start_minor, 100):
                if (major, minor) > (latest_major, latest_minor):
                    break
                all_versions.append(f"{major}.{minor}")

        supported = set()
        for version in all_versions:
            if self.version_satisfies_requirement(version, requires_python):
                supported.add(version)

        return supported

    def _extract_minimum_version(self, requires_python: str) -> str | None:
        """Extract the minimum version from requires-python specification."""
        # Handle >= version requirements
        if ">=" in requires_python:
            ge_match = re.search(r">=(\d+)\.(\d+)", requires_python)
            if ge_match:
                return f"{ge_match.group(1)}.{ge_match.group(2)}"

        # Handle ~= compatible release
        if "~=" in requires_python:
            compat_match = re.search(r"~=(\d+)\.(\d+)", requires_python)
            if compat_match:
                return f"{compat_match.group(1)}.{compat_match.group(2)}"

        # Handle exact version specifications
        exact_match = re.search(r"^(\d+)\.(\d+)$", requires_python.strip())
        if exact_match:
            return f"{exact_match.group(1)}.{exact_match.group(2)}"

        return None

    def version_satisfies_requirement(self, version: str, requirement: str) -> bool:
        """Check if a version satisfies the requires-python requirement."""
        major, minor = map(int, version.split("."))

        # Handle >= version requirements
        if ">=" in requirement:
            ge_match = re.search(r">=(\d+)\.(\d+)", requirement)
            if ge_match:
                req_major, req_minor = map(int, ge_match.groups())
                if (major, minor) < (req_major, req_minor):
                    return False

                # Check for upper bound constraints
                if "<" in requirement:
                    lt_match = re.search(r"<(\d+)\.(\d+)", requirement)
                    if lt_match:
                        max_major, max_minor = map(int, lt_match.groups())
                        if (major, minor) >= (max_major, max_minor):
                            return False
                return True

        # Handle ~= compatible release
        if "~=" in requirement:
            compat_match = re.search(r"~=(\d+)\.(\d+)", requirement)
            if compat_match:
                compat_major, compat_minor = map(int, compat_match.groups())
                return major == compat_major and minor == compat_minor

        # Handle exact version specifications
        exact_match = re.search(r"^(\d+)\.(\d+)$", requirement.strip())
        if exact_match:
            req_major, req_minor = map(int, exact_match.groups())
            return (major, minor) == (req_major, req_minor)

        return False

    def get_classifier_python_versions(self, classifiers: list[str]) -> set[str]:
        """Extract Python versions from Programming Language :: Python :: X.Y classifiers."""
        versions = set()
        python_version_pattern = r"^Programming Language :: Python :: (\d+\.\d+)$"

        for classifier in classifiers:
            match = re.match(python_version_pattern, classifier.strip())
            if match:
                versions.add(match.group(1))

        return versions
