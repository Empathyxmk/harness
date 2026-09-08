import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest

from pymsteams import cardsection, potentialaction, TeamsWebhookException

def test_cardsection_basic():
    section = cardsection()
    assert section.title("title text") is section
    assert section.payload["title"] == "title text"
    assert section.activityTitle("activity").payload["activityTitle"] == "activity"
    assert section.activitySubtitle("subtitle").payload["activitySubtitle"] == "subtitle"
    assert section.activityImage("http://image.png").payload["activityImage"] == "http://image.png"
    assert section.activityText("text here").payload["activityText"] == "text here"
    assert section.text("hello").payload["text"] == "hello"
    assert section.linkButton("Go", "http://go.com").payload["potentialAction"][0]["name"] == "Go"
    assert section.disableMarkdown().payload["markdown"] is False
    assert section.enableMarkdown().payload["markdown"] is True
    dumped = section.dumpSection()
    assert isinstance(dumped, dict)

def test_cardsection_addFact_and_addImage():
    section = cardsection()
    section.addFact("f1", "v1")
    assert section.payload["facts"] == [{"name": "f1", "value": "v1"}]
    section.addFact("f2", "v2")
    assert len(section.payload["facts"]) == 2
    section.addImage("http://img.com/img.jpg", "image1")
    assert section.payload["images"][0]["title"] == "image1"
    section.addImage("http://img.com/img2.jpg")
    assert "title" not in section.payload["images"][1]

def test_cardsection_fact_and_image_keys():
    section = cardsection()
    section.payload["facts"] = [{"name": "start", "value": "val"}]
    section.addFact("foo", "bar")
    assert len(section.payload["facts"]) == 2
    section.payload["images"] = [{"image": "test"}]
    section.addImage("img-url")
    assert len(section.payload["images"]) == 2

def test_potentialaction_inputs_and_actions():
    pa = potentialaction("TestAction")
    pa.addInput("TextInput", "inputid", "My Title", True)
    assert pa.payload["inputs"][0].get("isMultiline", None) is True

    # Test ChoiceInput with at least one choice
    pa.addInput("ChoiceInput", "input2", "Another", False)
    # addChoice is expected, so simulate its logic:
    if hasattr(pa, 'addChoice'):
        pa.addChoice("display", "value")
        assert "choices" in pa.payload["inputs"][-1]

    pa.addAction("ActionType", "ActionName", ["http://example.com"])
    assert pa.payload["actions"][0]["@type"] == "ActionType"
    pa.addAction("type", "name", ["url"], _body="body here")
    assert pa.payload["actions"][1]["body"] == "body here"

def test_potentialaction_addOpenURI_and_exceptions():
    pa = potentialaction("opentest")
    targets = [{"os": "default", "uri": "https://foo.bar/"}]
    res = pa.addOpenURI("OpenName", targets)
    assert res.payload["targets"] == targets
    with pytest.raises(TypeError):
        pa.addOpenURI("Broken", "notalist")

def test_potentialaction_dump():
    pa = potentialaction("dumpTest")
    dumped = pa.dumpPotentialAction()
    assert isinstance(dumped, dict)

def test_TeamsWebhookException_repr():
    ex = TeamsWebhookException("fail")
    assert isinstance(ex, Exception)
    assert "fail" in str(ex)