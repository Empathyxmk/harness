import pytest

class AppContext:
    """Simulated Android Context for testing."""
    def get_package_name(self):
        return "top.niunaijun.blackobfuscator.asplugin"

class InstrumentationRegistry:
    """Simulated InstrumentationRegistry for test."""
    @staticmethod
    def get_instrumentation():
        return InstrumentationRegistry()

    def get_target_context(self):
        return AppContext()

def test_use_app_context():
    # Simulate retrieving context in Android test
    app_context = InstrumentationRegistry.get_instrumentation().get_target_context()
    assert app_context.get_package_name() == "top.niunaijun.blackobfuscator.asplugin"