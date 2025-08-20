"""Implements requires-python check."""

import re

from pyvelocity.checks import Check
from pyvelocity.checks import Result
from pyvelocity.configurations.files.sections.project import Project
from pyvelocity.constants import LATEST_PYTHON_VERSION


class RequiresPython(Check):
    """Check that requires-python includes the latest Python version."""

    ID = "requires-python"

    def execute(self) -> Result:
        if self.configuration_files.py_project_toml is None:
            return Result(self.ID, is_ok=False, message="pyproject.toml is required for requires-python check")

        if self.configuration_files.py_project_toml.project is None:
            return Result(self.ID, is_ok=False, message="Project section is missing in pyproject.toml")

        return self._check_requires_python(self.configuration_files.py_project_toml.project)

    def _check_requires_python(self, project: Project) -> Result:
        """Check that requires-python includes the latest Python version."""
        requires_python_value = project.requires_python.value
        if requires_python_value is None:
            return Result(
                self.ID,
                is_ok=False,
                message="requires-python field is missing in [project] section of pyproject.toml",
            )

        if not self.supports_latest_python(requires_python_value):
            message = (
                f"requires-python should support Python {LATEST_PYTHON_VERSION}, "
                f'but found "{requires_python_value}" in [project] section of pyproject.toml'
            )
            return Result(self.ID, is_ok=False, message=message)

        return Result(self.ID, is_ok=True, message="")

    def supports_latest_python(self, requires_python: str) -> bool:
        """Check if the requires-python specification supports the latest Python version."""
        """
        Handle common patterns:
        ">=3.8" -> check if 3.13 >= 3.8
        ">=3.8,<4.0" -> check if 3.13 is in range
        "~=3.8" -> compatible release (3.8.x)
        """

        # Extract version components
        latest_major, latest_minor = map(int, LATEST_PYTHON_VERSION.split("."))

        # Handle >= version requirements
        if ">=" in requires_python:
            # Extract the minimum version from patterns like ">=3.8" or ">=3.8,<4.0"
            ge_match = re.search(r">=(\d+)\.(\d+)", requires_python)
            if ge_match:
                min_major, min_minor = map(int, ge_match.groups())

                # Check if latest version meets minimum requirement
                if (latest_major, latest_minor) >= (min_major, min_minor):
                    # Check for upper bound constraints
                    if "<" in requires_python:
                        lt_match = re.search(r"<(\d+)\.(\d+)", requires_python)
                        if lt_match:
                            max_major, max_minor = map(int, lt_match.groups())
                            return (latest_major, latest_minor) < (max_major, max_minor)
                    return True

        # Handle ~= compatible release
        if "~=" in requires_python:
            compat_match = re.search(r"~=(\d+)\.(\d+)", requires_python)
            if compat_match:
                compat_major, compat_minor = map(int, compat_match.groups())
                # Compatible release means same major.minor version family
                # ~=3.12 allows 3.12.x but not 3.13.x
                return latest_major == compat_major and latest_minor == compat_minor

        # Handle exact version specifications
        exact_match = re.search(r"^(\d+)\.(\d+)$", requires_python.strip())
        if exact_match:
            req_major, req_minor = map(int, exact_match.groups())
            return (latest_major, latest_minor) == (req_major, req_minor)

        return False
