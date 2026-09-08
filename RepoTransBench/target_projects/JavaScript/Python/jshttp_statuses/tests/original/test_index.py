import pytest
from src.statuses import status

def test_exports_a_function():
    assert callable(status)

def test_status_code_number_returns_status_message():
    assert status(200) == 'OK'
    assert status(404) == 'Not Found'
    assert status(500) == 'Internal Server Error'

def test_status_code_string_number_returns_status_message():
    assert status('200') == 'OK'
    assert status('404') == 'Not Found'

def test_status_code_string_message_returns_status_code():
    assert status('not found') == 404
    assert status('OK') == 200
    assert status('Internal Server Error') == 500

def test_status_throws_on_unknown_string_message():
    with pytest.raises(ValueError, match="invalid status message"):
        status('wut')
    with pytest.raises(ValueError):
        status('Nonexistent Status')

def test_status_throws_on_unknown_code_number():
    with pytest.raises(ValueError, match="invalid status code"):
        status(999)
    with pytest.raises(ValueError):
        status('999')

@pytest.mark.parametrize("val", [
    [],
    {},
    None,
    True,
    # Python has no 'undefined'
])
def test_status_throws_on_invalid_type(val):
    with pytest.raises(TypeError, match="number or string"):
        status(val)

def test_status_codes_is_array_of_numbers():
    assert isinstance(status.codes, list) or isinstance(status.codes, tuple)
    assert 200 in status.codes
    assert 404 in status.codes
    assert 500 in status.codes
    # Spot check for any int in codes
    assert any(isinstance(c, int) for c in status.codes)

def test_status_message_is_object_with_code_keys():
    assert isinstance(status.message, dict)
    assert status.message['200'] == 'OK'
    assert status.message['404'] == 'Not Found'

def test_status_code_is_lowercased_message_map_to_code():
    assert isinstance(status.code, dict)
    assert status.code['ok'] == 200
    assert status.code['not found'] == 404
    assert status.code['internal server error'] == 500

def test_status_redirect_contains_specific_codes():
    assert status.redirect[301] is True
    assert status.redirect[302] is True
    assert status.redirect[308] is True
    assert not status.redirect.get(200, False)

def test_status_empty_contains_specific_codes():
    assert status.empty[204] is True
    assert status.empty[205] is True
    assert status.empty[304] is True
    assert not status.empty.get(404, False)

def test_status_retry_contains_specific_codes():
    assert status.retry[502] is True
    assert status.retry[503] is True
    assert status.retry[504] is True
    assert not status.retry.get(501, False)

def test_status_is_case_insensitive_for_string_messages():
    assert status('iNtErNaL sErVeR eRrOr') == 500
    assert status('nOt fOuNd') == 404