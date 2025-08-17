"""Configuration of pytest."""

import shutil
from collections.abc import Generator
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch

collect_ignore = ["setup.py"]


@pytest.fixture
def configured_cli_runner(
    tmp_path: Path,
    resource_path_root: Path,
    files: List[str],
) -> Generator[CliRunner, None, None]:
    """Prepares CLI runner with configuration files in temporary directory."""
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as temp_dir:
        temp_path_dir = Path(temp_dir)
        shutil.copy(resource_path_root / files[0], temp_path_dir / "pyproject.toml")
        shutil.copy(resource_path_root / files[1], temp_path_dir / "setup.cfg")
        yield runner


@pytest.fixture
def ch_tmp_path(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    """Changes directory to temporary directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


# Reason: Fixture. pylint: disable=redefined-outer-name
@pytest.fixture
def configured_tmp_path(ch_tmp_path: Path, resource_path_root: Path, files: List[str]) -> Path:
    """Prepares configuration files in temporary directory."""
    shutil.copy(resource_path_root / files[0], ch_tmp_path / "pyproject.toml")
    shutil.copy(resource_path_root / files[1], ch_tmp_path / "setup.cfg")
    return ch_tmp_path
