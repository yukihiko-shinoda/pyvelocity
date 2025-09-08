"""Tests for configurations files sections __init__.py."""

from pyvelocity.configurations.files import ConfigurationFile
from pyvelocity.configurations.files.sections import WhereFile
from pyvelocity.configurations.files.sections.black import Black


def test_where_file_str_without_node(mock_config_file: ConfigurationFile) -> None:
    """Test WhereFile.__str__ when node is None."""
    where_file = WhereFile(mock_config_file, Black, None)  # node=None to trigger line 49
    result = str(where_file)
    assert result == "test.toml black"
