import pytest
from parsel.csstranslator import GenericTranslator, HTMLTranslator, SelectorError

def test_generic_translator_cache_behavior_public():
    g = GenericTranslator()
    assert g.css_to_xpath("a#main.class") == '//a[contains(concat(" ",normalize-space(@class)," ")," class ")][@id = "main"]'
    assert g.css_to_xpath("a#main.class") == g.css_to_xpath("a#main.class")

def test_htmltranslator_inheritance_public():
    assert issubclass(HTMLTranslator, GenericTranslator)

def test_xpath_expr_join_type_check_public():
    g = GenericTranslator()
    with pytest.raises(TypeError):
        g.xpath_expr("span", joiner=123)  # joiner must be a string

def test_xpath_pseudo_element_unknown_public():
    g = GenericTranslator()
    with pytest.raises(SelectorError):
        g.css_to_xpath("a::unknown")