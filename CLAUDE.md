# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyVelocity is a Python tool that checks configuration consistency across Python development tools to improve development velocity. It validates that line-length settings are consistent across docformatter, isort, Black, flake8, and Pylint, and ensures projects use pyproject.toml for configuration.

## Development Commands

### Virtual Environment
```bash
source /workspace/.venv/bin/activate
```

### Testing
- Run fast tests: `uv run invoke test` or `uv run invoke test.fast`
- Run all tests: `uv run invoke test.all`
- Run tests with coverage: `uv run invoke test.coverage`

### Linting
- Fast linting: `uv run invoke lint` or `uv run invoke lint.fast`
- Deep linting (slow): `uv run invoke lint.deep`
- Specific tools:
  - `uv run invoke lint.ruff`
  - `uv run invoke lint.flake8`
  - `uv run invoke lint.mypy`
  - `uv run invoke lint.pylint`

### Code Formatting
- Format code: `uv run invoke style` or `uv run invoke style.fmt`

### Build and Distribution
- Build package: `uv run invoke dist`
- Clean artifacts: `uv run invoke clean`

### Running the Tool
- Run pyvelocity: `pyvelocity` (requires installation) or `uv run python -m pyvelocity.cli`

## Architecture

The codebase follows a modular architecture with three main components:

### 1. Configuration Management (`pyvelocity/configurations/`)
- **Files layer** (`files/`): Parses pyproject.toml and setup.cfg files
- **Tools layer** (`tools/`): Abstracts configuration for each tool (Black, isort, flake8, Pylint, docformatter)
- **Aggregation** (`aggregation.py`): Combines all tool configurations

### 2. Checks (`pyvelocity/checks/`)
- **line_length.py**: Validates line length consistency across tools
- **using_py_project_toml.py**: Ensures pyproject.toml usage
- **aggregation.py**: Orchestrates all checks and collects results

### 3. CLI (`pyvelocity/cli.py`)
- Click-based command-line interface
- Coordinates configuration loading and check execution
- Provides user-friendly output with emoji support

## Configuration

The tool can be configured via pyproject.toml:
```toml
[tool.pyvelocity]
filter = ["line-length"]  # Ignore specific checks
```

## Code Patterns

- All configuration tools inherit from base classes in their respective directories
- Each check returns a `Result` object with `is_ok` boolean and optional message
- Configuration files are parsed through a factory pattern in `sections/factory.py`
- The project uses strict typing with mypy and comprehensive linting with multiple tools