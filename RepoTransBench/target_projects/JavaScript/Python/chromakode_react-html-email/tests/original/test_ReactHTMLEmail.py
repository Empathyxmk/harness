import src.index as module

def test_validates_style_objects():
    calls = []
    orig_validate = module.default.styleValidator.validate
    def fake_validate(style, component):
        calls.append((style, component))
        return None
    module.default.styleValidator.validate = fake_validate
    style = {"listStylePosition": "11px"}
    module.PropTypes.style(style)
    assert calls[-1] == (style, "TestComponent")
    module.default.styleValidator.validate = orig_validate