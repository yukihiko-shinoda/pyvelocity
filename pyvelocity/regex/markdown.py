"""Markdown and general regex patterns for PyVelocity."""

# Prevents docformatter from collapsing the two blank lines before the class
# (it would reduce them to one, then ruff format would add one back every lint run).
# - The docformatter removes blank line against PEP8 (conflicts with Ruff (Black)) · Issue #350 · PyCQA/docformatter
#   https://github.com/PyCQA/docformatter/issues/350


class RegexPatternsMarkDown:
    """Collection of reusable regex patterns used throughout the codebase."""

    # Python version specification patterns
    GREATER_EQUAL_VERSION = r">=(\d+)\.(\d+)"
    LESS_THAN_VERSION = r"<(\d+)\.(\d+)"
    COMPATIBLE_RELEASE_VERSION = r"~=(\d+)\.(\d+)"
    EXACT_VERSION = r"^(\d+)\.(\d+)$"

    # Python classifier patterns
    PYTHON_VERSION_CLASSIFIER = r"^Programming Language :: Python :: (\d+\.\d+)$"

    @staticmethod
    def badge_pattern(alt_text: str, image_url_pattern: str, link_url_pattern: str) -> str:
        """Generate a regex pattern to match markdown badge format.

        Args:
            alt_text: The alt text for the badge (e.g., "Test", "CodeQL")
            image_url_pattern: Regex pattern for the badge image URL
            link_url_pattern: Regex pattern for the badge link URL

        Returns:
            Complete regex pattern to match the badge in markdown format
        """
        return rf"\[!\[{alt_text}\]\({image_url_pattern}\)\]\({link_url_pattern}\)"
