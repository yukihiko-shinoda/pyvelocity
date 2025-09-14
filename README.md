# pyvelocity

[![Test](https://github.com/yukihiko-shinoda/pyvelocity/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/pyvelocity/actions?query=workflow%3ATest)
[![CodeQL](https://github.com/yukihiko-shinoda/pyvelocity/workflows/CodeQL/badge.svg)](https://github.com/yukihiko-shinoda/pyvelocity/actions?query=workflow%3ACodeQL)
[![Code Coverage](https://qlty.sh/gh/yukihiko-shinoda/projects/pyvelocity/coverage.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/pyvelocity)
[![Maintainability](https://qlty.sh/gh/yukihiko-shinoda/projects/pyvelocity/maintainability.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/pyvelocity)
[![Dependabot](https://flat.badgen.net/github/dependabot/yukihiko-shinoda/pyvelocity?icon=dependabot)](https://github.com/yukihiko-shinoda/pyvelocity/security/dependabot)
[![Python versions](https://img.shields.io/pypi/pyversions/pyvelocity.svg)](https://pypi.org/project/pyvelocity)
[![X URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Fpyvelocity)](https://x.com/intent/post?text=PyVelocity&url=https%3A%2F%2Fpypi.org%2Fproject%2Fpyvelocity%2F&hashtags=python)

Automates task to check configurations about Python project to follow best practices to increase development velocity.

## Attention

The development status of this package is Beta now. It may not be able to keep backward compatibility. Be careful to use, especially for CI.

## Available Checks

PyVelocity performs the following checks to ensure your Python project follows best practices:

### Core Configuration Checks

#### `line-length`

Ensures consistent line length settings across all Python development tools:

- **docformatter**: `wrap-descriptions` and `wrap-summaries`
- **isort**: `line_length`
- **Black**: `line-length`
- **flake8**: `max-line-length`
- **Ruff**: `line-length`
- **Pylint**: `format.max-line-length`

#### `using-py-project-toml`

Verifies that your project uses `pyproject.toml` for configuration instead of legacy files.

#### `legacy-setup-files`

Ensures that neither `setup.py` nor `setup.cfg` files are present in the project. These legacy configuration files should be replaced with `pyproject.toml` for modern Python packaging.

### Project Metadata Checks

#### `classifiers`

Validates that Python version classifiers in `pyproject.toml` are consistent with the `requires-python` field. For example, if `requires-python = ">=3.9"`, the classifiers should include all supported Python versions from 3.9 to the latest available.

#### `requires-python`

Ensures that the `requires-python` field supports the latest stable Python version to encourage adoption of newer Python features and improvements.

#### `readme`

Checks that the `readme` field is properly configured as `"README.md"` in the `[project]` section of `pyproject.toml`.

#### `keywords`

Ensures that at least one keyword is defined in the `[project]` section of `pyproject.toml`. Keywords help improve package discoverability on PyPI and other package indexes.

### Package Configuration Checks

#### `zip-safe-false`

Verifies that `zip-safe = false` is set in the `[tool.setuptools]` section to prevent issues with modern Python packaging.

#### `typed`

Ensures proper type hint configuration for typed packages:

- Validates that `tool.setuptools.package-data` includes `"*" = ["py.typed"]`
- Checks for the presence of `py.typed` files in package directories
- Requires the `"Typing :: Typed"` classifier in project metadata

This check helps ensure your package properly declares itself as typed for better IDE support and type checking.

## Quickstart

### 1. Install

```console
pip install pyvelocity
```

### 2. Run command

Run the following command in your project directory (where `pyproject.toml` exists):

```console
pyvelocity
```

#### Expected Output

**Success**: If all checks pass, you'll see:

```console
Looks high velocity! ⚡️ 🚄 ✨
```

**Issues Found**: If checks fail, PyVelocity will display specific error messages and exit with a non-zero status code, making it perfect for CI/CD integration.

<!-- markdownlint-disable no-trailing-punctuation -->
## How do I...
<!-- markdownlint-enable no-trailing-punctuation -->

### Ignore specific check?

You can configure PyVelocity to ignore specific checks by adding them to the `filter` list in `pyproject.toml`. For example, to ignore the `line-length` and `typed` checks:

```toml
[tool.pyvelocity]
filter = [
  "line-length",
  "typed"
]
```

Available check IDs:

- `line-length`
- `using-py-project-toml`
- `legacy-setup-files`
- `classifiers`
- `requires-python`
- `readme`
- `keywords`
- `zip-safe-false`
- `typed`

## Credits

This package was created with [Cookiecutter] and the [yukihiko-shinoda/cookiecutter-pypackage] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[yukihiko-shinoda/cookiecutter-pypackage]: https://github.com/yukihiko-shinoda/cookiecutter-pypackage
