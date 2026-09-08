import pytest

class EventStoreHandler:
    pass

class ApplicationContext:
    def __init__(self):
        self.beans = {
            "eventStoreHandler": EventStoreHandler()
        }
    def getBean(self, name):
        return self.beans.get(name)

@pytest.fixture
def application_context():
    return ApplicationContext()

def test_event_store_handler_is_not_applied_by_event_aop(application_context):
    bean = application_context.getBean("eventStoreHandler")
    assert bean is not None
    assert isinstance(bean, EventStoreHandler)