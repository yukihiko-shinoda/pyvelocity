"""Shields.io-specific regex patterns for PyVelocity."""

from pyvelocity.regex.github import RegexPatternsGitHub
from pyvelocity.regex.markdown import RegexPatternsMarkDown
from pyvelocity.regex.pypi import RegexPatternsPyPI


class RegexPatternsShieldsIO:
    """Shields.io-specific regex patterns for social media badges."""

    @classmethod
    def x_badge(cls) -> str:
        return RegexPatternsMarkDown.badge_pattern(
            "X URL",
            rf"https://img\.shields\.io/twitter/url\?style=social&url={RegexPatternsGitHub.BASE_URL_ENCODED}",
            rf"https://x\.com/intent/post\?text=[^&]*&url={RegexPatternsPyPI.BASE_URL_ENCODED}&hashtags=python",
        )
