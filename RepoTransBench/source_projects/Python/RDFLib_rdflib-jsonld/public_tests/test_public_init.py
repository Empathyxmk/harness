import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import_rdflib_jsonld_public():
    import rdflib_jsonld
    # Test attribute types instead of only existence
    assert isinstance(rdflib_jsonld.__doc__, str) or rdflib_jsonld.__doc__ is None
    assert isinstance(rdflib_jsonld.__version__, str)
    assert isinstance(rdflib_jsonld.__author__, str)
    assert isinstance(rdflib_jsonld.__contact__, str)
    assert isinstance(rdflib_jsonld.__docformat__, str)