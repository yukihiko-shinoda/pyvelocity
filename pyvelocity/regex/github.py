"""GitHub-specific regex patterns for PyVelocity."""

import re
import urllib.parse

from pyvelocity.regex.markdown import RegexPatternsMarkDown

GITHUB_BASE_URL = "https://github.com/"


class RegexPatternsGitHub:
    """GitHub-specific regex patterns for badges and URLs."""

    USER = r"[a-zA-Z0-9_.-]+"
    REPOSITORY = r"[a-zA-Z0-9_.-]+"
    REPOSITORY_URL = re.escape(GITHUB_BASE_URL) + rf"{USER}/{REPOSITORY}"
    BASE_URL_ENCODED = (
        re.escape(urllib.parse.quote_plus(GITHUB_BASE_URL))
        + USER
        + re.escape(urllib.parse.quote_plus("/"))
        + REPOSITORY
    )

    @classmethod
    def workflow_badge(cls, workflow_name: str) -> str:
        name = workflow_name
        return RegexPatternsMarkDown.badge_pattern(name, cls.url_workflow_badge(name), cls.url_queried_actions(name))

    @classmethod
    def url_workflow_badge(cls, workflow_name: str) -> str:
        return rf"{cls.REPOSITORY_URL}/workflows/{workflow_name}/badge\.svg"

    @classmethod
    def url_queried_actions(cls, workflow_name: str) -> str:
        return rf"{cls.REPOSITORY_URL}/actions\?query=workflow%3A{workflow_name}"

    @classmethod
    def dependabot_badge(cls) -> str:
        return RegexPatternsMarkDown.badge_pattern(
            "Dependabot",
            rf"https://flat\.badgen\.net/github/dependabot/{cls.USER}/{cls.REPOSITORY}\?icon=dependabot",
            rf"{cls.REPOSITORY_URL}/security/dependabot",
        )
