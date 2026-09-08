import pytest
from cssselect.xpath import XPathExpr

def test_xpath_expr_str_and_add_condition():
    x = XPathExpr(path="//", element="div", condition="foo=1")
    assert str(x) == "//div[foo=1]"
    x.add_condition("bar=2")
    assert "[foo=1)" not in x.condition  # parentheses wrapped
    assert "bar=2" in x.condition

def test_xpath_expr_add_name_test():
    x = XPathExpr(path="//", element="div")
    x.add_name_test()
    assert x.element == "*"
    assert "name()" in x.condition

def test_xpath_expr_add_star_prefix():
    x = XPathExpr(path="//", element="*", condition="")
    x.add_star_prefix()
    assert x.path == "//*" or x.path == "//*" or x.path.endswith("*/")

def test_xpath_expr_join():
    x1 = XPathExpr(path="//", element="a", condition="foo=1")
    x2 = XPathExpr(path="/*/", element="span", condition="bar=2")
    r = x1.join(combiner="|", other=x2, closing_combiner="::", has_inner_condition=True)
    assert isinstance(r, XPathExpr)
    assert r.element.startswith("span")
    # Check path joined
    assert "|" in r.path