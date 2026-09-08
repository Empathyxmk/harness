import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest

from pymsteams import connectorcard, TeamsWebhookException, cardsection

def test_connectorcard_init_and_summary():
    url = "https://outlook.office.com/webhook/dummy_url"
    c = connectorcard(url)
    assert c.hookurl == url
    c.text("Hello World")
    assert c.payload["text"] == "Hello World"
    c.summary("Summary")
    assert c.payload["summary"] == "Summary"
    c.title("A title here")
    assert c.payload["title"] == "A title here"
    c.color("123456")
    assert c.payload["themeColor"] == "123456"
    # Instead of c.activityImage, c is not supposed to have this, so only cardsection does.
    section = cardsection()
    section.activityImage("https://i/image.png")
    assert section.payload["activityImage"] == "https://i/image.png"
    section.activityTitle("Do Something")
    assert section.payload["activityTitle"] == "Do Something"
    section.activitySubtitle("subtitle")
    assert section.payload["activitySubtitle"] == "subtitle"
    section.activityText("text activity")
    assert section.payload["activityText"] == "text activity"
    payload = c.payload
    assert isinstance(payload, dict)
    # Use .json() instead of missing/toJSON method for payload serialization
    import json
    dumped = json.dumps(payload)
    assert isinstance(dumped, str)

def test_connectorcard_addSection():
    url = "https://outlook.office.com/webhook/dummy_url"
    c = connectorcard(url)
    section = cardsection()
    section.title("Section1 Title")
    c.addSection(section)
    assert "sections" in c.payload
    assert c.payload["sections"][0]["title"] == "Section1 Title"

def test_connectorcard_addPotentialAction():
    url = "https://outlook.office.com/webhook/dummy_url"
    c = connectorcard(url)
    from pymsteams import potentialaction
    pa = potentialaction("openUri")
    c.addPotentialAction(pa)
    assert "potentialAction" in c.payload
    assert c.payload["potentialAction"][0]["@type"] == "ActionCard"

def test_connectorcard_send_request(monkeypatch):
    url = "https://outlook.office.com/webhook/dummy_url"

    class DummyResponse:
        def __init__(self, code): self.status_code = code
        @property
        def text(self): return "dummy"
    def dummy_post(*args, **kwargs): return DummyResponse(200)

    c = connectorcard(url)
    c.text("posting")

    import pymsteams
    monkeypatch.setattr(pymsteams.requests, "post", dummy_post)
    c.send()  # Should "post" and not raise

def test_connectorcard_send_request_error(monkeypatch):
    url = "https://outlook.office.com/webhook/dummy_url"

    class DummyResponse:
        def __init__(self, code): self.status_code = code
        @property
        def text(self): return "dummy-error"
    def dummy_post(*args, **kwargs): return DummyResponse(400)

    c = connectorcard(url)
    c.text("posting error")

    import pymsteams
    monkeypatch.setattr(pymsteams.requests, "post", dummy_post)
    with pytest.raises(TeamsWebhookException):
        c.send()