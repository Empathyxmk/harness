import pytest

try:
    from src.sanitizer import sanitizer
    from src.elements import elements
except ImportError:
    import sys
    sanitizer = sys.modules.get('sanitizer', None)
    elements = sys.modules.get('elements', None)

def make_base_options():
    return {
        'allowedTags': ['a', 'div', 'span', 'img'],
        'allowedAttributes': {'*': ['href', 'src', 'class'], 'div': ['id'], 'a': ['href'], 'img': ['src']},
        'allowedClasses': {'div': ['cls1', 'cls2'], 'span': ['cls3']},
        'allowedSchemes': ['http', 'https']
    }

@pytest.fixture
def base_options():
    return make_base_options()

@pytest.fixture(autouse=True)
def buffer():
    return []

def test_output_simple_tag_with_allowed_attribute(monkeypatch):
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('a', {'href': 'http://test.com'}, False)
    s.end('a')
    assert ''.join(buffer) == '<a href="http://test.com"></a>'

def test_skip_tag_not_in_allowed_tags():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('script', {'src': 'evil.js'}, False)
    s.end('script')
    assert ''.join(buffer) == ''

def test_filter_out_disallowed_attribute():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('div', {'style': 'color:red', 'id': 'main'}, False)
    s.end('div')
    assert ''.join(buffer) == '<div id="main"></div>'

def test_keep_all_classes_as_allowed_when_class_not_filtered():
    custom_options = {
        'allowedTags': ['div'],
        'allowedAttributes': {'div': ['class']},
        'allowedClasses': {'div': ['cls1', 'other', 'cls2', 'wrongclass']},
        'allowedSchemes': ['http']
    }
    buffer = []
    s = sanitizer(buffer, custom_options)
    s.start('div', {'class': 'cls1 wrongclass cls2'}, False)
    s.end('div')
    assert ''.join(buffer) == '<div class="cls1 wrongclass cls2"></div>'

def test_filter_out_disallowed_classes():
    custom_options = {
        'allowedTags': ['div'],
        'allowedAttributes': {'div': []},
        'allowedClasses': {'div': ['cls1', 'cls2']},
        'allowedSchemes': ['http']
    }
    buffer = []
    s = sanitizer(buffer, custom_options)
    s.start('div', {'class': 'cls1 wrongclass cls2'}, False)
    s.end('div')
    assert ''.join(buffer) == '<div class="cls1 cls2"></div>'

def test_allow_allowed_schemes_for_uri_attributes():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('a', {'href': 'https://example.com'}, False)
    s.end('a')
    assert ''.join(buffer) == '<a href="https://example.com"></a>'

def test_not_allow_non_whitelisted_schemes():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('a', {'href': 'javascript:alert(1)'}, False)
    s.end('a')
    assert ''.join(buffer) == '<a></a>'

def test_allow_hash_and_slash_in_href():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('a', {'href': '#anchor'}, False)
    s.start('a', {'href': '/path/page'}, False)
    joined = ''.join(buffer)
    assert 'href="#anchor"' in joined
    assert 'href="/path/page"' in joined

def test_allow_transform_text_option():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div']
    opts['transformText'] = lambda txt: txt.upper()
    s = sanitizer(buffer, opts)
    s.start('div', {}, False)
    s.chars('hello!')
    s.end('div')
    assert ''.join(buffer) == '<div>HELLO!</div>'

def test_handle_unary_tags_self_closing():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('img', {'src': 'http://image'}, True)
    s.end('img')
    assert '<img src="http://image"/>' in ''.join(buffer)

def test_not_echo_tags_when_context_ignoring_is_set():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div']
    s = sanitizer(buffer, opts)
    s.start('script', {}, False)
    s.chars('alert(1)')
    s.end('script')
    assert ''.join(buffer) == ''

def test_call_filter_if_present():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['a']
    opts['filter'] = lambda ctx: ctx['attrs'].get('href', '').startswith('h') if 'href' in ctx['attrs'] else False
    s = sanitizer(buffer, opts)
    s.start('a', {'href': 'http://safe'}, False)
    assert 'href="http://safe"' in ''.join(buffer)
    buffer.clear()
    s.start('a', {'href': 'ftp://bad'}, False)
    assert 'ftp://bad' not in ''.join(buffer)

def test_write_chars_only_outside_ignored_context():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div']
    s = sanitizer(buffer, opts)
    s.start('div', {}, False)
    s.chars('word')
    assert 'word' in ''.join(buffer)

def test_ignore_void_elements_in_ignore():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['br']
    s = sanitizer(buffer, opts)
    s.start('br', {}, True)
    s.end('br')
    assert '<br/>' in ''.join(buffer)

def test_support_nested_ignored_tags():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div']
    s = sanitizer(buffer, opts)
    s.start('script', {}, False)
    s.start('script', {}, False)
    s.end('script')
    s.chars('content')
    s.end('script')
    s.start('div', {}, False)
    s.chars('hi')
    s.end('div')
    assert ''.join(buffer) == '<div>hi</div>'

def test_close_tags_when_not_ignoring():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div', 'style']
    s = sanitizer(buffer, opts)
    s.start('div', {}, False)
    s.end('div')
    assert ''.join(buffer) == '<div></div>'

def test_unignore_and_reset_context_after_ignoring():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div', 'style']
    s = sanitizer(buffer, opts)
    s.start('style', {}, False)
    s.end('style')
    s.start('div', {}, False)
    s.chars('okay')
    s.end('div')
    assert ''.join(buffer) == '<style></style><div>okay</div>'

def test_handle_tags_not_unignored_normally():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['div', 'style']
    s = sanitizer(buffer, opts)
    s.start('style', {}, False)
    s.end('div')
    assert ''.join(buffer) == '<style></div>'

def test_handle_when_allowed_tags_is_undefined():
    buffer = []
    s = sanitizer(buffer, {})
    s.start('h1', {'foo': 'bar'}, False)
    assert ''.join(buffer) == ''

def test_testurl_handle_questionmark_and_hash_before_colon():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['a']
    opts['allowedSchemes'] = ['http']
    s = sanitizer(buffer, opts)
    s.start('a', {'href': '?foo:bar'}, False)
    s.end('a')
    assert ''.join(buffer) == '<a href="?foo:bar"></a>'
    buffer.clear()
    s.start('a', {'href': '#foo:bar'}, False)
    s.end('a')
    assert ''.join(buffer) == ''

def test_testurl_handle_allowed_schemes_matching_at_beginning():
    buffer = []
    opts = make_base_options()
    opts['allowedTags'] = ['a']
    opts['allowedSchemes'] = ['ftp', 'http']
    s = sanitizer(buffer, opts)
    s.start('a', {'href': 'ftp://site.com'}, False)
    s.end('a')
    assert ''.join(buffer) == '<a href="ftp://site.com"></a>'

def test_not_output_attribute_if_value_is_undefined():
    buffer = []
    opts = make_base_options()
    s = sanitizer(buffer, opts)
    s.start('a', {}, False)
    s.end('a')
    assert ''.join(buffer) == '<a></a>'