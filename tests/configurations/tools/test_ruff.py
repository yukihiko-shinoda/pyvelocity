"""Tests for ruff tool configuration."""

import pytest

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.tools.ruff import Ruff


class TestRuff:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_ruff.toml", "setup_success.cfg")])
    def test() -> None:
        configuration_files = ConfigurationFiles()
        Ruff(configuration_files)

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_ruff_underscore.toml", "setup_success.cfg")])
    def test_underscore() -> None:
        configuration_files = ConfigurationFiles()
        Ruff(configuration_files)
