"""Tests for ReadMe file configuration."""

from pathlib import Path

import pytest

from pyvelocity.configurations.files.readme import ReadMe


class TestReadMe:
    """Test for ReadMe file configuration."""

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_name_property() -> None:
        """Tests the name property returns README.md."""
        readme_path = Path("README.md")
        readme_path.write_text("# Test", encoding="utf-8")

        readme = ReadMe(readme_path)
        assert readme.name == "README.md"

    @staticmethod
    @pytest.mark.usefixtures("ch_tmp_path")
    def test_has_badge_method() -> None:
        """Tests the generic has_badge method."""
        content = "This contains a test badge"
        readme_path = Path("README.md")
        readme_path.write_text(content, encoding="utf-8")

        readme = ReadMe(readme_path)
        assert readme.has_badge("test badge") is True
        assert readme.has_badge("missing badge") is False
