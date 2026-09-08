import pytest

from src.componentbase.service_factory import ServiceFactory
from src.componentbase.empty_service.empty_account_service import EmptyAccountService
from src.componentbase.service.i_account_service import IAccountService

class DifferentMockAccountService(IAccountService):
    def is_login(self):
        return False
    def get_account_id(self):
        return "public_mock_id"
    def new_user_fragment(self, activity, container_id, manager, bundle, tag):
        return None

@pytest.fixture(autouse=True)
def fresh_singleton():
    ServiceFactory._instance = None
    yield
    ServiceFactory._instance = None

def test_singleton_instance_public():
    inst1 = ServiceFactory.get_instance()
    inst2 = ServiceFactory.get_instance()
    assert inst1 is inst2

def test_set_and_get_different_mock_account_service():
    service = DifferentMockAccountService()
    ServiceFactory.get_instance().set_account_service(service)
    result = ServiceFactory.get_instance().get_account_service()
    assert result is service

def test_get_account_service_returns_empty_if_null_public():
    ServiceFactory.get_instance().set_account_service(None)
    service = ServiceFactory.get_instance().get_account_service()
    assert service is not None
    assert isinstance(service, EmptyAccountService)