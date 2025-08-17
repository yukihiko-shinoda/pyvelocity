"""Implements section for Black."""

from dataclasses import dataclass
from typing import ClassVar
from typing import Optional

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections import Section


@dataclass
class Black(Section):
    NAME: ClassVar[str] = "black"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = ["line-length"]
    line_length: ConfigurationFileParameter[Optional[int]]
