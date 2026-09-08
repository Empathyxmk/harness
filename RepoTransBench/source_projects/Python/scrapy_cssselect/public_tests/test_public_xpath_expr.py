import pytest
from cssselect.xpath import XPathExpr

def test_xpath_expr_str_and_add_condition_public():
    x = XPathExpr(path="/root/", element="span", condition="active=true")
    assert str(x).startswith("/root/span[active=")
    x.add_condition("visible=false")
    assert "visible=false" in x.condition
    assert "active=true" in x.condition

def test_xpath_expr_add_name_test_public():
    x = XPathExpr(path="//", element="section")
    x.add_name_test()
    assert x.element == "*"
    assert "name()" in x.condition

def test_xpath_expr_add_star_prefix_public():
    x = XPathExpr(path="/foo/", element="*", condition="")
    x.add_star_prefix()
    assert x.path.startswith("/foo/*")

def test_xpath_expr_join_public():
    x1 = XPathExpr(path="/root/", element="header", condition="data=val1")
    x2 = XPathExpr(path="/sibling/", element="footer", condition="data=val2")
    r = x1.join(combiner="//", other=x2, closing_combiner="-end-", has_inner_condition=True)
    assert isinstance(r, XPathExpr)
    assert r.element.startswith("footer")
    assert "//" in r.path or "-end-" in r.path