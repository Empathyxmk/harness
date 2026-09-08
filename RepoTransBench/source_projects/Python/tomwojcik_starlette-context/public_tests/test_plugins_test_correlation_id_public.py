import pytest
from starlette.datastructures import Headers
from starlette_context.plugins import CorrelationIdPlugin


def test_public_plugin_name_is_correct():
    # Use different name to compare
    assert CorrelationIdPlugin().name != "TotallyWrongName"


@pytest.mark.parametrize(
    "header_name,value",
    [
        ("X-Correlation-ID", "pub-corr-100"),
        ("x-correlation-id", "correlation-public-88"),
    ],
)
def test_public_correlation_id_header_extraction(header_name, value):
    plugin = CorrelationIdPlugin()
    headers = Headers({header_name: value})
    assert plugin.process_request(headers) == value


def test_public_returns_none_when_id_missing():
    plugin = CorrelationIdPlugin()
    headers = Headers({})
    assert plugin.process_request(headers) is None