import pytest
import cas

def test_extra_error_type_public():
    # Different error message
    x = cas.CASError("extra public error example")
    assert "extra" in str(x)
    assert isinstance(x, cas.CASError)

def test_extra_logout_mixin_invalid_xml_public():
    # Use different bad xml
    invalid_xml = "some completely invalid {{{"
    result = cas.SingleLogoutMixin.get_saml_slos(invalid_xml)
    assert result is None

def test_extra_logout_mixin_valid_xml_public():
    valid_xml = '''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>EXTRA-222-SLO</samlp:SessionIndex></samlp:LogoutRequest>'''
    result = cas.SingleLogoutMixin.get_saml_slos(valid_xml)
    assert len(result) == 1
    assert result[0].text == "EXTRA-222-SLO"