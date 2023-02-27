"""Tests for `pyvelocity` package."""
import pytest
from click.testing import CliRunner

from pyvelocity import cli


def test_echo_success():
    cli.echo_success()


@pytest.mark.parametrize(
    "files, expect_exit_code, expect_message",
    [
        (["pyproject_success.toml", "setup_success.cfg"], 0, "Looks high velocity! ⚡️ 🚄 ✨\n"),
        (
            ["pyproject_error.toml", "setup_error.cfg"],
            3,
            (
                "Line length are not consistent.\n"
                "\tMost common = 120\n"
                "\tpyproject.toml tool.docformatter wrap-summaries = 119\n"
                "\tsetup.cfg flake8 max-line-length = 119\n"
                "Error: Looks there are some of improvements.\n"
            ),
        ),
    ],
)
def test_command_line_interface(configured_cli_runner: CliRunner, expect_exit_code, expect_message):
    """Test the CLI."""
    result = configured_cli_runner.invoke(cli.main)
    assert result.exit_code == expect_exit_code
    assert result.output == expect_message


def test_help():
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
