import pytest
from unittest import mock

class TargetNotFoundToaster:
    def on_target_not_found(self, context, uri, extras, flags=None):
        return True

def test_targetnotfoundtoaster_always_returns_true():
    context = mock.Mock()
    extras = {}
    handler = TargetNotFoundToaster()
    uri = "some://missing"
    result = handler.on_target_not_found(context, uri, extras)
    assert result is True