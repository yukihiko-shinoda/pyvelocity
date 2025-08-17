from configparser import ConfigParser
from pathlib import Path
from typing import Any
from typing import Optional

import pytest

from pyvelocity.configurations.files.py_project_toml import WHERE_PY_PROJECT_TOML
from pyvelocity.configurations.files.py_project_toml import PyProjectToml
from pyvelocity.configurations.files.sections.pylint import Format
from pyvelocity.configurations.files.sections.pylint import Pylint
from pyvelocity.configurations.files.sections.pylint import PyProjectTomlPylintFactory
from pyvelocity.configurations.files.sections.pylint import SetupCfgPylintFactory
from pyvelocity.configurations.files.setup_cfg import WHERE_SETUP_CFG
from pyvelocity.configurations.files.setup_cfg import SetupCfg


class TestPyProjectTomlPylintFactory:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test_none() -> None:
        py_project_toml = PyProjectToml(Path(WHERE_PY_PROJECT_TOML))
        tool: dict[str, Optional[dict[str, Any]]] = {}
        assert PyProjectTomlPylintFactory.create(py_project_toml, "node", tool) is None


class TestSetupCfgPylintFactory:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test() -> None:
        setup_cfg = SetupCfg(Path(WHERE_SETUP_CFG))
        config_str = "[pylint.format]\nmax-line-length = 120"
        tool = ConfigParser()
        tool.read_string(config_str)
        pylint = SetupCfgPylintFactory.create(setup_cfg, tool)
        assert isinstance(pylint, Pylint)
        assert isinstance(pylint.format, Format)
        # TODO: It should be integer, however it's too difficult to convert type for now.
        assert pylint.format.max_line_length.value == "120"  # type: ignore[comparison-overlap]

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test_none() -> None:
        setup_cfg = SetupCfg(Path(WHERE_SETUP_CFG))
        config_str = ""
        tool = ConfigParser()
        tool.read_string(config_str)
        assert SetupCfgPylintFactory.create(setup_cfg, tool) is None
