"""Implements section for setuptools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from pyvelocity.configurations.files.sections import ConfigurationFileParameter
from pyvelocity.configurations.files.sections import Section


@dataclass
class Setuptools(Section):
    """Represents the [tool.setuptools] section in pyproject.toml configuration files."""

    NAME: ClassVar[str] = "setuptools"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = ["zip-safe"]
    zip_safe: ConfigurationFileParameter[str | None]
