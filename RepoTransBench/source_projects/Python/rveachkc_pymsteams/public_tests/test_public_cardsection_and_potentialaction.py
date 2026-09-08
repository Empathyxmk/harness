import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest

from pymsteams import cardsection, potentialaction, TeamsWebhookException

def test_cardsection_basic_public():
    section = cardsection()
    assert section.title("Public Section Title") is section
    assert section.payload["title"] == "Public Section Title"
    assert section.activityTitle("public activity").payload["activityTitle"] == "public activity"
    assert section.activitySubtitle("public subtitle").payload["activitySubtitle"] == "public subtitle"
    assert section.activityImage("https://example.com/img.png").payload["activityImage"] == "https://example.com/img.png"
    assert section.activityText("public text here").payload["activityText"] == "public text here"
    assert section.text("greetings").payload["text"] == "greetings"
    assert section.linkButton("Visit", "https://visit.com").payload["potentialAction"][0]["name"] == "Visit"
    assert section.disableMarkdown().payload["markdown"] is False
    assert section.enableMarkdown().payload["markdown"] is True
    dumped = section.dumpSection()
    assert isinstance(dumped, dict)

def test_cardsection_addFact_and_addImage_public():
    section = cardsection()
    section.addFact("fact_one", "value_one")
    assert section.payload["facts"] == [{"name": "fact_one", "value": "value_one"}]
    section.addFact("fact_two", "value_two")
    assert len(section.payload["facts"]) == 2
    section.addImage("https://img-server.com/photo1.jpg", "photo title")
    assert section.payload["images"][0]["title"] == "photo title"
    section.addImage("https://img-server.com/photo2.jpg")
    assert "title" not in section.payload["images"][1]

def test_cardsection_fact_and_image_keys_public():
    section = cardsection()
    section.payload["facts"] = [{"name": "init_name", "value": "init_val"}]
    section.addFact("another_name", "another_val")
    assert len(section.payload["facts"]) == 2
    section.payload["images"] = [{"image": "img_obj"}]
    section.addImage("more-img-url")
    assert len(section.payload["images"]) == 2

def test_potentialaction_inputs_and_actions_public():
    pa = potentialaction("PublicAction")
    pa.addInput("TextInput", "pub_input", "Public Input Title", False)
    assert pa.payload["inputs"][0].get("isMultiline", None) is False

    # Testing with another Input type and different id
    pa.addInput("ChoiceInput", "pub_input2", "Public Choice Input", True)
    # addChoice is expected, so simulate its logic:
    if hasattr(pa, 'addChoice'):
        pa.addChoice("pub_display", "pub_value")
        assert "choices" in pa.payload["inputs"][-1]

    pa.addAction("CustomActionType", "ActionPublic", ["https://example.org"])
    assert pa.payload["actions"][0]["@type"] == "CustomActionType"
    pa.addAction("secondtype", "publicaction", ["weburl"], _body="some body here")
    assert pa.payload["actions"][1]["body"] == "some body here"

def test_potentialaction_addOpenURI_and_exceptions_public():
    pa = potentialaction("testopen")
    targets = [{"os": "mobile", "uri": "https://other-url.com/"}]
    res = pa.addOpenURI("OpenOther", targets)
    assert res.payload["targets"] == targets
    with pytest.raises(TypeError):
        pa.addOpenURI("Failer", 12345)

def test_potentialaction_dump_public():
    pa = potentialaction("dumpPA")
    dumped = pa.dumpPotentialAction()
    assert isinstance(dumped, dict)

def test_TeamsWebhookException_repr_public():
    ex = TeamsWebhookException("public fail")
    assert isinstance(ex, Exception)
    assert "public fail" in str(ex)