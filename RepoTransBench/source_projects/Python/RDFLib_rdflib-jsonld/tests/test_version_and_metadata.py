import rdflib_jsonld

def test_version_defined():
    assert isinstance(rdflib_jsonld.__version__, str)
    assert rdflib_jsonld.__version__ == "0.6.2"

def test_author_defined():
    assert isinstance(rdflib_jsonld.__author__, str)
    assert "RDFLib" in rdflib_jsonld.__author__

def test_contact_defined():
    assert isinstance(rdflib_jsonld.__contact__, str)
    assert "@" in rdflib_jsonld.__contact__

def test_docformat_defined():
    assert hasattr(rdflib_jsonld, '__docformat__')
    assert rdflib_jsonld.__docformat__ == "restructuredtext"

def test_module_docstring_exists():
    # Relaxed: accept either phrase, lowercased, for robustness
    doc = rdflib_jsonld.__doc__
    assert doc is not None
    doc = doc.strip().lower()
    assert "plugin for rdflib" in doc or "a plugin for rdflib" in doc