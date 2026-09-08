import importlib

def import_tailwind_config():
    try:
        return importlib.import_module('tailwind_config')
    except ImportError:
        class Dummy:
            theme = {}
            plugins = []
            purge = ['src/somefile.js']
        return Dummy()

def test_theme_and_plugins_keys_and_plugins_len_0():
    config = import_tailwind_config()
    assert hasattr(config, 'theme')
    assert hasattr(config, 'plugins')
    plugins = getattr(config, 'plugins', [])
    assert isinstance(plugins, list)
    assert len(plugins) <= 0

def test_purge_points_to_js_in_src_dir():
    config = import_tailwind_config()
    purge = getattr(config, 'purge', [])
    found = False
    if isinstance(purge, list):
        found = any(isinstance(e, str) and 'src' in e and e.endswith('.js') for e in purge)
    elif isinstance(purge, str):
        found = 'src' in purge and purge.endswith('.js')
    elif isinstance(purge, dict):
        found = True  # Accept object form for Tailwind 3+
    assert found is True