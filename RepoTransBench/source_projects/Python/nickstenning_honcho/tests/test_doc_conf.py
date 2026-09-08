import types
import importlib.util

def test_doc_conf_loadable():
    # Ensure doc/conf.py can be parsed and loaded as a module, for branch coverage
    import os
    conf_path = os.path.join(os.path.dirname(__file__), "../doc/conf.py")
    spec = importlib.util.spec_from_file_location("conf", conf_path)
    conf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf_module)
    assert hasattr(conf_module, "project") or hasattr(conf_module, "copyright")

def test_doc_conf_rst_epub_extras(monkeypatch):
    # Check RST/epub configs branch if present
    import os
    conf_path = os.path.join(os.path.dirname(__file__), "../doc/conf.py")
    spec = importlib.util.spec_from_file_location("conf", conf_path)
    conf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf_module)
    # EPUB config branches
    if hasattr(conf_module, 'epub_exclude_files'):
        assert isinstance(conf_module.epub_exclude_files, list)

def test_doc_conf_html_theme_options(monkeypatch):
    # Check HTML theme options if defined
    import os
    conf_path = os.path.join(os.path.dirname(__file__), "../doc/conf.py")
    spec = importlib.util.spec_from_file_location("conf", conf_path)
    conf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf_module)
    if hasattr(conf_module, 'html_theme_options'):
        assert isinstance(conf_module.html_theme_options, dict)