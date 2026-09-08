import pytest
from fastapi.testclient import TestClient
import sys

from claude_to_chatgpt.app import app

def test_v1_models_route():
    client = TestClient(app)
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    data = resp.json()
    assert "object" in data and "data" in data
    assert data["object"] == "list"
    assert isinstance(data["data"], list)

@pytest.mark.asyncio
async def test_chat_completion_non_stream(monkeypatch):
    # Patch ClaudeAdapter.chat to return a dummy async generator
    from claude_to_chatgpt import app as app_module
    class DummyAdapter:
        async def chat(self, request):
            class DummyGen:
                async def __anext__(self_inner): return {"content": "hi"}
                def __aiter__(self_inner): return self_inner
            return DummyGen()
    monkeypatch.setattr(app_module, "adapter", DummyAdapter())
    client = TestClient(app)
    resp = client.post("/v1/chat/completions", json={"model": "gpt-3.5-turbo-0613", "messages": [], "stream": False})
    assert resp.status_code == 200
    # The response is JSON - dummy, just check it's a dict in our test
    assert isinstance(resp.json(), dict)