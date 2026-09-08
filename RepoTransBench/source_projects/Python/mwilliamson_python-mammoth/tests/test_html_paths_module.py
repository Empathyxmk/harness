import mammoth.html_paths as html_paths

def test_empty_elements_equals():
    a = html_paths.Empty()
    b = html_paths.Empty()
    assert a == b
    assert hash(a) == hash(b)
    assert str(a).startswith("Empty")

def test_fresh_path_element_html_generates_tag():
    e = html_paths.fresh_element("p")
    node = e.html("hi")
    assert hasattr(node, "tag")
    assert node.tag == "p"

def test_html_path_append_and_repr():
    a = html_paths.path(["div", "span"])
    b = a.append(html_paths.fresh_element("em"))
    assert b.elements[-1].tag_name == "em"
    assert "HtmlPath" in repr(a)

def test_html_path_equality_and_hash():
    p1 = html_paths.path(["div"])
    p2 = html_paths.path(["div"])
    assert p1 == p2
    assert hash(p1) == hash(p2)
    # Should not be equal after append
    p3 = p1.append(html_paths.fresh_element("span"))
    assert p1 != p3

def test_element_repr():
    e = html_paths.fresh_element("code")
    assert "Element" in repr(e)

def test_html_path_wraps_correctly():
    p = html_paths.path(["div"])
    wrapped = p.wrap("hello")
    # Result is some node structure
    assert wrapped is not None

def test_fresh_element_class_attributes():
    e = html_paths.fresh_element("i", class_names=["bold"])
    assert "bold" in e.class_names