import pytest
from unittest.mock import Mock, patch

# Stubs and static constants for GcmRegistrationService
class GcmRegistrationService:
    ACTION_REGISTER_GCM = 42
    EXTRA_ACTION_CODE = "action_code"
    EXTRA_HAS_WAKELOCK = "has_wakelock"

    @staticmethod
    def createGcmRegistrationIntent(context, hasWakeLock=False):
        intent = Intent()
        intent.putExtra(GcmRegistrationService.EXTRA_ACTION_CODE, GcmRegistrationService.ACTION_REGISTER_GCM)
        intent.putExtra(GcmRegistrationService.EXTRA_HAS_WAKELOCK, hasWakeLock)
        return intent

    # Simulate methods potentially used in onHandleIntent
    def isAlreadyRegistered(self, context):
        # Can be patched for test
        return False

    def releaseWakeLock(self):
        pass

    def registerGcm(self):
        pass

    def onHandleIntent(self, intent):
        action_code = intent.getIntExtra(self.EXTRA_ACTION_CODE, -1)
        if action_code == self.ACTION_REGISTER_GCM:
            context = getattr(intent, '_context', None)
            if self.isAlreadyRegistered(context):
                self.releaseWakeLock()
                # Should not register Gcm
            else:
                try:
                    self.registerGcm()
                finally:
                    self.releaseWakeLock()

class Intent:
    def __init__(self):
        self._extras = {}
        self._context = None

    def putExtra(self, key, value):
        self._extras[key] = value

    def getIntExtra(self, key, default):
        value = self._extras.get(key, default)
        return int(value) if isinstance(value, (int, bool)) else default

    def getBooleanExtra(self, key, default):
        value = self._extras.get(key, default)
        return bool(value) if value is not None else default

    def setContext(self, context):
        self._context = context

@pytest.fixture
def setup_service():
    service = GcmRegistrationService()
    mock_context = Mock()
    base_intent = Intent()
    return service, mock_context, base_intent

def test_create_gcm_registration_intent_defaults(setup_service):
    _, mock_context, _ = setup_service
    intent = GcmRegistrationService.createGcmRegistrationIntent(mock_context)
    assert intent is not None
    assert intent.getIntExtra(GcmRegistrationService.EXTRA_ACTION_CODE, -1) == GcmRegistrationService.ACTION_REGISTER_GCM

def test_create_gcm_registration_intent_with_wakelock(setup_service):
    _, mock_context, _ = setup_service
    intent = GcmRegistrationService.createGcmRegistrationIntent(mock_context, True)
    assert intent.getBooleanExtra(GcmRegistrationService.EXTRA_HAS_WAKELOCK, False) == True

def test_on_handle_intent_already_registered(monkeypatch):
    service = GcmRegistrationService()
    intent = Intent()
    intent.putExtra(GcmRegistrationService.EXTRA_ACTION_CODE, GcmRegistrationService.ACTION_REGISTER_GCM)
    context = Mock()
    intent.setContext(context)

    service_spy = service
    # Patch isAlreadyRegistered, releaseWakeLock, registerGcm
    service_spy.isAlreadyRegistered = Mock(return_value=True)
    service_spy.releaseWakeLock = Mock()
    service_spy.registerGcm = Mock()

    service_spy.onHandleIntent(intent)
    service_spy.registerGcm.assert_not_called()
    service_spy.releaseWakeLock.assert_called_once()

def test_on_handle_intent_registers_and_handles_error(monkeypatch):
    service = GcmRegistrationService()
    intent = Intent()
    intent.putExtra(GcmRegistrationService.EXTRA_ACTION_CODE, GcmRegistrationService.ACTION_REGISTER_GCM)
    context = Mock()
    intent.setContext(context)

    service_spy = service
    service_spy.isAlreadyRegistered = Mock(return_value=False)
    service_spy.releaseWakeLock = Mock()
    service_spy.registerGcm = Mock()

    service_spy.onHandleIntent(intent)
    service_spy.registerGcm.assert_called_once()
    service_spy.releaseWakeLock.assert_called_once()