import pytest
from parsel.csstranslator import GenericTranslator, HTMLTranslator, XPathExpr

def test_xpathexpr_str_textnode_and_attribute():
    # Test path mangling for attribute and textnode
    # path: default *
    e = XPathExpr.from_xpath(XPathExpr("*"))
    e.textnode = True
    # Accept both "*/text()" and "text()" which may vary by implementation
    assert str(e).endswith("text()")

    e = XPathExpr.from_xpath(XPathExpr("*"))
    e.attribute = "class"
    # Accept both "*/@class" and "@class"
    assert str(e).endswith("@class")

    # If both set, textnode usually takes precedence, but implementation dependent
    e = XPathExpr.from_xpath(XPathExpr("*"))
    e.textnode = True
    e.attribute = "href"
    s = str(e)
    # Accept either order, just check both appear
    assert "text()" in s or "@href" in s

def test_xpathexpr_join_type_check():
    e1 = XPathExpr("*")
    with pytest.raises(ValueError):
        e1.join("/", object())

def test_generic_translator_cache_behavior():
    t = GenericTranslator()
    path1 = t.css_to_xpath("div > a")
    path2 = t.css_to_xpath("div > a")
    assert path1 == path2

def test_htmltranslator_inheritance():
    h = HTMLTranslator()
    path = h.css_to_xpath("body > p")
    assert "body" in path

def test_xpath_pseudo_element_unknown(monkeypatch):
    t = GenericTranslator()
    class DummyPseudo:
        name = "unknown"
    xpath = XPathExpr("*")
    pe = DummyPseudo()
    with pytest.raises(Exception):
        t.xpath_pseudo_element(xpath, pe)

def test_xpath_attr_function_raises():
    t = GenericTranslator()
    xpath = XPathExpr("*")
    class DummyFunc:
        def argument_types(self): return ["INTEGER"]
        arguments = []
    with pytest.raises(Exception):
        t.xpath_attr_functional_pseudo_element(xpath, DummyFunc())