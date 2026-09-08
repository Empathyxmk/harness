import pytest

class AppContext:
    def get_package_name(self):
        # Simulate a differing package name for demonstration.
        return "architecture.google.coremodel.test.public"

def test_use_app_context_with_different_data():
    app_context = AppContext()
    assert app_context.get_package_name() != "architecture.google.coremodel"