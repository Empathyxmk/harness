"""Public tests for the cas protocol-related code - different data than private tests"""
import cas
import pytest
from pytest import fixture

# get_login_url tests with different URLs and parameters
def test_login_url_helper_public():
    client = cas.CASClientBase(
                        renew=True,
                        extra_login_params=False,
                        server_url='https://cas.otherdomain.org/auth/',
                        service_url='https://anotherdomain.org/app/'
                    )
    actual = client.get_login_url()
    expected = 'https://cas.otherdomain.org/auth/login?service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F&renew=true'

    assert actual == expected

def test_login_url_helper_with_extra_params_public():
    client = cas.CASClientBase(
                        renew=False,
                        extra_login_params={'foo': 'bar', 'baz': '5678'},
                        server_url='https://cas.otherdomain.org/auth/',
                        service_url='https://anotherdomain.org/app/'
                    )
    actual = client.get_login_url()
    # Check presence of all params
    assert 'service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F' in actual
    assert 'foo=bar' in actual
    assert 'baz=5678' in actual
    assert actual.startswith('https://cas.otherdomain.org/auth/login?')

def test_login_url_helper_with_renew_public():
    client = cas.CASClientBase(
                        renew=True,
                        extra_login_params=None,
                        server_url='https://cas.otherdomain.org/auth/',
                        service_url='https://anotherdomain.org/app/'
                    )
    actual = client.get_login_url()
    assert 'renew=true' in actual
    assert 'service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F' in actual

@fixture
def logout_client_v1_public():
    return cas.CASClient(
        version='1',
        server_url='https://cas.logouttest.org/sso/'
    )

@fixture
def logout_client_v2_public():
    return cas.CASClient(
        version='2',
        server_url='https://cas.logouttest.org/sso/'
    )

@fixture
def logout_client_v3_public():
    return cas.CASClient(
        version='3',
        server_url='https://cas.logouttest.org/sso/'
    )

def test_logout_url_public(logout_client_v3_public):
    actual = logout_client_v3_public.get_logout_url()
    expected = 'https://cas.logouttest.org/sso/logout'
    assert actual == expected

def test_v1_logout_url_with_redirect_public(logout_client_v1_public):
    actual = logout_client_v1_public.get_logout_url(
                redirect_url='https://anotherdomain.org/goodbye/'
            )
    expected = 'https://cas.logouttest.org/sso/logout?url=https%3A%2F%2Fanotherdomain.org%2Fgoodbye%2F'
    assert actual == expected

def test_v2_logout_url_with_redirect_public(logout_client_v2_public):
    actual = logout_client_v2_public.get_logout_url(
                redirect_url='https://anotherdomain.org/goodbye/'
            )
    expected = 'https://cas.logouttest.org/sso/logout?url=https%3A%2F%2Fanotherdomain.org%2Fgoodbye%2F'
    assert actual == expected

def test_v3_logout_url_with_redirect_public(logout_client_v3_public):
    actual = logout_client_v3_public.get_logout_url(
                redirect_url='https://anotherdomain.org/goodbye/'
            )
    expected = 'https://cas.logouttest.org/sso/logout?service=https%3A%2F%2Fanotherdomain.org%2Fgoodbye%2F'
    assert actual == expected

def test_v3_logout_url_without_redirect_public(logout_client_v3_public):
    actual = logout_client_v3_public.get_logout_url()
    expected = 'https://cas.logouttest.org/sso/logout'
    assert actual == expected


@fixture
def client_v3_public():
    return cas.CASClient(
        version='3',
        server_url='https://cas.mysite.org/sso/',
        service_url='https://mysite.org/home')

SUCCESS_RESPONSE_PUBLIC = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>public_user@domain.org</cas:user></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_cas3_basic_successful_response_verification_public(client_v3_public):
    user, attributes, pgtiou = client_v3_public.verify_response(SUCCESS_RESPONSE_PUBLIC)

    assert user == 'public_user@domain.org'
    assert not attributes
    assert not pgtiou

SUCCESS_RESPONSE_WITH_ATTRIBUTES_PUBLIC = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>public_user@domain.org</cas:user><cas:attributes><cas:alpha>xyz</cas:alpha><cas:beta>9999</cas:beta></cas:attributes></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_cas3_successful_response_verification_with_attributes_public(client_v3_public):
    user, attributes, pgtiou = client_v3_public.verify_response(SUCCESS_RESPONSE_WITH_ATTRIBUTES_PUBLIC)

    assert user == 'public_user@domain.org'
    assert not pgtiou
    assert attributes['alpha'] == 'xyz'
    assert attributes['beta'] == '9999'

SUCCESS_RESPONSE_WITH_PGTIOU_PUBLIC = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>public_user@domain.org</cas:user><cas:proxyGrantingTicket>PGTIOU-54321-aaaa</cas:proxyGrantingTicket></cas:authenticationSuccess></cas:serviceResponse>
"""
def test_successful_response_verification_with_pgtiou_public(client_v3_public):
    user, attributes, pgtiou = client_v3_public.verify_response(SUCCESS_RESPONSE_WITH_PGTIOU_PUBLIC)

    assert user == 'public_user@domain.org'
    assert pgtiou == 'PGTIOU-54321-aaaa'

FAILURE_RESPONSE_PUBLIC = """<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationFailure code="INVALID_TICKET">service ticket ST-555-ERRTEST has been revoked</cas:authenticationFailure></cas:serviceResponse>
"""
def test_unsuccessful_response_public(client_v3_public):
    user, attributes, pgtiou = client_v3_public.verify_response(FAILURE_RESPONSE_PUBLIC)
    assert user is None
    assert not pgtiou
    assert not attributes

# get_proxy_url public test: use different TGT and service_url
def test_proxy_url_public(client_v3_public):
    tgt = 'tgt-PUBLIC-5678'
    proxy_url_string = client_v3_public.get_proxy_url(tgt)
    # This tests proxy URL formatting
    expected_base = 'https://cas.mysite.org/sso/proxy?'
    assert proxy_url_string.startswith(expected_base)
    assert 'pgt=tgt-PUBLIC-5678' in proxy_url_string
    assert 'targetService=https%3A%2F%2Fmysite.org%2Fhome' in proxy_url_string