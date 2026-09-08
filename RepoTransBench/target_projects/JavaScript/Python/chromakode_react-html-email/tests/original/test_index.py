from src import index as mod

def test_exports_main_modules():
    assert hasattr(mod, 'PropTypes')
    assert callable(mod.configStyleValidator)
    assert callable(mod.renderEmail)

def test_exports_subcomponents():
    assert hasattr(mod, "Box")
    assert hasattr(mod, "Email")
    assert hasattr(mod, "Image")
    assert hasattr(mod, "Item")
    assert hasattr(mod, "Span")
    assert hasattr(mod, "A")

def test_exports_default_with_keys():
    assert hasattr(mod, "default")
    assert hasattr(mod.default, "PropTypes")
    assert hasattr(mod.default, "configStyleValidator")
    assert hasattr(mod.default, "renderEmail")
    assert hasattr(mod.default, "styleValidator")