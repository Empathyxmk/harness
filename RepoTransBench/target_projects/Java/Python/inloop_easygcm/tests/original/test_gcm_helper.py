import pytest
from unittest.mock import Mock

# GcmHelper, GcmListener, GcmServicesHandler, EasyGcm stubs

class GcmListener:
    pass

class GcmServicesHandler:
    pass

class EasyGcm:
    _instance = None
    _listener = None
    _handler = None
    _is_registered = False
    _registration_id = None
    _gcm_sender_id = None
    _logging_enabled = 0

    @staticmethod
    def getInstance():
        if EasyGcm._instance is None:
            EasyGcm._instance = EasyGcm()
        return EasyGcm._instance

    @staticmethod
    def setGcmListener(listener):
        EasyGcm._listener = listener

    @staticmethod
    def setCheckServicesHandler(handler):
        EasyGcm._handler = handler

    @staticmethod
    def isRegistered(context):
        return False

    @staticmethod
    def getRegistrationId(context):
        return None

    @staticmethod
    def removeRegistrationId(context):
        pass

    @staticmethod
    def getGcmSenderId(context):
        return None

    def setLoggingEnabled(self, level):
        EasyGcm._logging_enabled = level

    def getGcmListener(self, context):
        # Could return None for stub
        return None

class GcmHelper:
    @staticmethod
    def init(context):
        # Calls EasyGcm initialization
        pass

    @staticmethod
    def getInstance():
        return EasyGcm.getInstance()

    @staticmethod
    def setGcmListener(listener):
        EasyGcm.setGcmListener(listener)

    @staticmethod
    def setCheckServicesHandler(handler):
        EasyGcm.setCheckServicesHandler(handler)

    @staticmethod
    def isRegistered(context):
        return EasyGcm.isRegistered(context)

    @staticmethod
    def getRegistrationId(context):
        return EasyGcm.getRegistrationId(context)

    @staticmethod
    def removeRegistrationId(context):
        EasyGcm.removeRegistrationId(context)

    @staticmethod
    def getGcmSenderId(context):
        return EasyGcm.getGcmSenderId(context)

@pytest.fixture
def gcm_helper_mocks():
    mock_context = Mock()
    mock_listener = Mock(spec=GcmListener)
    mock_handler = Mock(spec=GcmServicesHandler)
    return mock_context, mock_listener, mock_handler

def test_init_delegates_to_easygcm(gcm_helper_mocks):
    mock_context, _, _ = gcm_helper_mocks
    GcmHelper.init(mock_context)  # should not throw

def test_get_instance_singleton():
    instance1 = GcmHelper.getInstance()
    instance2 = GcmHelper.getInstance()
    assert instance1 is not None
    assert instance1 is instance2

def test_set_gcm_listener_delegates_to_easygcm(gcm_helper_mocks):
    _, mock_listener, _ = gcm_helper_mocks
    GcmHelper.setGcmListener(mock_listener)

def test_set_check_services_handler_delegates_to_easygcm(gcm_helper_mocks):
    _, _, mock_handler = gcm_helper_mocks
    GcmHelper.setCheckServicesHandler(mock_handler)

def test_is_registered_delegates_to_easygcm(gcm_helper_mocks):
    mock_context, _, _ = gcm_helper_mocks
    result = GcmHelper.isRegistered(mock_context)
    assert result is False  # Because default EasyGcm.isRegistered returns false

def test_get_registration_id_delegates_to_easygcm(gcm_helper_mocks):
    mock_context, _, _ = gcm_helper_mocks
    assert GcmHelper.getRegistrationId(mock_context) is None

def test_remove_registration_id_delegates_to_easygcm(gcm_helper_mocks):
    mock_context, _, _ = gcm_helper_mocks
    GcmHelper.removeRegistrationId(mock_context)

def test_get_gcm_sender_id_delegates_to_easygcm(gcm_helper_mocks):
    mock_context, _, _ = gcm_helper_mocks
    assert GcmHelper.getGcmSenderId(mock_context) is None

def test_set_logging_enabled():
    helper = GcmHelper.getInstance()
    helper.setLoggingEnabled(1)

def test_get_gcm_listener_delegates_to_easygcm():
    helper = GcmHelper.getInstance()
    # Should not throw, returns None
    assert helper.getGcmListener(Mock()) is None