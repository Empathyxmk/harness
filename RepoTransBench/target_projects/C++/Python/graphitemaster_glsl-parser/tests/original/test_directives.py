import pytest

def test_directives_version_and_extension():
    # Simulate GLSL preprocessor directives
    version_line = "#version 330 core"
    extension_line = "#extension all : enable"
    
    assert version_line.startswith("#version")
    assert extension_line.startswith("#extension")
    assert "core" in version_line
    assert "enable" in extension_line