from src.renderEmail import render_email

def test_returns_doctype_markup_simple_tree_public_variant():
    class Comp:
        def __call__(self):
            return "<html><body><h2>Hello World!</h2></body></html>"
    output = render_email(Comp())
    assert output.startswith("<!DOCTYPE html")
    assert "<h2>Hello World!</h2>" in output

def test_works_with_bare_span_element_public_variant():
    class DummySpan:
        tag = 'span'
    output = render_email(DummySpan())
    assert "<span" in output