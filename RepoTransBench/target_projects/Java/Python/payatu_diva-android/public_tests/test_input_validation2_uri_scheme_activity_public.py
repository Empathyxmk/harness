import pytest

class EditText:
    def __init__(self):
        self._text = ""
    def set_text(self, value):
        self._text = value
    def get_text(self):
        return self._text

class InputValidation2URISchemeActivity:
    def __init__(self):
        self.input = EditText()
    def find_view_by_id(self, key):
        if key == "issue2Input":
            return self.input
        return None

@pytest.fixture
def activity():
    return InputValidation2URISchemeActivity()

def test_user_input_is_accepted_public(activity):
    input_obj = activity.find_view_by_id("issue2Input")
    public_input = "publicTestInput"
    input_obj.set_text(public_input)
    assert input_obj.get_text() == public_input