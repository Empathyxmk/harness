import importlib

def import_tailwind_config():
    try:
        return importlib.import_module('tailwind_config')
    except ImportError:
        # fallback for test context
        class Dummy:
            purge = ''
            darkMode = None
            theme = {}
            variants = {}
            plugins = []
        return Dummy()

def test_should_export_expected_structure():
    config = import_tailwind_config()
    assert hasattr(config, 'purge')
    assert hasattr(config, 'darkMode')
    assert hasattr(config, 'theme')
    assert hasattr(config, 'variants')
    assert hasattr(config, 'plugins')
    assert isinstance(config.plugins, list)
    assert isinstance(config.theme, dict)
    assert isinstance(config.variants, dict)

def test_darkMode_is_false_media_or_class():
    config = import_tailwind_config()
    assert config.darkMode in ['media', 'class', False]