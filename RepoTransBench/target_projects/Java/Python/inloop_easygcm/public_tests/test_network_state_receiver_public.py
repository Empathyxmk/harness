import pytest
from unittest.mock import Mock, call

# Stubs for Context, Intent, Receiver - with public stubbers
class Context:
    pass

class Intent:
    def __init__(self, ctx=None, obj_cls=None):
        self._created_with = (ctx, obj_cls)

class WakefulBroadcastReceiver:
    def startWakefulService(self, context, intent):
        pass

    def onReceive(self, context, intent):
        if GcmUtilsPublic.checkCanAndShouldRegister(context):
            intent_to_start = GcmRegistrationServicePublic.createGcmRegistrationIntent(context, True)
            self.startWakefulService(context, intent_to_start)

class GcmUtilsStubberPublic:
    forcedResult = False
    override = False

    @staticmethod
    def setCheckCanAndShouldRegisterResult(result):
        GcmUtilsStubberPublic.forcedResult = result
        GcmUtilsStubberPublic.override = True

    @staticmethod
    def reset():
        GcmUtilsStubberPublic.forcedResult = False
        GcmUtilsStubberPublic.override = False

class GcmRegistrationServiceStubberPublic:
    forcedIntent = None

    @staticmethod
    def setCreateGcmRegistrationIntentResult(intent):
        GcmRegistrationServiceStubberPublic.forcedIntent = intent

    @staticmethod
    def reset():
        GcmRegistrationServiceStubberPublic.forcedIntent = None

# Patch for public test
class GcmUtilsPublic:
    @staticmethod
    def checkCanAndShouldRegister(context):
        if GcmUtilsStubberPublic.override:
            return GcmUtilsStubberPublic.forcedResult
        return False

class GcmRegistrationServicePublic:
    @staticmethod
    def createGcmRegistrationIntent(context, hasWakeLock=True):
        if GcmRegistrationServiceStubberPublic.forcedIntent is not None:
            return GcmRegistrationServiceStubberPublic.forcedIntent
        return Intent()

class NetworkStateReceiverPublic(WakefulBroadcastReceiver):
    pass

@pytest.fixture
def setup_mocks_public(monkeypatch):
    mock_context = Mock(spec=Context)
    mock_intent = Mock(spec=Intent)
    return mock_context, mock_intent

def test_receive_registers_when_allowed_public(monkeypatch, setup_mocks_public):
    mock_context, mock_intent = setup_mocks_public
    try:
        GcmUtilsStubberPublic.setCheckCanAndShouldRegisterResult(True)
        reg_intent = Intent(mock_context, object)  # Use different intent for public test
        GcmRegistrationServiceStubberPublic.setCreateGcmRegistrationIntentResult(reg_intent)

        receiver = NetworkStateReceiverPublic()
        receiver.startWakefulService = Mock()

        receiver.onReceive(mock_context, mock_intent)

        receiver.startWakefulService.assert_called_once_with(mock_context, reg_intent)
    finally:
        GcmUtilsStubberPublic.reset()
        GcmRegistrationServiceStubberPublic.reset()

def test_receive_does_nothing_if_not_allowed_public(monkeypatch, setup_mocks_public):
    mock_context, mock_intent = setup_mocks_public
    try:
        GcmUtilsStubberPublic.setCheckCanAndShouldRegisterResult(False)
        receiver = NetworkStateReceiverPublic()
        receiver.startWakefulService = Mock()
        receiver.onReceive(mock_context, mock_intent)
        receiver.startWakefulService.assert_not_called()
    finally:
        GcmUtilsStubberPublic.reset()
        GcmRegistrationServiceStubberPublic.reset()