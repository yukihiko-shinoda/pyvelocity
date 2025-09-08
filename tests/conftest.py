"""Configuration of pytest."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

from pyvelocity.checks import Result
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files import ConfigurationFile
from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.py_project_toml import PyProjectToml

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Generator

    from pyvelocity.configurations.files.sections.setuptools import Setuptools

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
    if len(files) > 1:
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
def configuration_files() -> ConfigurationFiles:
    """Fixture providing a ConfigurationFiles instance."""
    return ConfigurationFiles()


@pytest.fixture
# Reason: Using fixture. pylint: disable-next=redefined-outer-name
def configurations(configuration_files: ConfigurationFiles) -> Configurations:
    """Fixture providing a Configurations instance."""
    return Configurations(configuration_files)


@pytest.fixture
def successful_result() -> Result:
    """Fixture providing a successful Result for testing."""
    return Result("test", is_ok=True, message="")


@pytest.fixture
def failed_result() -> Result:
    """Fixture providing a failed Result for testing."""
    return Result("test", is_ok=False, message="Test failure message")


@pytest.fixture
def mock_setuptools() -> Setuptools:
    """Fixture providing a real Setuptools object for testing."""
    # Create a temporary pyproject.toml with setuptools configuration
    content = """[tool.setuptools]
zip-safe = "false"
package-data = {"*" = ["py.typed"]}
"""
    pyproject_toml = _create_temp_pyproject_toml(content)
    setuptools = pyproject_toml.setuptools

    # Ensure setuptools is not None (it should never be with valid config)
    if setuptools is None:
        msg = "Failed to create setuptools configuration"
        raise RuntimeError(msg)

    # Add packages attribute for typed check compatibility
    setuptools.packages = ["testpackage"]  # type: ignore[attr-defined]

    return setuptools


@pytest.fixture
def mock_setuptools_with_packages() -> Callable[[list[str]], Setuptools]:
    """Fixture providing a real Setuptools object factory with specific packages."""

    def _mock_setuptools_with_packages(packages: list[str]) -> Setuptools:
        # Create a temporary pyproject.toml with setuptools configuration
        content = """[tool.setuptools]
zip-safe = "false"
package-data = {"*" = ["py.typed"]}
"""
        pyproject_toml = _create_temp_pyproject_toml(content)
        setuptools = pyproject_toml.setuptools

        # Ensure setuptools is not None (it should never be with valid config)
        if setuptools is None:
            msg = "Failed to create setuptools configuration"
            raise RuntimeError(msg)

        # Set the specific packages for this instance
        setuptools.packages = packages  # type: ignore[attr-defined]

        return setuptools

    return _mock_setuptools_with_packages


@pytest.fixture
def mock_config_file() -> ConfigurationFile:
    """Fixture providing a mock ConfigurationFile for testing."""

    class MockConfigFile(ConfigurationFile):
        """Mock implementation of ConfigurationFile interface."""

        def __init__(self, name: str = "test.toml") -> None:
            self._name = name

        @property
        def name(self) -> str:
            return self._name

    return MockConfigFile()


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
