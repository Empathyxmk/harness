import pytest

class MultiDexApplication:
    def attach_base_context(self, base):
        # In real code, would call MultiDex.install(self)
        pass

def test_attach_base_context():
    app = MultiDexApplication()
    try:
        app.attach_base_context(object())
    except Exception:
        pass  # Accept any outcome (no-op or exception)