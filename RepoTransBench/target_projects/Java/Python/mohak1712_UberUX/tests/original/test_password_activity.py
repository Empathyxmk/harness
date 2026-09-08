import pytest
from unittest.mock import MagicMock

class PasswordActivity:
    def on_create(self, bundle):
        self.bundle = bundle
        self.created = True

    def setup_window_animations(self):
        self.anim_setup = True

@pytest.fixture
def activity():
    activity = MagicMock(spec=PasswordActivity)
    activity.on_create = PasswordActivity.on_create
    activity.setup_window_animations = PasswordActivity.setup_window_animations
    activity.bundle = None
    activity.created = False
    activity.anim_setup = False
    return activity

def test_on_create_no_crash(activity):
    activity.on_create(activity, {})
    assert activity.created

def test_setup_window_animations(activity):
    activity.setup_window_animations(activity)