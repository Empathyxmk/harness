import pytest
from parsel.selector import SelectorList, CannotRemoveElementWithoutRoot, CannotRemoveElementWithoutParent, CannotDropElementWithoutParent, create_root_node
from lxml import etree, html

def test_selectorlist_getstate_not_pickle():
    sel_list = SelectorList()
    with pytest.raises(TypeError):
        sel_list.__getstate__()

def test_root_node_empty_text_html():
    # Should parse as HTML if not specified XML
    n = create_root_node("", html.HTMLParser)
    assert etree.iselement(n)

def test_root_node_huge_tree_warn(monkeypatch):
    import warnings
    from parsel import selector
    monkeypatch.setattr(selector, "LXML_SUPPORTS_HUGE_TREE", False)
    logs = []
    def fake_warn(msg, stacklevel=2):
        logs.append(msg)
    monkeypatch.setattr(warnings, "warn", fake_warn)
    n = create_root_node("test", html.HTMLParser, huge_tree=False)
    assert etree.iselement(n)

def test_exceptions_inheritance():
    assert issubclass(CannotDropElementWithoutParent, CannotRemoveElementWithoutParent)
    assert issubclass(CannotRemoveElementWithoutParent, Exception)
    assert issubclass(CannotRemoveElementWithoutRoot, Exception)