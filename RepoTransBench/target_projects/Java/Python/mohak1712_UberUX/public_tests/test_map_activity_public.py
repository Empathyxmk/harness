import pytest
from unittest.mock import MagicMock

class MapActivity:
    def __init__(self):
        self.created = False

    def on_create(self, bundle):
        self.created = True
        self.bundle = bundle

@pytest.fixture
def activity():
    return MapActivity()

def test_on_create_executes_without_crash_public(activity):
    bundle = {"public_test_double": 88.88}
    activity.on_create(bundle)
    assert activity.created