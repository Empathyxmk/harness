import pytest

from src.componentbase.service_factory import ServiceFactory
from src.componentbase.empty_service.empty_account_service import EmptyAccountService
from src.componentbase.service.i_account_service import IAccountService

class MockAccountService(IAccountService):
    def is_login(self):
        return True
    def get_account_id(self):
        return "mock"
    def new_user_fragment(self, activity, container_id, manager, bundle, tag):
        return None

@pytest.fixture(autouse=True)
def fresh_singleton():
    ServiceFactory._instance = None
    yield
    ServiceFactory._instance = None

def test_singleton_instance():
    factory1 = ServiceFactory.get_instance()
    factory2 = ServiceFactory.get_instance()
    assert factory1 is factory2

def test_set_and_get_account_service():
    mock_service = MockAccountService()
    ServiceFactory.get_instance().set_account_service(mock_service)
    result = ServiceFactory.get_instance().get_account_service()
    assert result is mock_service

def test_get_account_service_returns_empty_if_null():
    ServiceFactory.get_instance().set_account_service(None)
    service = ServiceFactory.get_instance().get_account_service()
    assert service is not None
    assert isinstance(service, EmptyAccountService)