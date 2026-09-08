import pytest

class Application:
    pass

def test_application_public_instantiation():
    """Public test for Application class to ensure proper instantiation with a different test class name."""
    app = Application()
    assert app is not None