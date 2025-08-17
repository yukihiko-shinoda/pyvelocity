"""Implements section for pyvelocity."""

from dataclasses import dataclass
from typing import ClassVar
from typing import Optional

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections import Section


@dataclass
class Pyvelocity(Section):
    NAME: ClassVar[str] = "pyvelocity"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = ["filter"]
    filter: ConfigurationFileParameter[Optional[list[str]]]
