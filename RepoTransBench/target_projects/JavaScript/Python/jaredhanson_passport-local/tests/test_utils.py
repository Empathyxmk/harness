from passport_local.utils import lookup

def test_returns_found_field_at_root():
    assert lookup({'foo': 'bar'}, 'foo') == 'bar'

def test_returns_found_nested_field_with_brackets():
    assert lookup({'foo': {'bar': 'baz'}}, 'foo[bar]') == 'baz'

def test_returns_null_if_not_found():
    assert lookup({'foo': {}}, 'foo[bar]') is None
    assert lookup({'foo': 'bar'}, 'doesnotexist') is None
    assert lookup(None, 'foo') is None

def test_returns_non_object_field_in_deep_nesting():
    assert lookup({'foo': {'bar': {'baz': 7}}}, 'foo[bar][baz]') == 7

def test_returns_null_for_undefined_along_chain():
    assert lookup({'foo': None}, 'foo[bar]') is None

def test_returns_null_for_empty_string_field_on_chain():
    assert lookup({'foo': {'': 1}}, 'foo[]') == 1