"""Implements section for project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections import Section


@dataclass
class Project(Section):
    NAME: ClassVar[str] = "project"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = ["readme"]
    readme: ConfigurationFileParameter[str | None]
