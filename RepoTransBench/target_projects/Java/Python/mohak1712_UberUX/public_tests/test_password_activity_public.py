import pytest
from unittest.mock import MagicMock

class PasswordActivity:
    def on_create(self, bundle):
        self.bundle = bundle
        self.created = True

@pytest.fixture
def activity():
    activity = MagicMock(spec=PasswordActivity)
    activity.on_create = PasswordActivity.on_create
    activity.bundle = None
    activity.created = False
    return activity

def test_on_create_executes_without_crash_public(activity):
    bundle = {"public_test_char": "P"}
    activity.on_create(activity, bundle)
    assert activity.created