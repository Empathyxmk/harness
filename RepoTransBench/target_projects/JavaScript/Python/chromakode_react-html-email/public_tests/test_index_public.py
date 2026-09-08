from src import index as mod

def test_exports_stylevalidator_instance_public_variant():
    assert isinstance(mod.default.styleValidator, object)
    assert callable(mod.default.styleValidator.validate)

def test_exports_configstylevalidator_public_variant():
    assert callable(mod.configStyleValidator)

def test_exports_proptypes_public_variant():
    assert hasattr(mod.PropTypes, "style")
    assert callable(mod.PropTypes.style)