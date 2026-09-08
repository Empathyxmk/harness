import pytest
from starlette.datastructures import Headers
from starlette_context.plugins import DateHeaderPlugin
from datetime import datetime, timezone


def test_public_plugin_name_is_correct():
    # Different assertion
    assert DateHeaderPlugin().name.endswith("date")


def test_returns_formatted_date_if_present_public():
    dt = datetime(2014, 2, 3, 5, 6, 7, tzinfo=timezone.utc)
    iso = dt.isoformat()
    plugin = DateHeaderPlugin()
    headers = Headers({"Date": iso})
    assert plugin.process_request(headers) == iso


def test_returns_none_if_no_header_public():
    plugin = DateHeaderPlugin()
    headers = Headers({})
    assert plugin.process_request(headers) is None