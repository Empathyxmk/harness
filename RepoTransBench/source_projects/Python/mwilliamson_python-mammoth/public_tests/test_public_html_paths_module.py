import pytest
from mammoth import html_paths

def test_element_repr_public():
    el = html_paths.element("strong", class_names=["main1", "main2"], is_self_closing=False)
    r = repr(el)
    assert "strong" in r and "main1" in r

def test_element_eq_ne_public():
    el1 = html_paths.element("em", class_names=["cls1"], is_self_closing=False)
    el2 = html_paths.element("em", class_names=["cls2"], is_self_closing=False)
    assert el1 != el2
    el3 = html_paths.element("em", class_names=["cls1"], is_self_closing=False)
    assert el1 == el3

def test_path_repr_public():
    path = html_paths.path([html_paths.element("u"), html_paths.element("s")])
    text = repr(path)
    assert "u" in text and "s" in text

def test_path_eq_ne_public():
    el1 = html_paths.element("b")
    el2 = html_paths.element("em")
    path1 = html_paths.path([el1, el2])
    path2 = html_paths.path([el1, el2])
    path3 = html_paths.path([el1])
    assert path1 == path2
    assert path1 != path3

def test_empty_path_singleton_public():
    assert html_paths.empty_path is html_paths.path([])

def test_class_names_hash_public():
    c1 = html_paths._ClassNames(["x", "y"])
    c2 = html_paths._ClassNames(["x", "y"])
    c3 = html_paths._ClassNames(["z"])
    assert hash(c1) == hash(c2)
    assert hash(c1) != hash(c3)