import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest

from pymsteams import connectorcard, TeamsWebhookException, cardsection

def test_connectorcard_init_and_summary_public():
    url = "https://somedomain.com/webhook/unique_id"
    c = connectorcard(url)
    assert c.hookurl == url
    c.text("Public Hello Text")
    assert c.payload["text"] == "Public Hello Text"
    c.summary("Public Summary")
    assert c.payload["summary"] == "Public Summary"
    c.title("Some Public Title")
    assert c.payload["title"] == "Some Public Title"
    c.color("ABCDEF")
    assert c.payload["themeColor"] == "ABCDEF"
    section = cardsection()
    section.activityImage("https://images.example.com/pic.png")
    assert section.payload["activityImage"] == "https://images.example.com/pic.png"
    section.activityTitle("Demo Action")
    assert section.payload["activityTitle"] == "Demo Action"
    section.activitySubtitle("demo subtitle")
    assert section.payload["activitySubtitle"] == "demo subtitle"
    section.activityText("some public activity text")
    assert section.payload["activityText"] == "some public activity text"
    payload = c.payload
    assert isinstance(payload, dict)
    import json
    dumped = json.dumps(payload)
    assert isinstance(dumped, str)

def test_connectorcard_addSection_public():
    url = "https://somedomain.com/webhook/other_id"
    c = connectorcard(url)
    section = cardsection()
    section.title("Public Section2 Title")
    c.addSection(section)
    assert "sections" in c.payload
    assert c.payload["sections"][0]["title"] == "Public Section2 Title"

def test_connectorcard_addPotentialAction_public():
    url = "https://somedomain.com/webhook/pa_id"
    c = connectorcard(url)
    from pymsteams import potentialaction
    pa = potentialaction("otherOpenUri")
    c.addPotentialAction(pa)
    assert "potentialAction" in c.payload
    assert c.payload["potentialAction"][0]["@type"] == "ActionCard"

def test_connectorcard_send_request_public(monkeypatch):
    url = "https://somedomain.com/webhook/send_id"

    class DummyResponse:
        def __init__(self, code): self.status_code = code
        @property
        def text(self): return "public-dummy"
    def dummy_post(*args, **kwargs): return DummyResponse(201)

    c = connectorcard(url)
    c.text("another post")

    import pymsteams
    monkeypatch.setattr(pymsteams.requests, "post", dummy_post)
    c.send()  # Should post and not raise

def test_connectorcard_send_request_error_public(monkeypatch):
    url = "https://somedomain.com/webhook/send_error"

    class DummyResponse:
        def __init__(self, code): self.status_code = code
        @property
        def text(self): return "public-dummy-error"
    def dummy_post(*args, **kwargs): return DummyResponse(404)

    c = connectorcard(url)
    c.text("posting error test")

    import pymsteams
    monkeypatch.setattr(pymsteams.requests, "post", dummy_post)
    with pytest.raises(TeamsWebhookException):
        c.send()