import pytest
from starlette.datastructures import Headers
from starlette_context.plugins import ApiKeyPlugin, RequestIdPlugin


def test_public_api_key_plugin_diff_key():
    plugin = ApiKeyPlugin(header_name="Authorization", key="public_api_key")
    headers = Headers({"Authorization": "Token public-key-99"})
    assert plugin.process_request(headers) == "Token public-key-99"
    assert plugin.key == "public_api_key"


def test_plugin_key_customization_public():
    plugin = RequestIdPlugin(header_name="another-header", key="pub_request_id")
    headers = Headers({"another-header": "pub-req-header-1"})
    assert plugin.process_request(headers) == "pub-req-header-1"
    assert plugin.key == "pub_request_id"