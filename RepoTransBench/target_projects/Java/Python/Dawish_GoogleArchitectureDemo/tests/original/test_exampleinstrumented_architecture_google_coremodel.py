import pytest

class AppContext:
    def get_package_name(self):
        return "architecture.google.coremodel.test"

def test_use_app_context():
    app_context = AppContext()
    assert app_context.get_package_name() == "architecture.google.coremodel.test"