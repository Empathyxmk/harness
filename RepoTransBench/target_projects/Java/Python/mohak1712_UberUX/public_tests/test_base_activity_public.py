import pytest
from unittest.mock import MagicMock

class BaseActivity:
    def get_context(self):
        # In the public test, this gets a mocked context object
        return self._ctx if hasattr(self, "_ctx") else None

@pytest.fixture
def base_activity():
    base_activity = BaseActivity()
    base_activity._ctx = object()  # Mocked context
    return base_activity

def test_get_context_public(base_activity):
    assert base_activity.get_context() is not None