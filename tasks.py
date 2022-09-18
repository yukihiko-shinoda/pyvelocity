"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import platform
import shutil
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli
from invoke import task  # type: ignore
from invoke.runners import Failure, Result  # type: ignore

ROOT_DIR = Path(__file__).parent
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("pyvelocity")
SETUP_PY = ROOT_DIR.joinpath("setup.py")
TASKS_PY = ROOT_DIR.joinpath("tasks.py")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
PYTHON_DIRS = [str(directory) for directory in [SETUP_PY, TASKS_PY, SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


@task(help={"check": "Checks if source is formatted without applying changes"})
def style(context, check=False):
    """Format code."""
    for result in [
        docformatter(context, check),
        isort(context, check),
        autoflake(context, check),
        black(context, check),
    ]:
        if result.failed:
            raise Failure(result)


def docformatter(context, check=False) -> Result:
    """Runs docformatter.

    This function includes hard coding of line length.
    see:
    - Add pyproject.toml support for config (Issue #10) by weibullguy · Pull Request #77 · PyCQA/docformatter
      https://github.com/PyCQA/docformatter/pull/77
    """
    parsed_toml = tomli.loads(Path("pyproject.toml").read_text("UTF-8"))
    config = parsed_toml["tool"]["docformatter"]
    list_options = build_list_options_docformatter(config, check)
    docformatter_options = f"{' '.join(list_options)}"
    return context.run(f"docformatter {docformatter_options} {' '.join(PYTHON_DIRS)}", warn=True)


@dataclass
class DocformatterOption:
    list_str: list[str]
    enable: bool


def build_list_options_docformatter(config: dict[str, Any], check: bool) -> list[str]:
    """Builds list of docformatter options."""
    docformatter_options = (
        DocformatterOption(["--recursive"], "recursive" in config and config["recursive"]),
        DocformatterOption(["--wrap-summaries", str(config["wrap-summaries"])], "wrap-summaries" in config),
        DocformatterOption(["--wrap-descriptions", str(config["wrap-descriptions"])], "wrap-descriptions" in config),
        DocformatterOption(["--check"], check),
        DocformatterOption(["--in-place"], not check),
    )
    return [
        item
        for docformatter_option in docformatter_options
        if docformatter_option.enable
        for item in docformatter_option.list_str
    ]


def autoflake(context, check=False) -> Result:
    """Runs autoflake."""
    autoflake_options = f"--recursive {'--check' if check else '--in-place'}"
    return context.run(f"autoflake {autoflake_options} {' '.join(PYTHON_DIRS)}", warn=True)


def isort(context, check=False) -> Result:
    """Runs isort."""
    isort_options = "--check-only --diff" if check else ""
    return context.run(f"isort {isort_options} {' '.join(PYTHON_DIRS)}", warn=True)


def black(context, check=False) -> Result:
    """Runs black."""
    black_options = "--check --diff" if check else ""
    return context.run(f"black {black_options} {' '.join(PYTHON_DIRS)}", warn=True)


@task
def lint_bandit(context):
    """Lints code with bandit."""
    space = " "
    context.run(f"bandit --recursive {space.join([str(p) for p in [SOURCE_DIR, TASKS_PY]])}", pty=True)
    context.run(f"bandit --recursive --skip B101 {TEST_DIR}", pty=True)


@task
def lint_dodgy(context):
    """Lints code with dodgy."""
    context.run("dodgy --ignore-paths csvinput", pty=True)


@task
def lint_flake8(context):
    """Lint code with flake8."""
    context.run(f"flake8 {'--radon-show-closures'} {' '.join(PYTHON_DIRS)}")


@task
def lint_pydocstyle(context):
    """Lints code with pydocstyle."""
    context.run("pydocstyle .", pty=True)


@task
def lint_pylint(context):
    """Lint code with pylint."""
    context.run(f"pylint {' '.join(PYTHON_DIRS)}")


@task
def lint_mypy(context):
    """Lint code with pylint."""
    context.run(f"mypy {' '.join(PYTHON_DIRS)}")


@task(lint_bandit, lint_dodgy, lint_flake8, lint_pydocstyle)
def lint(_context):
    """Run all linting."""


@task(lint_mypy, lint_pylint)
def lint_deep(_context):
    """Runs deep linting."""


@task
def radon_cc(context):
    """Reports code complexity."""
    context.run(f"radon cc {' '.join(PYTHON_DIRS)}")


@task
def radon_mi(context):
    """Reports maintainability index."""
    context.run(f"radon mi {' '.join(PYTHON_DIRS)}")


@task(radon_cc, radon_mi)
def radon(_context):
    """Reports radon."""


@task
def xenon(context):
    """Check code complexity."""
    context.run(("xenon" " --max-absolute A" "--max-modules A" "--max-average A" f"{' '.join(PYTHON_DIRS)}"))


@task
def test(context):
    """Run tests."""
    pty = platform.system() == "Linux"
    context.run("pytest", pty=pty)


@task(
    help={
        "publish": "Publish the result via coveralls",
        "xml": "Export report as xml format",
    }
)
def coverage(context, publish=False, xml=False):
    """Create coverage report."""
    context.run(f"coverage run --source {SOURCE_DIR} -m pytest")
    context.run("coverage report -m")
    if publish:
        # Publish the results via coveralls
        context.run("coveralls")
        return
    # Build a local report
    if xml:
        context.run("coverage xml")
    else:
        context.run("coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task
def clean_build(context):
    """Clean up files from package building."""
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    context.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(context):
    """Clean up python file artifacts."""
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    context.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(_context):
    """Clean up files from testing."""
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests])
def clean(_context):
    """Runs all clean sub-tasks."""


@task(clean)
def dist(context):
    """Build source and wheel packages."""
    context.run("python -m build")
