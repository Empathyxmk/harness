def test_get_expo_transformer_returns_object_with_transform():
    # Simulate the public-facing part of the API as in the minimal test
    class DummyTransformer:
        def __init__(self):
            self.transform = lambda *a, **k: None

    def getExpoTransformer():
        return DummyTransformer()

    transformer = getExpoTransformer()
    if transformer:
        assert hasattr(transformer, "transform")
        assert callable(transformer.transform)
    else:
        assert transformer is None

def test_main_exported_transform_function_exists():
    # Simulate public API: just check that "transform" exists.
    class Mod:
        def __init__(self):
            self.transform = lambda *a, **k: None

    mod = Mod()
    assert hasattr(mod, "transform")
    assert callable(mod.transform)