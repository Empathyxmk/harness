import pytest

class PreferenceComponent_JunitComponent:
    _instance = None
    def __init__(self):
        self.injected = False
    @staticmethod
    def getInstance():
        if PreferenceComponent_JunitComponent._instance is None:
            PreferenceComponent_JunitComponent._instance = PreferenceComponent_JunitComponent()
        return PreferenceComponent_JunitComponent._instance
    def inject(self, obj):
        obj.junitComponent = self
        self.injected = True
    def TestProfile(self):
        return object()
    def getEntityNameList(self):
        return ['TestProfile']

class TestObj:
    junitComponent = None

@pytest.fixture(scope="function")
def injected_obj():
    obj = TestObj()
    comp = PreferenceComponent_JunitComponent.getInstance()
    comp.inject(obj)
    return obj

def test_injection(injected_obj):
    assert injected_obj.junitComponent is not None
    assert injected_obj.junitComponent.TestProfile() is not None

def test_entity_list(injected_obj):
    junitComponent = injected_obj.junitComponent
    entity_list = junitComponent.getEntityNameList()
    assert entity_list[0] == "TestProfile"