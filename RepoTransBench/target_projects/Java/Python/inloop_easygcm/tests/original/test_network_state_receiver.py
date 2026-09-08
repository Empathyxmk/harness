import pytest
from unittest.mock import Mock, call

# Stubs for Context, Intent, Receiver
class Context:
    pass

class Intent:
    def __init__(self):
        pass

class WakefulBroadcastReceiver:
    def startWakefulService(self, context, intent):
        pass

    def onReceive(self, context, intent):
        # Patchable for test
        if GcmUtils.checkCanAndShouldRegister(context):
            intent_to_start = GcmRegistrationService.createGcmRegistrationIntent(context, True)
            self.startWakefulService(context, intent_to_start)

# Static stubbers for test injection
class GcmUtilsStubber:
    forcedResult = False
    override = False

    @staticmethod
    def setCheckCanAndShouldRegisterResult(result):
        GcmUtilsStubber.forcedResult = result
        GcmUtilsStubber.override = True

    @staticmethod
    def reset():
        GcmUtilsStubber.forcedResult = False
        GcmUtilsStubber.override = False

class GcmRegistrationServiceStubber:
    forcedIntent = None

    @staticmethod
    def setCreateGcmRegistrationIntentResult(intent):
        GcmRegistrationServiceStubber.forcedIntent = intent

    @staticmethod
    def reset():
        GcmRegistrationServiceStubber.forcedIntent = None

# Implement the classes used inside NetworkStateReceiver for the above static stub
class GcmUtils:
    @staticmethod
    def checkCanAndShouldRegister(context):
        if GcmUtilsStubber.override:
            return GcmUtilsStubber.forcedResult
        return False

class GcmRegistrationService:
    @staticmethod
    def createGcmRegistrationIntent(context, hasWakeLock=True):
        if GcmRegistrationServiceStubber.forcedIntent is not None:
            return GcmRegistrationServiceStubber.forcedIntent
        return Intent()

class NetworkStateReceiver(WakefulBroadcastReceiver):
    pass

@pytest.fixture
def setup_mocks(monkeypatch):
    mock_context = Mock(spec=Context)
    mock_intent = Mock(spec=Intent)
    return mock_context, mock_intent

def test_receive_registers_when_allowed(monkeypatch, setup_mocks):
    mock_context, mock_intent = setup_mocks
    try:
        GcmUtilsStubber.setCheckCanAndShouldRegisterResult(True)
        reg_intent = Intent()
        GcmRegistrationServiceStubber.setCreateGcmRegistrationIntentResult(reg_intent)

        receiver = NetworkStateReceiver()
        # Patch startWakefulService to a mock
        receiver.startWakefulService = Mock()

        receiver.onReceive(mock_context, mock_intent)

        receiver.startWakefulService.assert_called_once_with(mock_context, reg_intent)
    finally:
        GcmUtilsStubber.reset()
        GcmRegistrationServiceStubber.reset()

def test_receive_does_nothing_if_not_allowed(monkeypatch, setup_mocks):
    mock_context, mock_intent = setup_mocks
    try:
        GcmUtilsStubber.setCheckCanAndShouldRegisterResult(False)
        receiver = NetworkStateReceiver()
        receiver.startWakefulService = Mock()
        receiver.onReceive(mock_context, mock_intent)
        receiver.startWakefulService.assert_not_called()
    finally:
        GcmUtilsStubber.reset()
        GcmRegistrationServiceStubber.reset()