import pytest

try:
    from src.attributes import attributes
except ImportError:
    # Fallback so tests can still run even if the structure isn't complete yet
    import sys
    attributes = sys.modules.get('attributes', None)

def test_include_known_uri_attributes():
    assert attributes is not None
    assert attributes.uris['href'] is True
    assert attributes.uris['src'] is True
    assert attributes.uris['background'] is True
    assert len(attributes.uris.keys()) > 4

def test_not_include_non_uri_attributes():
    assert attributes.uris.get('style', None) is None