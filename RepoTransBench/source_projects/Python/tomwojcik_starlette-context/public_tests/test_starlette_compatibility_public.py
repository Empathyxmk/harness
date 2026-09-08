"""
Public tests to ensure compatibility with the latest Starlette version, using different test data.
"""

import importlib.metadata

import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)


@pytest.fixture
def starlette_version():
    """
    Get the installed Starlette version.
    """
    return importlib.metadata.version("starlette")


def test_starlette_version_major(starlette_version):
    """
    Public: Check that Starlette version's minor version is a digit.
    """
    minor = starlette_version.split(".")[1]
    assert minor.isdigit()


@pytest.fixture
def public_context_app():
    """
    Create a test application with ContextMiddleware and different context key/value.
    """

    async def homepage(request):
        context["public_key"] = "public_value"
        return JSONResponse({"context": context.data})

    app = Starlette(routes=[Route("/", homepage)])

    app.add_middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    return app


@pytest.fixture
def public_raw_context_app():
    """
    Create a test application with RawContextMiddleware and different context key/value.
    """

    async def homepage(request):
        context["another_public_key"] = "another_public_value"
        return JSONResponse({"context": context.data})

    app = Starlette(routes=[Route("/", homepage)])

    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    return app


def test_context_middleware_public_initialization(public_context_app):
    """
    Public test: ContextMiddleware initializes and sets different key/value.
    """
    with TestClient(public_context_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK

        data = response.json()["context"]
        assert "public_key" in data
        assert data["public_key"] == "public_value"
        assert plugins.RequestIdPlugin.key in data
        assert plugins.CorrelationIdPlugin.key in data


def test_raw_context_middleware_public_initialization(public_raw_context_app):
    """
    Public test: RawContextMiddleware initializes with different key/value.
    """
    with TestClient(public_raw_context_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK

        data = response.json()["context"]
        assert "another_public_key" in data
        assert data["another_public_key"] == "another_public_value"
        assert plugins.RequestIdPlugin.key in data
        assert plugins.CorrelationIdPlugin.key in data


def test_public_middleware_response_headers(public_raw_context_app):
    """
    Public: Middleware adds expected headers to response.
    """
    with TestClient(public_raw_context_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK

        # Check that the expected headers are set in the response
        assert plugins.RequestIdPlugin.key.lower() in response.headers
        assert plugins.CorrelationIdPlugin.key.lower() in response.headers