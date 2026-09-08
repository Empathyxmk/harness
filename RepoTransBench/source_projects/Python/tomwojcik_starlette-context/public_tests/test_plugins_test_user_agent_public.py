import pytest
from starlette.datastructures import Headers
from starlette_context.plugins import UserAgentPlugin


def test_public_plugin_name_is_correct():
    # Use different assertion than in private tests
    assert UserAgentPlugin().name == "user_agent"


def test_user_agent_extraction_public():
    plugin = UserAgentPlugin()
    ua = "SpecialPublicUserAgent/6.7"
    headers = Headers({"User-Agent": ua})
    assert plugin.process_request(headers) == ua


def test_user_agent_missing_returns_none_public():
    plugin = UserAgentPlugin()
    headers = Headers({})
    assert plugin.process_request(headers) is None