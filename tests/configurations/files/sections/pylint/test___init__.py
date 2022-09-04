from configparser import ConfigParser
from pathlib import Path

import pytest

from pyvelocity.configurations.files.py_project_toml import WHERE_PY_PROJECT_TOML, PyProjectToml
from pyvelocity.configurations.files.sections.pylint import PyProjectTomlPylintFactory, SetupCfgPylintFactory
from pyvelocity.configurations.files.setup_cfg import WHERE_SETUP_CFG, SetupCfg


class TestPyProjectTomlPylintFactory:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test_none():
        py_project_toml = PyProjectToml(Path(WHERE_PY_PROJECT_TOML))
        tool = {}
        assert PyProjectTomlPylintFactory.create(py_project_toml, "node", tool) is None


class TestSetupCfgPylintFactory:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test():
        setup_cfg = SetupCfg(Path(WHERE_SETUP_CFG))
        config_str = "[pylint.format]\nmax-line-length = 120"
        tool = ConfigParser()
        tool.read_string(config_str)
        pylint = SetupCfgPylintFactory.create(setup_cfg, tool)
        assert pylint.format.max_line_length.value == "120"

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_success.cfg")])
    def test_none():
        setup_cfg = SetupCfg(Path(WHERE_SETUP_CFG))
        config_str = ""
        tool = ConfigParser()
        tool.read_string(config_str)
        assert SetupCfgPylintFactory.create(setup_cfg, tool) is None
