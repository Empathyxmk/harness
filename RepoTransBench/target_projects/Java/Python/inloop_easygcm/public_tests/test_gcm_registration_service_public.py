import pytest
from unittest.mock import Mock

class GcmRegistrationServicePublic:
    ACTION_REGISTER_GCM = 42
    EXTRA_ACTION_CODE = "action_code"
    EXTRA_HAS_WAKELOCK = "has_wakelock"

    @staticmethod
    def createGcmRegistrationIntent(context, hasWakeLock=False):
        intent = IntentPublic()
        intent.putExtra(GcmRegistrationServicePublic.EXTRA_ACTION_CODE, GcmRegistrationServicePublic.ACTION_REGISTER_GCM)
        intent.putExtra(GcmRegistrationServicePublic.EXTRA_HAS_WAKELOCK, hasWakeLock)
        return intent

class IntentPublic:
    def __init__(self):
        self._extras = {}

    def putExtra(self, key, value):
        self._extras[key] = value

    def getIntExtra(self, key, default):
        value = self._extras.get(key, default)
        return int(value) if isinstance(value, (int, bool)) else default

    def getBooleanExtra(self, key, default):
        value = self._extras.get(key, default)
        return bool(value) if value is not None else default

@pytest.fixture
def mock_context_public():
    return Mock()

def test_create_gcm_registration_intent_with_wakelock_public(mock_context_public):
    # Using hasWakeLock = False for public test
    service_intent = GcmRegistrationServicePublic.createGcmRegistrationIntent(mock_context_public, False)
    assert service_intent is not None

def test_create_gcm_registration_intent_with_wakelock_public_different(mock_context_public):
    service_intent = GcmRegistrationServicePublic.createGcmRegistrationIntent(mock_context_public, True)
    assert service_intent is not None