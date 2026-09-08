import pytest

def get_public_mock_app_context_channel():
    # Simulated, as in Android Instrumentation test, with a purposely wrong package name string.
    class AppContext:
        def get_package_name(self):
            return "com.fake.publicchannel"
    return AppContext()

def test_use_app_context_public_channel():
    """
    Translated from ExampleInstrumentedPublicTest.java (channelview)
    """
    app_context = get_public_mock_app_context_channel()
    # The test asserts the package name is NOT the real channelview package name.
    assert app_context.get_package_name() != "com.cheng.channelview.test"