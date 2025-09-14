"""Qlty-specific regex patterns for PyVelocity."""

from pyvelocity.regex.github import RegexPatternsGitHub
from pyvelocity.regex.markdown import RegexPatternsMarkDown


class RegexPatternsQlty:
    """Qlty-specific regex patterns for code quality badges."""

    PROJECT_ID = r"[a-zA-Z0-9_.-]+"
    URL_PROJECT_PAGE = (
        rf"https://qlty\.sh/gh/{RegexPatternsGitHub.USER}/{RegexPatternsGitHub.REPOSITORY}/projects/{PROJECT_ID}"
    )
    URL_COVERAGE_BADGE = rf"{URL_PROJECT_PAGE}/coverage\.svg"
    URL_MAINTAINABILITY_BADGE = rf"{URL_PROJECT_PAGE}/maintainability\.svg"

    @classmethod
    def coverage_badge(cls) -> str:
        return RegexPatternsMarkDown.badge_pattern("Code Coverage", cls.URL_COVERAGE_BADGE, cls.URL_PROJECT_PAGE)

    @classmethod
    def maintainability_badge(cls) -> str:
        return RegexPatternsMarkDown.badge_pattern(
            "Maintainability",
            cls.URL_MAINTAINABILITY_BADGE,
            cls.URL_PROJECT_PAGE,
        )
