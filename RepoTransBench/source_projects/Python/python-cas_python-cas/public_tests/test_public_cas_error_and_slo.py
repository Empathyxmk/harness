import pytest
from cas import CASError, SingleLogoutMixin

def test_caserror_str_public():
    err = CASError("another_fail")
    assert isinstance(err, CASError)
    assert str(err) == "another_fail"

def test_slo_get_saml_slos_invalid_xml_public():
    # Invalid XML should return None
    invalid_xml = "<xml broken"
    result = SingleLogoutMixin.get_saml_slos(invalid_xml)
    assert result is None

def test_slo_get_saml_slos_valid_xml_public():
    valid_xml = '''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-999-SLO</samlp:SessionIndex></samlp:LogoutRequest>'''
    result = SingleLogoutMixin.get_saml_slos(valid_xml)
    assert len(result) == 1

def test_slo_verify_logout_request_true_public():
    # The SessionIndex matches ticket (different ticket)
    valid_ticket = "ST-999-SLO"
    valid_xml = f'''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>{valid_ticket}</samlp:SessionIndex></samlp:LogoutRequest>'''
    assert SingleLogoutMixin.verify_logout_request(valid_xml, valid_ticket)

def test_slo_verify_logout_request_false_public():
    valid_xml = '''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-555</samlp:SessionIndex></samlp:LogoutRequest>'''
    ticket = "ST-999"
    assert not SingleLogoutMixin.verify_logout_request(valid_xml, ticket)

def test_slo_verify_logout_request_invalid_xml_public():
    # Invalid XML should return False
    assert not SingleLogoutMixin.verify_logout_request("<broken <xml>", "otherticket")