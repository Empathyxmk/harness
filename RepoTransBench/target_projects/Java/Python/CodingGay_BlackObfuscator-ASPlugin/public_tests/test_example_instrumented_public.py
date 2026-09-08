import pytest

class AppContext:
    def get_package_name(self):
        return "top.niunaijun.blackobfuscator.asplugin"

class InstrumentationRegistry:
    @staticmethod
    def get_instrumentation():
        return InstrumentationRegistry()

    def get_target_context(self):
        return AppContext()

def test_use_app_context_different_package():
    app_context = InstrumentationRegistry.get_instrumentation().get_target_context()
    assert app_context.get_package_name().startswith("top.")