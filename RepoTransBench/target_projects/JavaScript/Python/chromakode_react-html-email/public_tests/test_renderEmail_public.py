from src.renderEmail import render_email

def test_renders_complex_tree_different_content_public_variant():
    class Comp:
        def __call__(self):
            return "<html><body><h3>Greetings</h3><p>Test paragraph</p></body></html>"
    output = render_email(Comp())
    assert output.startswith("<!DOCTYPE html")
    assert "<h3>Greetings</h3>" in output
    assert "Test paragraph" in output

def test_renders_bare_section_element_public_variant():
    class DummySection:
        tag = 'section'
    output = render_email(DummySection())
    assert "<section" in output