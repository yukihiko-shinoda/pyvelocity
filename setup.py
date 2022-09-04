#!/usr/bin/env python
"""The setup script."""

from setuptools import setup  # type: ignore

setup(
    # pipenv-setup causes error without dependency_links property:
    # https://github.com/Madoshakalaka/pipenv-setup/issues/23
    dependency_links=[],
    install_requires=["click>=7.0", "tomli", "typing-extensions"],
)
