import pytest
from unittest.mock import MagicMock

class LoginActivity:
    def on_create(self, bundle):
        self.bundle = bundle
        self.created = True

    def setup_window_animations(self):
        self.anim_setup = True

@pytest.fixture
def activity():
    activity = MagicMock(spec=LoginActivity)
    activity.on_create = LoginActivity.on_create
    activity.setup_window_animations = LoginActivity.setup_window_animations
    activity.bundle = None
    activity.created = False
    activity.anim_setup = False
    return activity

def test_on_create_executes_without_crash_public(activity):
    bundle = {"public_test_key": "public_test_value"}
    activity.on_create(activity, bundle)
    assert activity.created

def test_setup_window_animations_no_crash_public(activity):
    activity.setup_window_animations(activity)