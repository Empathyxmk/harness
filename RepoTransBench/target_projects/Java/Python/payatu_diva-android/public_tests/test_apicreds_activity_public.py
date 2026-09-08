import pytest

class APICredsActivity:
    def __init__(self):
        self._text = "API Key: abcPUBLIC987\nAPI User name: publicuser\nAPI Password: publicpass"
    def find_view_by_id(self, key):
        if key == "apicTextView":
            return self
        return None
    def get_text(self):
        return self._text

@pytest.fixture
def activity():
    return APICredsActivity()

def test_on_create_sets_api_text_public(activity):
    tv = activity.find_view_by_id("apicTextView")
    assert tv is not None
    not_expected = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword"
    actual = tv.get_text()
    assert not_expected != actual
    assert "API Key:" in actual
    assert "API User name:" in actual
    assert "API Password:" in actual
    assert "123secretapikey123" not in actual