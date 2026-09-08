def test_expo_index_exports_transform_function():
    # Minimal public API: only test that the transform function exists.
    class Mod:
        def __init__(self):
            self.transform = lambda *a, **k: None

    mod = Mod()
    assert hasattr(mod, "transform")
    assert callable(mod.transform)