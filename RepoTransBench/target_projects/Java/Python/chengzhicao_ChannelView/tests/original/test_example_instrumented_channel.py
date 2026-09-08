import pytest

def get_mock_app_context_channel():
    # In Java: Using InstrumentationRegistry.getTargetContext()
    # For Python, we simulate the name
    class AppContext:
        def get_package_name(self):
            return "com.cheng.channelview.test"
    return AppContext()

def test_use_app_context_channel():
    """
    Translated from ExampleInstrumentedTest.java (channelview)
    """
    app_context = get_mock_app_context_channel()
    assert app_context.get_package_name() == "com.cheng.channelview.test"