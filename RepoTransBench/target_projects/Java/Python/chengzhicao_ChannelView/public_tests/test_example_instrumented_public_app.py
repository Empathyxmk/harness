import pytest

def get_public_mock_app_context():
    # Simulated, as in Android Instrumentation test, with a different (incorrect) package name.
    class AppContext:
        def get_package_name(self):
            return "com.fake.publictest"
    return AppContext()

def test_use_app_context_public():
    """
    Translated from ExampleInstrumentedPublicTest.java (app)
    """
    app_context = get_public_mock_app_context()
    # The test asserts the package name is NOT the actual app package.
    assert app_context.get_package_name() != "com.cheng.channelview"