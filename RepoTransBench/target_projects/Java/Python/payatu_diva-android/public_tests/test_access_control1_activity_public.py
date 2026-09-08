import pytest

class AccessControl1Activity:
    def __init__(self):
        self.ac1ViewCredsBtn = True

    def find_view_by_id(self, key):
        if key == "ac1ViewCredsBtn":
            return self.ac1ViewCredsBtn
        return None

def test_activity_starts_and_layout_public():
    activity = AccessControl1Activity()
    assert activity.find_view_by_id("ac1ViewCredsBtn") is not None