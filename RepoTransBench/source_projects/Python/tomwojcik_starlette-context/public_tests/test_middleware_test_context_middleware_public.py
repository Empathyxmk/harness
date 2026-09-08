import pytest
from starlette.requests import Request

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware


@pytest.mark.asyncio
async def test_set_context_method_public(
    mocked_request: Request,
    mocked_middleware: ContextMiddleware,
):
    # Use the UserAgentPlugin for a different plugin from the original test.
    mocked_middleware.plugins = [plugins.UserAgentPlugin()]
    # The UserAgentPlugin retrieves the user-agent from the request header.
    ua = mocked_request.headers.get(HeaderKeys.user_agent)
    expected = {plugins.UserAgentPlugin.key: ua}
    assert expected == await mocked_middleware.set_context(mocked_request)