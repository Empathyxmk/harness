import pytest

class EventStoreHandler:
    pass

class ApplicationContext:
    def __init__(self):
        self.beans = {
            "eventStoreHandlerA": EventStoreHandler(),
            "eventStoreHandlerB": EventStoreHandler(),
        }
    def getBeanNamesForType(self, typ):
        return [name for name, bean in self.beans.items() if isinstance(bean, typ)]
    def getBean(self, name):
        return self.beans[name]

@pytest.fixture
def application_context():
    return ApplicationContext()

def test_event_store_handler_bean_has_application_context_and_type(application_context):
    beans = application_context.getBeanNamesForType(EventStoreHandler)
    assert len(beans) > 0
    for bean_name in beans:
        bean = application_context.getBean(bean_name)
        assert bean is not None
        assert isinstance(bean, EventStoreHandler)