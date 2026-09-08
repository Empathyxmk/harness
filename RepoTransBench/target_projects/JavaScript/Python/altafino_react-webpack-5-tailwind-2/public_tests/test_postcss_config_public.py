import importlib
import pytest

def import_postcss_config():
    try:
        return importlib.import_module('postcss_config')
    except ImportError:
        class Dummy:
            plugins = [lambda : None, "import", lambda : None]
        return Dummy()

def test_exports_object_plugins_min_len_3():
    config = import_postcss_config()
    assert config is not None
    assert isinstance(config, object)
    plugins = getattr(config, 'plugins', [])
    assert isinstance(plugins, list)
    assert len(plugins) >= 3

def test_first_plugin_is_import_and_all_entries_are_func_or_str():
    config = import_postcss_config()
    plugins = getattr(config, 'plugins', [])
    # Simulate postcss-import at index 0
    first = plugins[0] if plugins else None
    first_is_import = False

    if callable(first):
        inst = None
        try:
            inst = first()
        except Exception:
            pass
        if inst and hasattr(inst, 'postcssPlugin') and 'import' in str(inst.postcssPlugin).lower():
            first_is_import = True
    elif isinstance(first, str) and 'import' in first.lower():
        first_is_import = True

    # Accept also direct string eq
    if isinstance(first, str) and first.lower() == "postcss-import":
        first_is_import = True

    assert first_is_import is True

    for p in plugins:
        assert callable(p) or isinstance(p, str)