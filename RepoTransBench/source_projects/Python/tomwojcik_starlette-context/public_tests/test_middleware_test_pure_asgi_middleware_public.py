import pytest
from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import RawContextMiddleware


async def public_index(request: Request) -> JSONResponse:
    # Insert a different key in context than in the original test
    context["public_middle_key"] = "val"
    return JSONResponse(content=context.data)


public_plugins_to_use = (
    plugins.ApiKeyPlugin(),
    plugins.UserAgentPlugin(),
    plugins.DateHeaderPlugin(),
)

public_app = Starlette(
    routes=[
        Route("/", public_index),
    ],
    middleware=[
        Middleware(
            RawContextMiddleware,
            plugins=public_plugins_to_use,
        )
    ],
)


@pytest.fixture
def public_client():
    with TestClient(public_app) as client:
        yield client


def test_valid_request_public(public_client):
    resp = public_client.get("/", headers={"Authorization": "Bearer public"})
    assert resp.status_code == status.HTTP_200_OK

    for plugin in public_plugins_to_use:
        assert plugin.key in resp.text

    assert HeaderKeys.api_key in resp.headers
    assert HeaderKeys.user_agent in resp.headers