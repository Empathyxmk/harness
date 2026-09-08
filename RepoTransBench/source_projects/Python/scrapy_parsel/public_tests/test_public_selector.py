import pytest
from parsel.selector import Selector

def test_extract_from_html():
    html = "<html><body><span>world</span></body></html>"
    sel = Selector(text=html)
    assert sel.xpath("//span/text()").get() == "world"

def test_css_selection():
    html = "<div><b>BoldContent</b></div>"
    sel = Selector(text=html)
    assert sel.css("b::text").get() == "BoldContent"

def test_extract_first_custom_default():
    html = "<root></root>"
    sel = Selector(text=html)
    assert sel.xpath("//missing/text()").get(default="nothing") == "nothing"

def test_extract_list():
    html = '<ul><li>egg</li><li>cheese</li></ul>'
    sel = Selector(text=html)
    result = sel.css('li::text').getall()
    assert result == ["egg", "cheese"]

def test_error_handling_wrong_type():
    with pytest.raises(TypeError):
        Selector(text=object())