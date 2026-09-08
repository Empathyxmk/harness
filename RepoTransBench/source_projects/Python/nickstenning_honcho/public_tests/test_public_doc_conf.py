def test_public_doc_conf_imports():
    import doc.conf
    assert hasattr(doc.conf, "extensions")
    assert isinstance(doc.conf.extensions, list)
    assert "sphinx.ext.autodoc" in doc.conf.extensions