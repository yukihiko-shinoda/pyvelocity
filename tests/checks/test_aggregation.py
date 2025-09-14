"""Tests for aggregation.py."""

from pathlib import Path

import pytest

from pyvelocity.checks.aggregation import Checks
from pyvelocity.checks.aggregation import Results
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


class TestChecks:
    """Test for Checks."""

    @staticmethod
    @pytest.mark.usefixtures("configured_tmp_path")
    @pytest.mark.parametrize(
        ("files", "expect_message", "expect_is_ok"),
        [
            (["pyproject_success.toml"], "README.md file not found", False),
            (
                ["pyproject_error.toml"],
                (
                    "Line length are not consistent.\n"
                    "\tMost common = 119\n"
                    "\tpyproject.toml tool.docformatter wrap-summaries = 118\n"
                    "\tFlake8 tool default max-line-length = 79 (B950 in flake8-bugbear detects: 87)\n"
                    "\tpyproject.toml tool.ruff line-length = 118\n"
                    "Python version classifiers don't match requires-python '>=3.5': missing classifiers: "
                    "Programming Language :: Python :: 3.10, "
                    "Programming Language :: Python :: 3.11, "
                    "Programming Language :: Python :: 3.12, "
                    "Programming Language :: Python :: 3.13\n"
                    "README.md file not found"
                ),
                False,
            ),
        ],
    )
    def test(
        configuration_files: ConfigurationFiles,
        configurations: Configurations,
        expect_message: str,
        *,
        expect_is_ok: bool,
    ) -> None:
        """Tests general case."""
        results = Results(list(Checks(configuration_files, configurations).execute()))
        assert results.message == expect_message
        assert results.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_py_project_toml(configuration_files: ConfigurationFiles, configurations: Configurations) -> None:
        """Tests case when no pyproject.toml."""
        results = Results(list(Checks(configuration_files, configurations).execute()))
        assert results.message == (
            "It's recommended to use pyproject.toml to gather settings for project.\n"
            "Line length are not consistent.\n"
            "\tMost common = 72\n"
            "\tdocformatter tool default wrap summaries = 79\n"
            "\tFlake8 tool default max-line-length = 79 (B950 in flake8-bugbear detects: 87)\n"
            "\tPylint tool default max-line-length = 100\n"
            "\tRuff tool default line-length = 88\n"
            "pyproject.toml is required for readme check\n"
            "pyproject.toml is required for requires-python check\n"
            "pyproject.toml is required for classifiers check\n"
            "pyproject.toml is required for zip-safe-false check\n"
            'Missing tool.setuptools.package-data "*" = ["py.typed"] configuration\n'
            "Missing py.typed files in package directories\n"
            'Missing "Typing :: Typed" classifier in pyproject.toml\n'
            "pyproject.toml is required for keywords check\n"
            "README.md file not found"
        )
        assert results.is_ok is False

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_legacy_setup_files_detected(
        configuration_files: ConfigurationFiles,
        configurations: Configurations,
    ) -> None:
        """Tests case when legacy setup files are detected."""
        # Create a setup.cfg file to trigger the legacy-setup-files check
        Path("setup.cfg").touch()

        results = Results(list(Checks(configuration_files, configurations).execute()))
        assert "Legacy setup files found: setup.cfg. Use pyproject.toml instead." in results.message
        assert results.is_ok is False
