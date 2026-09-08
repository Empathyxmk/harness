import pytest

try:
    from src.attributes import attributes
except ImportError:
    import sys
    attributes = sys.modules.get('attributes', None)

def test_include_other_known_uri_attributes():
    assert attributes is not None
    assert attributes.uris['usemap'] is True
    assert attributes.uris['longdesc'] is True
    assert attributes.uris['base'] is True
    keys = attributes.uris.keys()
    assert set(['href', 'usemap', 'longdesc', 'src', 'cite', 'background', 'base']).issubset(keys)

def test_not_include_random_attribute():
    assert attributes.uris.get('alt') is None
    assert attributes.uris.get('class') is None