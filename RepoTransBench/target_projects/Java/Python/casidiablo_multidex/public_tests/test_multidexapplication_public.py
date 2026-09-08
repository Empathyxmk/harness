import pytest

class MultiDexApplication:
    def attach_base_context(self, base):
        pass

class MockContext:
    pass

class MyApp(MultiDexApplication):
    def attach_base_context(self, base):
        super().attach_base_context(base)

def test_attach_base_context_override_public():
    app = MyApp()
    app.attach_base_context(MockContext())
    assert app is not None
    assert type(app) == MyApp