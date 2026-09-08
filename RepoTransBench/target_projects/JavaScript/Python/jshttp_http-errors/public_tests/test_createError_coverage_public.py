import pytest
import sys
sys.path.insert(0, 'src')
from http_errors import createError

def test_accept_error_and_preserve_status_different_status():
    original_error = Exception('origin')
    original_error.status = 402
    err = createError(original_error)
    assert err.status == 402
    assert str(err) == 'origin' or getattr(err, 'message', None) == 'origin'
    assert isinstance(err, Exception)

def test_accept_number_string_different():
    err = createError(403, 'Forbidden here')
    assert err.status == 403
    assert err.statusCode == 403
    assert getattr(err, 'message', None) == 'Forbidden here'

def test_accept_number_object_with_detail():
    err = createError(401, {'reason': 'denied'})
    assert err.status == 401
    assert err.statusCode == 401
    assert getattr(err, 'reason', None) == 'denied'

def test_accept_string_object_new():
    err = createError('Unique error', {'bar': 2})
    assert err.status == 500
    assert err.statusCode == 500
    assert getattr(err, 'bar', None) == 2
    assert getattr(err, 'message', None) == 'Unique error'

def test_accept_number_string_object_different():
    err = createError(401, 'No access', {'info': 'xyz'})
    assert err.status == 401
    assert err.statusCode == 401
    assert getattr(err, 'info', None) == 'xyz'
    assert getattr(err, 'message', None) == 'No access'

def test_throw_on_unsupported_type_symbol():
    with pytest.raises(TypeError, match="unsupported type symbol"):
        createError(400, createError.SimulatedSymbol('nope'))

def test_non_number_status_fallback_to_500_different_object():
    err = createError({'bar': 'baz'}, 'AltMsg')
    assert err.status == 500
    assert err.statusCode == 500
    assert getattr(err, 'message', None) == 'AltMsg'
    assert getattr(err, 'bar', None) == 'baz'

def test_not_add_props_with_forbidden_keys_allow_others():
    err = createError(403, 'bar', {'status': 200, 'statusCode': 201, 'y': 2})
    assert err.status == 403
    assert err.statusCode == 403
    assert getattr(err, 'y', None) == 2
    assert err.status == err.statusCode

def test_create_custom_error_classes_via_named_export_gone():
    Gone = createError.Gone
    err = Gone('No longer here')
    assert err.status == 410
    assert err.statusCode == 410
    assert getattr(err, 'message', None) == 'No longer here'
    assert getattr(err, 'name', None) == 'GoneError'

def test_expose_and_name_correct_properties_for_different_client_error():
    Unauthorized = createError.Unauthorized
    err = Unauthorized()
    assert err.status == 401
    assert getattr(err, 'name', None) == 'UnauthorizedError'
    assert getattr(err, 'expose', None) is True

def test_expose_and_name_correct_properties_for_different_server_error():
    BadGateway = createError.BadGateway
    err = BadGateway()
    assert err.status == 502
    assert getattr(err, 'name', None) == 'BadGatewayError'
    assert getattr(err, 'expose', None) is False

def test_use_custom_error_class_for_another_specific_status_code():
    err = createError(401)
    assert err.status == 401
    assert getattr(err, 'name', None) == 'UnauthorizedError'
    assert getattr(err, 'message', None) == 'Unauthorized'

def test_isHttpError_false_for_different_nonobjects_and_null():
    isHttpError = createError.isHttpError
    for v in [None, float('nan'), 1, 'hello', True]:
        assert not isHttpError(v)

def test_isHttpError_true_for_instance_of_another_HttpError():
    err = createError.Gone()
    assert createError.isHttpError(err) is True

def test_isHttpError_true_for_different_generic_error_with_status_statusCode_expose():
    err = Exception('bar')
    err.status = 418
    err.statusCode = 418
    err.expose = True
    assert createError.isHttpError(err) is True

def test_isHttpError_false_for_error_lacking_expose():
    err = Exception('baz')
    err.status = 418
    err.statusCode = 418
    assert createError.isHttpError(err) is False