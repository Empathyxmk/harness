import pytest

def fake_animations():
    return True

def test_should_export_something_from_animations_public():
    animations = fake_animations
    assert animations
    assert callable(animations)