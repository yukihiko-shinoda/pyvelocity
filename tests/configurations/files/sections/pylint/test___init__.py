"""Tests for pylint configuration sections."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from pyvelocity.configurations.files.py_project_toml import WHERE_PY_PROJECT_TOML
from pyvelocity.configurations.files.py_project_toml import PyProjectToml
from pyvelocity.configurations.files.sections.pylint import PyProjectTomlPylintFactory


class TestPyProjectTomlPylintFactory:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test_none() -> None:
        py_project_toml = PyProjectToml(Path(WHERE_PY_PROJECT_TOML))
        tool: dict[str, dict[str, Any] | None] = {}
        assert PyProjectTomlPylintFactory.create(py_project_toml, "node", tool) is None
