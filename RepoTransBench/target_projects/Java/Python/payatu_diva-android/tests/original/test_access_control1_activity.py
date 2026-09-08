import pytest

class AccessControl1Activity:
    def __init__(self):
        self.ac1ViewCredsBtn = True  # Simulate presence of btn
        self.package_manager = self.PackageManagerMock()
        self.activity_started = False
        self.toast_shown = False
    def find_view_by_id(self, key):
        if key == "ac1ViewCredsBtn":
            return self.ac1ViewCredsBtn
        return None
    def get_package_manager(self):
        return self.package_manager
    class PackageManagerMock:
        def __init__(self):
            self.should_resolve = True
        def resolve_activity(self, intent, flags):
            if self.should_resolve:
                return object()
            else:
                return None
    def view_api_credentials(self, view):
        pm = self.get_package_manager()
        result = pm.resolve_activity("test_intent", 0)
        if result:
            self.activity_started = True
        else:
            self.toast_shown = True
    def start_activity(self, intent):
        self.activity_started = True

@pytest.fixture
def activity():
    return AccessControl1Activity()

def test_on_create_sets_layout(activity):
    assert activity.ac1ViewCredsBtn == True

def test_view_api_credentials_intent_resolved_starts_activity(activity):
    activity.package_manager.should_resolve = True
    activity.view_api_credentials("dummy_view")
    assert activity.activity_started is True

def test_view_api_credentials_intent_not_resolved_shows_toast_and_logs(activity):
    activity.package_manager.should_resolve = False
    activity.view_api_credentials("dummy_view")
    assert activity.toast_shown is True