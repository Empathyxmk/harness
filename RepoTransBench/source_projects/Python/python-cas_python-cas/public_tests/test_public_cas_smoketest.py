import pytest
import cas

def test_smoketest_cas_error_public():
    e = cas.CASError("smoke_public")
    assert str(e) == "smoke_public"

def test_smoketest_slo_public():
    # Check SingleLogoutMixin call with another dummy XML
    logout_xml = '''<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-PUBLIC-777</samlp:SessionIndex></samlp:LogoutRequest>'''
    session_indexes = cas.SingleLogoutMixin.get_saml_slos(logout_xml)
    assert len(session_indexes) == 1
    assert session_indexes[0].text == "ST-PUBLIC-777"

    # Should return True when ticket matches, False otherwise
    assert cas.SingleLogoutMixin.verify_logout_request(logout_xml, "ST-PUBLIC-777") is True
    assert cas.SingleLogoutMixin.verify_logout_request(logout_xml, "ST-PUBLIC-888") is False

def test_smoketest_clientbase_public():
    # Just instantiate and check get_login_url / get_logout_url for another domain
    cl = cas.CASClientBase(
        server_url='https://smoke.cas.org/server/',
        service_url='https://smoke.cas.org/client/',
        renew=True
    )
    url = cl.get_login_url()
    assert url.startswith('https://smoke.cas.org/server/login?')
    assert 'renew=true' in url
    out = cl.get_logout_url()
    assert out == 'https://smoke.cas.org/server/logout'