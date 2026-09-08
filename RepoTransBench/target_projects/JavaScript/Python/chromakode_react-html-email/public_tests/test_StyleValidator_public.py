from src.StyleValidator import StyleValidator

def test_validates_allowed_styles_public():
    val = StyleValidator()
    val.validate({"color": "orange"}, "OrangeCompPublic")
    val.validate({"fontSize": "1.5em"}, "OrangeCompPublic")

def test_warns_on_unknown_style_property_public():
    val = StyleValidator()
    val.setConfig({'warn': True})
    val.validate({"myCustomSecretStyle": 555}, "UnknownWarnPublic")

def test_does_not_throw_error_strict_mode_allowed_properties_public():
    val = StyleValidator()
    val.setConfig({'strict': True})
    val.validate({"color": "navy"}, "StrictColorCompPublic")

def test_does_not_throw_non_spec_properties_strict_mode_public():
    val = StyleValidator()
    val.setConfig({'strict': True})
    val.validate({"totallyRandomProp": True}, "NonSpecPropPublic")