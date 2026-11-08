# SPDX-FileCopyrightText: Copyright (c) 2022 Yukihiko Shinoda
# SPDX-License-Identifier: MIT
"""Implements configuration files."""

from abc import ABC
from abc import abstractmethod


class ConfigurationFile(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError  # pragma: no cover
