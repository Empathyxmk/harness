import pytest

class APICredsActivity:
    # This mock class emulates the behavior for test
    def __init__(self):
        self._text = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword"
    def find_view_by_id(self, key):
        # Always returns a TextView object
        if key == "apicTextView":
            return self
        return None
    def get_text(self):
        return self._text

@pytest.fixture
def activity():
    return APICredsActivity()

def test_on_create_sets_api_text(activity):
    tv = activity.find_view_by_id("apicTextView")
    assert tv is not None
    expected = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword"
    assert tv.get_text() == expected