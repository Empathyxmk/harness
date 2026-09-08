import pytest
from src.statuses import status

def test_arguments_code_should_be_required():
    with pytest.raises(TypeError, match='code must be'):
        status()

def test_arguments_code_accepts_number():
    assert status(200) == 'OK'

def test_arguments_code_accepts_string():
    assert status('OK') == 200

def test_arguments_code_accepts_string_number():
    assert status('200') == 'OK'

def test_arguments_code_rejects_object():
    with pytest.raises(TypeError, match='code must be'):
        status({})

def test_when_given_number_returns_message_for_valid_status_code():
    assert status(200) == 'OK'
    assert status(404) == 'Not Found'
    assert status(500) == 'Internal Server Error'

def test_when_given_number_throws_for_invalid_status_code():
    with pytest.raises(ValueError, match='invalid status code'):
        status(0)
    with pytest.raises(ValueError, match='invalid status code'):
        status(1000)

def test_when_given_number_throws_for_unknown_status_code():
    with pytest.raises(ValueError, match='invalid status code'):
        status(299)
    with pytest.raises(ValueError, match='invalid status code'):
        status(310)

def test_when_given_number_throws_for_discontinued_status_code():
    with pytest.raises(ValueError, match='invalid status code'):
        status(306)

def test_when_given_string_returns_message_for_valid_status_code():
    assert status('200') == 'OK'
    assert status('404') == 'Not Found'
    assert status('500') == 'Internal Server Error'

def test_when_given_string_truthy_for_valid_status_message():
    assert status('OK')
    assert status('Not Found')
    assert status('Internal Server Error')

def test_when_given_string_is_case_insensitive():
    assert status('Ok')
    assert status('not found')
    assert status('INTERNAL SERVER ERROR')

def test_when_given_string_throws_for_unknown_status_message():
    with pytest.raises(ValueError, match='invalid status message'):
        status('too many bugs')
    with pytest.raises(ValueError, match='invalid status message'):
        status('constructor')
    with pytest.raises(ValueError, match='invalid status message'):
        status('__proto__')

def test_when_given_string_throws_for_unknown_status_code():
    with pytest.raises(ValueError, match='invalid status code'):
        status('299')

def test_codes_includes_expected_codes():
    # Simulate a check for presence of codes, since not importing http.STATUS_CODES
    for code in [200, 404, 500]:
        assert code in status.codes

def test_empty_is_object_and_includes_204():
    assert status.empty
    assert isinstance(status.empty, dict)
    assert status.empty[204]

def test_message_is_map_and_includes_200():
    assert status.message[200] == 'OK'

def test_message_includes_expected_codes():
    for code in ['200', '404', '500']:
        assert status.message[code]

def test_redirect_is_object_and_includes_308():
    assert status.redirect
    assert isinstance(status.redirect, dict)
    assert status.redirect[308]

def test_retry_is_object_and_includes_504():
    assert status.retry
    assert isinstance(status.retry, dict)
    assert status.retry[504]