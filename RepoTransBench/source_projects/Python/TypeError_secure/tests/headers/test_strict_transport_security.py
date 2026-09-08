import pytest
from secure.headers.strict_transport_security import StrictTransportSecurity

def test_default_header_value():
    sts = StrictTransportSecurity()
    assert 'max-age' in sts.header_value

def test_set_and_clear_directives():
    sts = StrictTransportSecurity()
    sts.max_age(1234)
    assert "max-age=1234" in sts.header_value
    sts.include_subdomains()
    assert "includeSubDomains" in sts.header_value
    sts.preload()
    assert "preload" in sts.header_value
    val = sts.header_value
    # Test all directives present
    assert "max-age=1234" in val and "includeSubDomains" in val and "preload" in val
    # Clear sets to default
    sts.clear()
    assert sts.header_value == "max-age=31536000"

def test_set_custom_value():
    sts = StrictTransportSecurity()
    sts.max_age(1).include_subdomains()
    sts.set("something-custom")
    assert sts.header_value == "something-custom"

def test_no_duplicate_directives():
    sts = StrictTransportSecurity()
    sts.include_subdomains().include_subdomains()
    assert sts.header_value.count('includeSubDomains') == 1