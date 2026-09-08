import pytest

def get_mock_app_context():
    # In Java: Using InstrumentationRegistry.getTargetContext()
    # For Python, we simulate the name
    class AppContext:
        def get_package_name(self):
            return "com.cheng.channelview"
    return AppContext()

def test_use_app_context():
    """
    Translated from ExampleInstrumentedTest.java (app)
    """
    app_context = get_mock_app_context()
    assert app_context.get_package_name() == "com.cheng.channelview"