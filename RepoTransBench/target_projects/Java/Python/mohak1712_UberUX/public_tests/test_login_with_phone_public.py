import pytest
from unittest.mock import MagicMock

class LoginWithPhone:
    def on_create(self, bundle):
        self.bundle = bundle
        self.created = True

    def setup_window_animations(self):
        self.anim_setup = True

@pytest.fixture
def activity():
    activity = MagicMock(spec=LoginWithPhone)
    activity.on_create = LoginWithPhone.on_create
    activity.setup_window_animations = LoginWithPhone.setup_window_animations
    activity.bundle = None
    activity.created = False
    activity.anim_setup = False
    return activity

def test_on_create_no_crash_public(activity):
    bundle = {"public_test_number": 42}
    activity.on_create(activity, bundle)
    assert activity.created

def test_setup_window_animations_no_crash_public(activity):
    activity.setup_window_animations(activity)