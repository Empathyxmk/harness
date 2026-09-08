import pytest

try:
    from src.insane import insane
except ImportError:
    import sys
    insane = sys.modules.get('insane', None)

def test_export_defaults():
    assert insane is not None
    assert hasattr(insane, "defaults")

def test_sanitize_html_with_defaults():
    # Given HTML string with unsafe event handlers and JS URLs
    html = '<div onclick="evil()">hello <a href="javascript:evil()">link</a></div>'
    result = insane(html)
    assert '<div>' in result
    assert 'hello' in result
    assert 'onclick' not in result
    assert '<a>' in result

def test_allow_allowed_options():
    html = '<a href="http://safe">ok</a>'
    opts = {
        "allowedTags": ['a'],
        "allowedAttributes": {'a': ['href']},
        "allowedSchemes": ['http']
    }
    result = insane(html, opts, True)
    assert 'href="http://safe"' in result
    assert '<a' in result

def test_strict_mode_works():
    html = '<span class="asdf">xx</span>'
    opts = {
        "allowedTags": ['span'],
        "allowedAttributes": {'span': ['class']},
        "allowedClasses": {'span': ['asdf']}
    }
    result = insane(html, opts, True)
    assert 'class="asdf"' in result

def test_fallback_to_defaults_if_strict_not_true():
    html = '<hr noshade>'
    opts = {
        "allowedTags": ['hr'],
        "allowedAttributes": {'hr': ['noshade']}
    }
    result = insane(html, opts)
    assert '<hr' in result