# Fix import failure by ensuring the package directory is in sys.path
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import_rdflib_jsonld():
    import rdflib_jsonld
    assert hasattr(rdflib_jsonld, '__doc__')
    assert hasattr(rdflib_jsonld, '__version__')
    assert hasattr(rdflib_jsonld, '__author__')
    assert hasattr(rdflib_jsonld, '__contact__')
    assert hasattr(rdflib_jsonld, '__docformat__')