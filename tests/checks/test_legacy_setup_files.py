"""Tests for legacy-setup-files check."""

from pathlib import Path

import pytest

from pyvelocity.checks.legacy_setup_files import LegacySetupFiles
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestLegacySetupFiles:
    """Test for LegacySetupFiles check."""

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_legacy_files() -> None:
        """Test when no legacy setup files exist."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        legacy_check = LegacySetupFiles(configuration_files, configurations)
        result = legacy_check.execute()
        assert result.message == ""
        assert result.is_ok is True

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_setup_py_exists() -> None:
        """Test when setup.py exists."""
        # Create setup.py file
        Path("setup.py").touch()

        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        legacy_check = LegacySetupFiles(configuration_files, configurations)
        result = legacy_check.execute()
        assert result.message == "Legacy setup files found: setup.py. Use pyproject.toml instead."
        assert result.is_ok is False

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_setup_cfg_exists() -> None:
        """Test when setup.cfg exists."""
        # Create setup.cfg file
        Path("setup.cfg").touch()

        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        legacy_check = LegacySetupFiles(configuration_files, configurations)
        result = legacy_check.execute()
        assert result.message == "Legacy setup files found: setup.cfg. Use pyproject.toml instead."
        assert result.is_ok is False

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_both_legacy_files_exist() -> None:
        """Test when both setup.py and setup.cfg exist."""
        # Create both files
        Path("setup.py").touch()
        Path("setup.cfg").touch()

        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        legacy_check = LegacySetupFiles(configuration_files, configurations)
        result = legacy_check.execute()
        assert result.message == "Legacy setup files found: setup.py, setup.cfg. Use pyproject.toml instead."
        assert result.is_ok is False
