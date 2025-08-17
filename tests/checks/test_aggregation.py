"""Tests for aggregation.py."""

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
        "files, expect_message, expect_is_ok",
        [
            (["pyproject_success.toml", "setup_success.cfg"], "", True),
            (
                ["pyproject_error.toml", "setup_error.cfg"],
                (
                    "Line length are not consistent.\n"
                    "\tMost common = 120\n"
                    "\tpyproject.toml tool.docformatter wrap-summaries = 119\n"
                    "\tsetup.cfg flake8 max-line-length = 119"
                ),
                False,
            ),
        ],
    )
    def test(expect_message: str, expect_is_ok: bool) -> None:
        """Tests general case."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        results = Results(list(Checks(configuration_files, configurations).execute()))
        assert results.message == expect_message
        assert results.is_ok == expect_is_ok

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_no_py_project_toml() -> None:
        """Tests case when no pyproject.toml."""
        configuration_files = ConfigurationFiles()
        configurations = Configurations(configuration_files)
        results = Results(list(Checks(configuration_files, configurations).execute()))
        assert results.message == (
            "It's recommended to use pyproject.toml to gather settings for project.\n"
            "Line length are not consistent.\n"
            "\tMost common = 79\n"
            "\tdocformatter tool default = 72\n"
            "\tBlack tool default = 88\n"
            "\tPylint tool default = 100"
        )
        assert results.is_ok is False
