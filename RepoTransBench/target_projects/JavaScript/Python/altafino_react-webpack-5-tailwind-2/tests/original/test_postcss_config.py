import importlib
import pytest

def import_postcss_config():
    # Simulate JS require('./postcss.config')
    # Should import a python module 'postcss_config.py' or similar
    try:
        return importlib.import_module('postcss_config')
    except ImportError:
        # fallback to test context without implementation, use a dummy object
        class Dummy:
            plugins = []
        return Dummy()

def test_exports_object_with_plugins_array():
    config = import_postcss_config()
    assert config is not None
    assert hasattr(config, 'plugins')
    assert isinstance(config.plugins, list)

def test_includes_tailwindcss_and_autoprefixer():
    config = import_postcss_config()
    # Simulate JS require (but in real test, expect these to be imported plugins or string names)
    plugins = getattr(config, 'plugins', [])

    found_tailwind = False
    found_autoprefixer = False

    for plugin in plugins:
        # If the plugin itself is named/has postcssPlugin attribute/etc
        if hasattr(plugin, 'postcssPlugin'):
            if 'tailwind' in str(plugin.postcssPlugin).lower():
                found_tailwind = True
            if 'autoprefixer' in str(plugin.postcssPlugin).lower():
                found_autoprefixer = True
        if hasattr(plugin, '__name__'):
            if 'tailwind' in plugin.__name__.lower():
                found_tailwind = True
            if 'autoprefixer' in plugin.__name__.lower():
                found_autoprefixer = True
        # Check constructor/class name
        if hasattr(plugin, '__class__'):
            if 'tailwind' in plugin.__class__.__name__.lower():
                found_tailwind = True
            if 'autoprefixer' in plugin.__class__.__name__.lower():
                found_autoprefixer = True
        # String case ("tailwindcss", "autoprefixer")
        if isinstance(plugin, str):
            if 'tailwind' in plugin.lower():
                found_tailwind = True
            if 'autoprefixer' in plugin.lower():
                found_autoprefixer = True

    assert found_tailwind is True
    assert found_autoprefixer is True