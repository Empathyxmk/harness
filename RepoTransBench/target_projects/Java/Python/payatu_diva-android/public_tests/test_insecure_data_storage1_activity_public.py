import pytest

class InsecureDataStorage1Activity:
    def __init__(self):
        self.shared_prefs = {}
        self.user = ""
        self.password = ""
    def find_view_by_id(self, key):
        if key == "ids1Usr":
            return self._UserText(self, "user")
        if key == "ids1Pwd":
            return self._UserText(self, "password")
        return None
    def save_credentials(self, _):
        self.shared_prefs["user"] = self.user
        self.shared_prefs["password"] = self.password
    def get_shared_preferences(self):
        return self.shared_prefs
    class _UserText:
        def __init__(self, parent, attr):
            self.parent = parent
            self.attr = attr
        def set_text(self, text):
            setattr(self.parent, self.attr, text)
        def get_text(self):
            return getattr(self.parent, self.attr)

@pytest.fixture
def activity():
    return InsecureDataStorage1Activity()

def test_save_credentials_saves_to_prefs_public(activity):
    user = activity.find_view_by_id("ids1Usr")
    passwd = activity.find_view_by_id("ids1Pwd")
    user.set_text("publicuser")
    passwd.set_text("publicpass")
    activity.save_credentials(None)
    prefs = activity.get_shared_preferences()
    assert prefs["user"] == "publicuser"
    assert prefs["password"] == "publicpass"