"""Tests for configurations files sections factory.py."""

from pyvelocity.configurations.files import ConfigurationFile
from pyvelocity.configurations.files.sections.black import Black
from pyvelocity.configurations.files.sections.factory import SectionFactory


def test_section_factory_create_configuration_parameter(mock_config_file: ConfigurationFile) -> None:
    """Test SectionFactory.create_configuration_parameter method directly."""
    config_dict = {"line-length": "88"}

    factory = SectionFactory(mock_config_file, None, Black, config_dict)
    param = factory.create_configuration_parameter("line-length")

    assert param.name == "line-length"
    assert param.value == "88"
    assert str(param.where) == "test.toml black"
