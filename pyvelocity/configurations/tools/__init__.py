# SPDX-FileCopyrightText: Copyright (c) 2022 Yukihiko Shinoda
# SPDX-License-Identifier: MIT
"""Implements tools."""

from abc import ABC


# Reason: abstruct class. pylint: disable=too-few-public-methods
class Tool(ABC):
    NAME: str
