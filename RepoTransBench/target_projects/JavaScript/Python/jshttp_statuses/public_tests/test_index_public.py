import pytest
from src.statuses import status

def test_exports_a_function_public():
    assert callable(status)

def test_status_code_number_returns_status_message_public():
    assert status(201) == 'Created'
    assert status(403) == 'Forbidden'
    assert status(418) == "I'm a Teapot"

def test_status_code_string_number_returns_status_message_public():
    assert status('201') == 'Created'
    assert status('418') == "I'm a Teapot"

def test_status_code_string_message_returns_status_code_public():
    assert status('created') == 201
    assert status('FORBIDDEN') == 403
    assert status("I'm a Teapot") == 418

def test_status_throws_on_unknown_string_message_public():
    with pytest.raises(ValueError, match="invalid status message"):
        status('foo')
    with pytest.raises(ValueError):
        status('Definitely Not A Status')

def test_status_throws_on_unknown_code_number_public():
    with pytest.raises(ValueError, match="invalid status code"):
        status(777)
    with pytest.raises(ValueError):
        status('777')

@pytest.mark.parametrize("val", [
    [123],
    {'foo': 'bar'},
    None,
    False,
])
def test_status_throws_on_invalid_type_public(val):
    with pytest.raises(TypeError, match="number or string"):
        status(val)

def test_status_codes_is_array_of_numbers_public():
    assert isinstance(status.codes, list) or isinstance(status.codes, tuple)
    assert 201 in status.codes
    assert 403 in status.codes
    assert 418 in status.codes
    assert any(c > 208 for c in status.codes)

def test_status_message_is_object_with_code_keys_public():
    assert isinstance(status.message, dict)
    assert status.message['201'] == 'Created'
    assert status.message['403'] == 'Forbidden'

def test_status_code_is_lowercased_map_public():
    assert isinstance(status.code, dict)
    assert status.code['created'] == 201
    assert status.code['forbidden'] == 403
    assert status.code["i'm a teapot"] == 418

def test_status_redirect_contains_specific_codes_public():
    assert status.redirect[303] is True
    assert status.redirect[305] is True
    assert status.redirect[307] is True
    assert not status.redirect.get(403, False)

def test_status_empty_contains_specific_codes_public():
    assert status.empty[204] is True
    assert status.empty[205] is True
    assert status.empty[304] is True
    assert not status.empty.get(403, False)

def test_status_retry_contains_specific_codes_public():
    assert status.retry[503] is True
    assert status.retry[504] is True
    assert status.retry[502] is True
    assert not status.retry.get(400, False)

def test_status_is_case_insensitive_for_string_messages_public():
    assert status('cReAtEd') == 201
    assert status('FoRbIdDeN') == 403