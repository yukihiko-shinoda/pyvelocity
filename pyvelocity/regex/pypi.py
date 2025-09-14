"""PyPI-specific regex patterns for PyVelocity."""

import re
import urllib.parse

from pyvelocity.regex.markdown import RegexPatternsMarkDown

PYPI_BASE_URL = "https://pypi.org/project/"


class RegexPatternsPyPI:
    """PyPI-specific regex patterns for packages and badges."""

    PACKAGE_NAME = r"[a-zA-Z0-9_.-]+"
    BASE_URL = re.escape(PYPI_BASE_URL) + PACKAGE_NAME
    BASE_URL_ENCODED = (
        re.escape(urllib.parse.quote_plus(PYPI_BASE_URL)) + PACKAGE_NAME + re.escape(urllib.parse.quote_plus("/"))
    )
    SHIELDS_PYVERSIONS_URL = rf"https://img\.shields\.io/pypi/pyversions/{PACKAGE_NAME}(?:\.svg)?"

    @classmethod
    def python_versions_badge(cls) -> str:
        return RegexPatternsMarkDown.badge_pattern(
            "Python versions",
            cls.SHIELDS_PYVERSIONS_URL,
            rf"{cls.BASE_URL}/?/?",
        )
