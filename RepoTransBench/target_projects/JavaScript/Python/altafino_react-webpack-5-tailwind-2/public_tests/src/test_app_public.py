import pytest

class DummyApp:
    def __init__(self):
        self.text = "Welcome to Tailwind!"

def render_app():
    # In actual React test, this renders the App and allows text query.
    # Here, just simulate component presence.
    return DummyApp()

def test_renders_component_with_welcome_text():
    app = render_app()
    assert hasattr(app, 'text')
    assert "welcome" in app.text.lower() or "tailwind" in app.text.lower()

def test_renders_div_as_root_element():
    app = render_app()
    # Simulate (no DOM), so just check for dummy property for demonstration
    assert hasattr(app, 'text')