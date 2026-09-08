import pytest
from unittest.mock import Mock

# Public variants like original, but with data changes
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
        return None

class GcmHelper:
    @staticmethod
    def init(context):
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
def gcm_helper_mocks_public():
    mock_context = Mock()
    mock_listener = Mock(spec=GcmListener)
    mock_handler = Mock(spec=GcmServicesHandler)
    return mock_context, mock_listener, mock_handler

def test_init_delegates_to_easygcm_public(gcm_helper_mocks_public):
    mock_context, _, _ = gcm_helper_mocks_public
    GcmHelper.init(mock_context)

def test_set_gcm_listener_public(gcm_helper_mocks_public):
    _, mock_listener, _ = gcm_helper_mocks_public
    GcmHelper.setGcmListener(mock_listener)

def test_set_check_services_handler_public(gcm_helper_mocks_public):
    _, _, mock_handler = gcm_helper_mocks_public
    GcmHelper.setCheckServicesHandler(mock_handler)

def test_is_registered_public_different_input(gcm_helper_mocks_public):
    mock_context, _, _ = gcm_helper_mocks_public
    GcmHelper.isRegistered(mock_context)

def test_get_registration_id_public_different_input(gcm_helper_mocks_public):
    mock_context, _, _ = gcm_helper_mocks_public
    GcmHelper.getRegistrationId(mock_context)

def test_remove_registration_id_public_different_input(gcm_helper_mocks_public):
    mock_context, _, _ = gcm_helper_mocks_public
    GcmHelper.removeRegistrationId(mock_context)

def test_get_gcm_sender_id_public_different_input(gcm_helper_mocks_public):
    mock_context, _, _ = gcm_helper_mocks_public
    GcmHelper.getGcmSenderId(mock_context)

def test_set_logging_enabled_public():
    helper = GcmHelper.getInstance()
    helper.setLoggingEnabled(5)

def test_get_gcm_listener_public():
    helper = GcmHelper.getInstance()
    helper.getGcmListener(Mock())