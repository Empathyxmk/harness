import pytest

class FontExample:
    @staticmethod
    def get_available_font_family_names():
        # Simulate
        return ["Arial", "Monospaced", "Times", "DialogInput"]

def test_get_available_font_family_names_public():
    font_names = FontExample.get_available_font_family_names()
    assert font_names is not None
    found = any(font in ("Monospaced", "DialogInput") for font in font_names)
    assert found, "Should have some basic monospace font family available"