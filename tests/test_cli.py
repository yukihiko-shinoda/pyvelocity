"""Tests for `pyvelocity` package."""
# Reason: Accept risk of using subprocess.
import os
from subprocess import PIPE, run  # nosec B404

from click.testing import CliRunner
import pytest

from pyvelocity import cli


def test_echo_success() -> None:
    cli.echo_success()


def test_echo_success_in_subprocess() -> None:
    """Function echo_success() should fallback to no emoji.

    When echo emoji in subprocess on Windows, Following error raised:
      UnicodeEncodeError: 'charmap' codec can't encode characters in position 21-22
    Pyvelocity may be used in CI and it may be used in subprocess.
    see:
    - UnicodeEncodeError on Windows when there are Unicode chars in the help message
       · Issue #2121 · pallets/click
      https://github.com/pallets/click/issues/2121
    - UnicodeEncodeError in Windows agent CI pipelines
      https://gist.github.com/NodeJSmith/e7e37f2d3f162456869f015f842bcf15
    """
    # Reason: Accept risk of using subprocess.
    completed_process = run("pyvelocity", check=True, stdout=PIPE, stderr=PIPE)  # nosec B603 B607
    expected = ["Looks high velocity! ⚡️ 🚄 ✨\n", f"Looks high velocity!{os.linesep}"]
    assert completed_process.stdout.decode("utf-8") in expected


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
def test_command_line_interface(configured_cli_runner: CliRunner, expect_exit_code: int, expect_message: str) -> None:
    """Test the CLI."""
    result = configured_cli_runner.invoke(cli.main)
    assert result.exit_code == expect_exit_code
    assert result.output == expect_message


def test_help() -> None:
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
