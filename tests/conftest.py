"""Configuration of pytest."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

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


# Reason: Fixture. pylint: disable=redefined-outer-name
@pytest.fixture
def configured_tmp_path(ch_tmp_path: Path, resource_path_root: Path, files: list[str]) -> Path:
    """Prepares configuration files in temporary directory."""
    shutil.copy(resource_path_root / files[0], ch_tmp_path / "pyproject.toml")
    shutil.copy(resource_path_root / files[1], ch_tmp_path / "setup.cfg")
    return ch_tmp_path


class MockClassifiersField:
    """Mock classifiers field that implements the protocol."""

    def __init__(self, value: list[str] | str | None) -> None:
        self.value = value


class MockProject:
    """Mock project configuration that implements the protocol."""

    def __init__(self, classifiers_value: list[str] | str | None) -> None:
        self.classifiers = MockClassifiersField(classifiers_value) if classifiers_value is not None else None


class MockPyProjectToml:
    """Mock pyproject.toml configuration that implements the protocol."""

    def __init__(self, project: MockProject | None) -> None:
        self.project = project


@pytest.fixture
def mock_classifiers_field() -> type[MockClassifiersField]:
    """Factory fixture for creating MockClassifiersField instances."""
    return MockClassifiersField


@pytest.fixture
def mock_project() -> type[MockProject]:
    """Factory fixture for creating MockProject instances."""
    return MockProject


@pytest.fixture
def mock_py_project_toml() -> type[MockPyProjectToml]:
    """Factory fixture for creating MockPyProjectToml instances."""
    return MockPyProjectToml


@pytest.fixture
def mock_py_project_toml_with_typing_classifier(
    mock_py_project_toml: type[MockPyProjectToml],
    mock_project: type[MockProject],
) -> MockPyProjectToml:
    """Fixture providing a mock pyproject.toml with 'Typing :: Typed' classifier."""
    classifiers = ["Development Status :: 4 - Beta", "Typing :: Typed"]
    project = mock_project(classifiers)
    return mock_py_project_toml(project)


@pytest.fixture
def mock_py_project_toml_without_typing_classifier(
    mock_py_project_toml: type[MockPyProjectToml],
    mock_project: type[MockProject],
) -> MockPyProjectToml:
    """Fixture providing a mock pyproject.toml without 'Typing :: Typed' classifier."""
    classifiers = ["Development Status :: 4 - Beta", "License :: OSI Approved"]
    project = mock_project(classifiers)
    return mock_py_project_toml(project)


@pytest.fixture
def mock_py_project_toml_empty_classifiers(
    mock_py_project_toml: type[MockPyProjectToml],
    mock_project: type[MockProject],
) -> MockPyProjectToml:
    """Fixture providing a mock pyproject.toml with empty classifiers list."""
    project = mock_project([])
    return mock_py_project_toml(project)


@pytest.fixture
def mock_py_project_toml_non_list_classifiers(
    mock_py_project_toml: type[MockPyProjectToml],
    mock_project: type[MockProject],
) -> MockPyProjectToml:
    """Fixture providing a mock pyproject.toml with non-list classifiers."""
    project = mock_project("not-a-list")
    return mock_py_project_toml(project)


@pytest.fixture
def mock_py_project_toml_no_project(mock_py_project_toml: type[MockPyProjectToml]) -> MockPyProjectToml:
    """Fixture providing a mock pyproject.toml with no project section."""
    return mock_py_project_toml(None)


@pytest.fixture
def mock_py_project_toml_no_classifiers(
    mock_py_project_toml: type[MockPyProjectToml],
    mock_project: type[MockProject],
) -> MockPyProjectToml:
    """Fixture providing a mock pyproject.toml with no classifiers field."""
    project = mock_project(None)
    return mock_py_project_toml(project)
