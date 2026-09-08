import pytest

class AppContext:
    # Simulate minimal context with package_name for testing purpose
    def get_package_name(self):
        return "mohak.uberux"

@pytest.fixture
def app_context():
    return AppContext()

def test_use_app_context(app_context):
    assert app_context.get_package_name() == "mohak.uberux"