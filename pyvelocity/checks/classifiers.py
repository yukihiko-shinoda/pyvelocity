"""Implements classifiers check."""

from pyvelocity.checks import Check
from pyvelocity.checks import Result
from pyvelocity.configurations.files.sections.project import Project
from pyvelocity.constants import LATEST_PYTHON_VERSION


class Classifiers(Check):
    """Check that classifiers include the latest Python version."""

    ID = "classifiers"

    def execute(self) -> Result:
        if self.configuration_files.py_project_toml is None:
            return Result(self.ID, is_ok=False, message="pyproject.toml is required for classifiers check")

        if self.configuration_files.py_project_toml.project is None:
            return Result(self.ID, is_ok=False, message="Project section is missing in pyproject.toml")

        return self._check_classifiers(self.configuration_files.py_project_toml.project)

    def _check_classifiers(self, project: Project) -> Result:
        """Check that classifiers include the latest Python version."""
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

        if not self._has_latest_python_classifier(classifiers_value):
            expected_classifier = f"Programming Language :: Python :: {LATEST_PYTHON_VERSION}"
            message = f"classifiers should include '{expected_classifier}' in [project] section of pyproject.toml"
            return Result(self.ID, is_ok=False, message=message)

        return Result(self.ID, is_ok=True, message="")

    def _has_latest_python_classifier(self, classifiers: list[str]) -> bool:
        """Check if classifiers include the latest Python version."""
        expected_classifier = f"Programming Language :: Python :: {LATEST_PYTHON_VERSION}"
        return expected_classifier in classifiers
