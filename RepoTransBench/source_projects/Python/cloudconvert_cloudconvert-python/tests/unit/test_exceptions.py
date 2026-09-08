import pytest
import cloudconvert.exceptions.exceptions as exceptions

def test_apierror_str():
    e = exceptions.ApiError('msg', code=400)
    assert 'msg' in str(e)
    assert e.code == 400

def test_timeout_exception():
    e = exceptions.TimeoutException('Timeouted!')
    assert isinstance(e, exceptions.TimeoutException)
    assert str(e) == 'Timeouted!'

def test_auth_exception():
    e = exceptions.AuthException('Unauthorized')
    assert isinstance(e, exceptions.AuthException)
    assert str(e) == 'Unauthorized'

def test_parse_exception():
    e = exceptions.ParseException('bad parse')
    assert isinstance(e, exceptions.ParseException)
    assert str(e) == 'bad parse'

def test_invalid_request():
    e = exceptions.InvalidRequest('invalid')
    assert isinstance(e, exceptions.InvalidRequest)
    assert str(e) == 'invalid'

def test_invalid_response():
    e = exceptions.InvalidResponse('invalidresp')
    assert isinstance(e, exceptions.InvalidResponse)
    assert str(e) == 'invalidresp'

def test_connection_failed():
    e = exceptions.ConnectionFailed('fail')
    assert isinstance(e, exceptions.ConnectionFailed)
    assert str(e) == 'fail'