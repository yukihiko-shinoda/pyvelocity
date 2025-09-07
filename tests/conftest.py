"""Configuration of pytest."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

from pyvelocity.configurations.files.py_project_toml import PyProjectToml

if TYPE_CHECKING:
    from collections.abc import Generator

collect_ignore = ["setup.py"]


@pytest.fixture
def configured_cli_runner(
    tmp_path: Path,
    resource_path_root: Path,
    files: list[str],
) -> Generator[CliRunner, None, None]:
    """Prepares CLI runner with configuration files in temporary directory."""
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as temp_dir:
        temp_path_dir = Path(temp_dir)
        shutil.copy(resource_path_root / files[0], temp_path_dir / "pyproject.toml")
        shutil.copy(resource_path_root / files[1], temp_path_dir / "setup.cfg")
        yield runner


@pytest.fixture
def ch_tmp_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Changes directory to temporary directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def configured_tmp_path(ch_tmp_path: Path, resource_path_root: Path, files: list[str]) -> Path:  # pylint: disable=redefined-outer-name
    """Prepares configuration files in temporary directory."""
    shutil.copy(resource_path_root / files[0], ch_tmp_path / "pyproject.toml")
    shutil.copy(resource_path_root / files[1], ch_tmp_path / "setup.cfg")
    return ch_tmp_path


def _create_temp_pyproject_toml(content: str) -> PyProjectToml:
    """Create a temporary pyproject.toml file with the given content and return PyProjectToml object."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(content)
        temp_path = Path(f.name)

    try:
        return PyProjectToml(temp_path)
    finally:
        temp_path.unlink()  # Clean up the temporary file


@pytest.fixture
def mock_py_project_toml_with_typing_classifier() -> PyProjectToml:
    """Fixture providing a real pyproject.toml with 'Typing :: Typed' classifier."""
    content = """[project]
name = "test"
version = "0.1.0"
description = "Test project"
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Development Status :: 4 - Beta",
    "Typing :: Typed"
]
"""
    return _create_temp_pyproject_toml(content)


@pytest.fixture
def mock_py_project_toml_without_typing_classifier() -> PyProjectToml:
    """Fixture providing a real pyproject.toml without 'Typing :: Typed' classifier."""
    content = """[project]
name = "test"
version = "0.1.0"
description = "Test project"
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved"
]
"""
    return _create_temp_pyproject_toml(content)


@pytest.fixture
def mock_py_project_toml_empty_classifiers() -> PyProjectToml:
    """Fixture providing a real pyproject.toml with empty classifiers list."""
    content = """[project]
name = "test"
version = "0.1.0"
description = "Test project"
readme = "README.md"
requires-python = ">=3.9"
classifiers = []
"""
    return _create_temp_pyproject_toml(content)


@pytest.fixture
def mock_py_project_toml_non_list_classifiers() -> PyProjectToml:
    """Fixture providing a real pyproject.toml with non-list classifiers."""
    content = """[project]
name = "test"
version = "0.1.0"
description = "Test project"
readme = "README.md"
requires-python = ">=3.9"
classifiers = "not-a-list"
"""
    return _create_temp_pyproject_toml(content)


@pytest.fixture
def mock_py_project_toml_no_project() -> PyProjectToml:
    """Fixture providing a real pyproject.toml with no project section."""
    content = """[tool.setuptools]
zip-safe = "false"
"""
    return _create_temp_pyproject_toml(content)


@pytest.fixture
def mock_py_project_toml_no_classifiers() -> PyProjectToml:
    """Fixture providing a real pyproject.toml with no classifiers field."""
    content = """[project]
name = "test"
version = "0.1.0"
description = "Test project"
readme = "README.md"
requires-python = ">=3.9"
"""
    return _create_temp_pyproject_toml(content)
