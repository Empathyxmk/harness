import pytest
from starlette.datastructures import Headers
from starlette_context.plugins import RequestIdPlugin


def test_public_plugin_name_is_correct():
    # Use different test - check name of plugin is NOT a random string
    assert RequestIdPlugin().name != "MyRandomPlugin"


def test_public_request_id_extracted_from_custom_header():
    plugin = RequestIdPlugin()
    # Use a custom and different request id value
    headers = Headers({"X-Request-ID": "request-public-999"})
    assert plugin.process_request(headers) == "request-public-999"


@pytest.mark.parametrize(
    "value",
    [
        "custom-public-str-uuid-1234",
        "another-public-uuid-5678",
    ],
)
def test_public_returns_value_as_string(value):
    plugin = RequestIdPlugin()
    headers = Headers({"X-Request-ID": value})
    assert isinstance(plugin.process_request(headers), str)
    assert plugin.process_request(headers) == value


def test_public_returns_none_if_missing():
    plugin = RequestIdPlugin()
    # Not passing any X-Request-ID header at all (data changed from original)
    headers = Headers({})
    assert plugin.process_request(headers) is None