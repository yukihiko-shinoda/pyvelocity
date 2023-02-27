import pytest

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.tools.pylint import Format


class TestFormat:
    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize("files", [("pyproject_success.toml", "setup_pylint.cfg")])
    def test() -> None:
        configuration_files = ConfigurationFiles()
        Format(configuration_files)
