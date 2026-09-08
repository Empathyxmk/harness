import pytest

try:
    from src.insane import insane
except ImportError:
    import sys
    insane = sys.modules.get('insane', None)

def test_export_defaults_object():
    assert insane is not None
    assert isinstance(insane.defaults, dict)
    assert insane.defaults is not None

def test_sanitize_html_with_defaults_and_strip_unsafe_content():
    html = '<p style="color:red">Safe <script>bad()</script>text <img src="javascript:bad()" /></p>'
    result = insane(html)
    assert '<p' in result
    assert 'Safe' in result
    assert 'script' not in result
    assert 'javascript:bad()' not in result
    assert '<img' in result

def test_allow_safe_urls_with_custom_allowed_options():
    html = '<img src="https://safeimage.com/x.png">'
    opts = {
        "allowedTags": ['img'],
        "allowedAttributes": {'img': ['src']},
        "allowedSchemes": ['https']
    }
    result = insane(html, opts, True)
    assert 'src="https://safeimage.com/x.png"' in result
    assert '<img' in result

def test_work_with_strict_true_config():
    html = '<section class="main">abc</section>'
    opts = {
        "allowedTags": ['section'],
        "allowedAttributes": {'section': ['class']},
        "allowedClasses": {'section': ['main']}
    }
    result = insane(html, opts, True)
    assert 'class="main"' in result
    assert 'section' in result

def test_return_fallback_to_defaults_if_strict_not_true():
    html = '<br nobr>'
    opts = {
        "allowedTags": ['br'],
        "allowedAttributes": {'br': ['nobr']}
    }
    result = insane(html, opts)
    assert '<br' in result