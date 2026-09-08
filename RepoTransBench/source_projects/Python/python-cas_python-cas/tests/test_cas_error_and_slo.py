import pytest
from cas import CASError, SingleLogoutMixin

def test_caserror_str():
    err = CASError("fail")
    assert isinstance(err, CASError)
    assert str(err) == "fail"

def test_slo_get_saml_slos_invalid_xml():
    # Invalid XML should return None
    invalid_xml = "<bad<xml>"
    result = SingleLogoutMixin.get_saml_slos(invalid_xml)
    assert result is None

def test_slo_get_saml_slos_valid_xml():
    valid_xml = '''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-123-SLO</samlp:SessionIndex></samlp:LogoutRequest>'''
    result = SingleLogoutMixin.get_saml_slos(valid_xml)
    assert len(result) == 1

def test_slo_verify_logout_request_true():
    # The SessionIndex matches ticket
    valid_ticket = "ST-123-SLO"
    valid_xml = f'''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>{valid_ticket}</samlp:SessionIndex></samlp:LogoutRequest>'''
    assert SingleLogoutMixin.verify_logout_request(valid_xml, valid_ticket)

def test_slo_verify_logout_request_false():
    # The SessionIndex does not match ticket
    valid_xml = '''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-456</samlp:SessionIndex></samlp:LogoutRequest>'''
    ticket = "ST-123"
    assert not SingleLogoutMixin.verify_logout_request(valid_xml, ticket)

def test_slo_verify_logout_request_invalid_xml():
    # Invalid XML should return False
    assert not SingleLogoutMixin.verify_logout_request("<bad<xml>", "anyticket")