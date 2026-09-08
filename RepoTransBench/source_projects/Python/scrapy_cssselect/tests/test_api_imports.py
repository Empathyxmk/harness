import pytest

def test_import_all_attrs():
    import cssselect
    for attr in [
        "ExpressionError",
        "FunctionalPseudoElement",
        "GenericTranslator",
        "HTMLTranslator",
        "Selector",
        "SelectorError",
        "SelectorSyntaxError",
        "parse",
    ]:
        assert hasattr(cssselect, attr)

def test_version():
    import cssselect
    assert isinstance(cssselect.VERSION, str)
    assert cssselect.VERSION == cssselect.__version__