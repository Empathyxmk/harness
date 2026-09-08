import pytest

class NeXMLReporterConfig:
    ATTR_TC_NAME = "testName"
    ATTR_TC_SUITES = "suiteName"
    ATTR_AUTHOR = "author"

def test_config_constants_with_different_access_pattern():
    assert NeXMLReporterConfig.ATTR_AUTHOR == "author"
    assert NeXMLReporterConfig.ATTR_TC_NAME == "testName"
    assert NeXMLReporterConfig.ATTR_TC_SUITES == "suiteName"