import types

class DummyTransformer:
    def __call__(self, *args, **kwargs):
        return "rn transformed"

def createTransformer(transformer_callable):
    return transformer_callable

class MockIndexModule:
    @staticmethod
    def createTransformer(fn):
        return createTransformer(fn)

    @staticmethod
    def getReactNativeTransformer():
        class Dummy:
            def __init__(self):
                self.transform = lambda *a, **k: None
        return Dummy()

def test_react_native_index_exports_transform_via_createTransformer():
    mod = types.SimpleNamespace()
    mod.createTransformer = MockIndexModule.createTransformer
    mod.getReactNativeTransformer = MockIndexModule.getReactNativeTransformer
    mod.transform = createTransformer(lambda *args, **kwargs: "rn transformed")
    assert callable(mod.transform)
    assert mod.transform() == "rn transformed"