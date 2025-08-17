"""Implements isort."""

from typing import Optional

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections import WhereToolDefault
from pyvelocity.configurations.files.sections import is_not_none_value
from pyvelocity.configurations.files.sections import isort
from pyvelocity.configurations.tools import Tool


class Isort(Tool):
    """Isort configurations."""

    NAME = "isort"

    def __init__(self, configuration_files: ConfigurationFiles) -> None:
        self.line_length = ConfigurationFileParameter(
            WhereToolDefault(self),
            ConfigurationFileParameter.NAME_TOOL_DEFAULT,
            79,
        )
        if configuration_files.setup_cfg:
            self.overwrite(configuration_files.setup_cfg.isort)
        if configuration_files.py_project_toml:
            self.overwrite(configuration_files.py_project_toml.isort)

    def overwrite(self, section_isort: Optional[isort.Isort]) -> None:
        if section_isort:
            if is_not_none_value(section_isort.line_length):
                self.line_length = section_isort.line_length
