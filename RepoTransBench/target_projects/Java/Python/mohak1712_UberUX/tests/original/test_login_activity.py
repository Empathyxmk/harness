import pytest
from unittest.mock import MagicMock

class LoginActivity:
    def on_create(self, bundle):
        # Simulate minimal on_create logic
        self.bundle = bundle
        self.created = True

    def setup_window_animations(self):
        # Simulate protected method
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

def test_on_create_executes_without_crash(activity):
    bundle = {}
    activity.on_create(activity, bundle)
    assert activity.created

def test_setup_window_animations_no_crash(activity):
    activity.setup_window_animations(activity)