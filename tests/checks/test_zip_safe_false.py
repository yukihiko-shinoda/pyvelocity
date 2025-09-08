"""Tests for zip-safe-false check."""

import pytest

from pyvelocity.checks.zip_safe_false import ZipSafeFalse
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.sections.setuptools import Setuptools


class TestZipSafeFalse:
    """Test for ZipSafeFalse check."""

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize(
        ("files", "expect_message", "expect_is_ok"),
        [
            (
                ["pyproject_setuptools_zip_safe_false.toml", "setup_success.cfg"],
                "",
                True,
            ),
            (
                ["pyproject_setuptools_zip_safe_true.toml", "setup_success.cfg"],
                (
                    'zip-safe should be "false", but found "true" '
                    "in [tool.setuptools] section of pyproject.toml. "
                    "New users of setuptools should not attempt to create egg files "
                    "using the deprecated build_egg command."
                ),
                False,
            ),
            (
                ["pyproject_setuptools_zip_safe_missing.toml", "setup_success.cfg"],
                "zip-safe field is missing in [tool.setuptools] section of pyproject.toml",
                False,
            ),
            (
                ["pyproject_setuptools_missing.toml", "setup_success.cfg"],
                "[tool.setuptools] section is missing in pyproject.toml",
                False,
            ),
        ],
    )
    def test_zip_safe_false_check(
        configuration_files: ConfigurationFiles,
        configurations: Configurations,
        expect_message: str,
        *,
        expect_is_ok: bool,
    ) -> None:
        """Tests zip-safe-false check scenarios."""
        zip_safe_false_check = ZipSafeFalse(configuration_files, configurations)
        result = zip_safe_false_check.execute()
        assert result.message == expect_message
        assert result.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_pyproject_toml(configuration_files: ConfigurationFiles, configurations: Configurations) -> None:
        """Tests case when no pyproject.toml exists."""
        zip_safe_false_check = ZipSafeFalse(configuration_files, configurations)
        result = zip_safe_false_check.execute()
        assert result.message == "pyproject.toml is required for zip-safe-false check"
        assert result.is_ok is False


class TestZipSafeFalseValueHandling:
    """Test value handling logic for ZipSafeFalse."""

    @staticmethod
    @pytest.mark.parametrize(
        "zip_safe_value",
        ["false", "False", "FALSE"],
    )
    def test_zip_safe_accepts_false_values(mock_setuptools: Setuptools, zip_safe_value: str) -> None:
        """Test zip-safe accepts 'false' values (case insensitive)."""
        zip_safe_false_check = ZipSafeFalse(None, None)  # type: ignore[arg-type]
        mock_setuptools.zip_safe.value = zip_safe_value

        result = zip_safe_false_check.check_zip_safe(mock_setuptools)
        assert result.is_ok is True

    @staticmethod
    @pytest.mark.parametrize(
        "zip_safe_value",
        ["true", "True", "TRUE", "1", "0", "yes", "no"],
    )
    def test_zip_safe_rejects_non_false_values(mock_setuptools: Setuptools, zip_safe_value: str) -> None:
        """Test zip-safe rejects non-'false' values."""
        zip_safe_false_check = ZipSafeFalse(None, None)  # type: ignore[arg-type]
        mock_setuptools.zip_safe.value = zip_safe_value

        result = zip_safe_false_check.check_zip_safe(mock_setuptools)
        assert result.is_ok is False
        assert "zip-safe should be" in result.message
        assert "deprecated build_egg command" in result.message
