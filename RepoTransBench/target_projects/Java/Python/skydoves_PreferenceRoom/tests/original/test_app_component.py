import pytest

class PreferenceComponent_AppComponent:
    _instance = None
    @staticmethod
    def getInstance():
        if PreferenceComponent_AppComponent._instance is None:
            PreferenceComponent_AppComponent._instance = PreferenceComponent_AppComponent()
        return PreferenceComponent_AppComponent._instance
    def UserProfile(self):
        return object()
    def UserDevice(self):
        return object()
    def getEntityNameList(self):
        return ['UserProfile', 'UserDevice']

@pytest.fixture(scope="function")
def appComponent():
    PreferenceComponent_AppComponent._instance = None  # reset singleton between tests
    return PreferenceComponent_AppComponent.getInstance()

def test_component_initialize(appComponent):
    assert PreferenceComponent_AppComponent.getInstance() is not None

def test_entity_initialize(appComponent):
    assert appComponent.UserProfile() is not None
    assert appComponent.UserDevice() is not None

def test_entity_list(appComponent):
    entity_list = appComponent.getEntityNameList()
    assert entity_list[0] == "UserProfile"
    assert entity_list[1] == "UserDevice"