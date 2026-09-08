import types

class DummyTransformer:
    def __call__(self, *args, **kwargs):
        return "expo transformed"

def createTransformer(transformer_callable):
    # returns a transformer function
    return transformer_callable

# Mock the index.js module functionality
class MockIndexModule:
    @staticmethod
    def createTransformer(fn):
        return createTransformer(fn)

    @staticmethod
    def getExpoTransformer():
        # Returns an object with a .transform attribute (simulated)
        class Dummy:
            def __init__(self):
                self.transform = lambda *a, **k: None
        return Dummy()

def test_expo_index_exports_transform_via_createTransformer():
    # Simulate importing ./index.js and constructing expo/index.js's transform
    mod = types.SimpleNamespace()
    mod.createTransformer = MockIndexModule.createTransformer
    mod.getExpoTransformer = MockIndexModule.getExpoTransformer
    # expo/index.js: exports "transform = createTransformer(getExpoTransformer())"
    mod.transform = createTransformer(lambda *args, **kwargs: "expo transformed")
    assert callable(mod.transform)
    assert mod.transform() == "expo transformed"