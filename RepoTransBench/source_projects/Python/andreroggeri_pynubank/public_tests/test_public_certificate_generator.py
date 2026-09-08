import json
from unittest.mock import MagicMock

import pytest
from requests import Response

from pynubank import NuException, MockHttpClient
from pynubank.utils.certificate_generator import CertificateGenerator
from pynubank.utils.discovery import Discovery

headers_public = {
    'WWW-Authenticate': 'device-authorization encrypted-code="def456", sent-to="jane@public.com"'
}

def fake_update_proxy_public(self: Discovery):
    self.proxy_list_app_url = {
        'gen_certificate': 'https://other-url/gen-cert',
    }

def mock_response_public(content=None, return_headers=None, status_code=200):
    response = Response()
    response.status_code = status_code
    response.headers = return_headers
    if content:
        response._content = json.dumps(content).encode()
    return response

def test_request_code_fails_when_status_code_is_403_public(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(status_code=403)))
    generator = CertificateGenerator('987654321', 'password1', '4321', http_client=http)

    with pytest.raises(NuException) as ex:
        email = generator.request_code()
        assert ex is not None
        assert email is None

def test_request_code_fails_when_no_authenticate_header_public(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(None, {}, 401)))
    generator = CertificateGenerator('987654321', 'password1', '4321', http_client=http)

    with pytest.raises(NuException) as ex:
        email = generator.request_code()
        assert ex is not None
        assert email is None

def test_request_code_public(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(None, headers_public, 401)))
    generator = CertificateGenerator('987654321', 'password1', '4321', http_client=http)

    email = generator.request_code()
    assert email == 'jane@public.com'
    assert generator.encrypted_code == 'def456'

def test_exchange_certs_fails_without_request_code_public(monkeypatch):
    http = MockHttpClient()
    generator = CertificateGenerator('987654321', 'password1', '4321', http_client=http)

    with pytest.raises(NuException) as ex:
        cert1, cert2 = generator.exchange_certs('4321')
        assert cert1 is None
        assert cert2 is None
        assert ex is not None

def test_exchange_cert_fails_with_status_code_403_public(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(None, headers_public, 401)))
    generator = CertificateGenerator('987654321', 'password1', '4321', http_client=http)

    generator.request_code()

    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(None, headers_public, 403)))
    with pytest.raises(NuException) as ex:
        cert1, cert2 = generator.exchange_certs('4321')
        assert cert1 is None
        assert cert2 is None
        assert ex is not None

@pytest.fixture
def gen_certificate_return_public():
    return {
        "certificate": "fake_cert_public",
        "private_key": "fake_private_key_public"
    }

def test_exchange_certs_public(monkeypatch, gen_certificate_return_public):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(None, headers_public, 401)))
    generator = CertificateGenerator('987654321', 'password1', '4321', http_client=http)

    generator.request_code()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response_public(gen_certificate_return_public, headers_public, 200)))
    cert1, cert2 = generator.exchange_certs('4321')
    assert cert1 is not None
    assert cert2 is not None