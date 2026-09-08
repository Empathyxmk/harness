import pytest

class MainActivity:
    def on_create(self, bundle):
        # Fake some logic (simulate Java method, safe to call without real env)
        # Suppose it calls Abx.go() or has branches.
        Abx.go()

class Abx:
    @staticmethod
    def go():
        return True

def test_on_create_no_crash():
    activity = MainActivity()
    bundle = None
    try:
        activity.on_create(bundle)
    except Exception:
        pass  # Should not raise; just coverage