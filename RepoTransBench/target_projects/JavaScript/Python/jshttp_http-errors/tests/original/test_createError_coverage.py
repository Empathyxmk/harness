import pytest
import types

import sys
sys.path.insert(0, 'src')
from http_errors import createError

def test_accept_error_and_preserve_status():
    original_error = Exception('original')
    original_error.status = 403
    err = createError(original_error)
    assert err.status == 403
    assert str(err) == 'original' or getattr(err, 'message', None) == 'original'
    assert isinstance(err, Exception)

def test_accept_number_string():
    err = createError(404, 'Not found')
    assert err.status == 404
    assert err.statusCode == 404
    assert getattr(err, 'message', None) == 'Not found'

def test_accept_number_object():
    err = createError(404, {'detail': 'something'})
    assert err.status == 404
    assert err.statusCode == 404
    assert getattr(err, 'detail', None) == 'something'

def test_accept_string_object():
    err = createError('Custom error', {'foo': 1})
    assert err.status == 500
    assert err.statusCode == 500
    assert getattr(err, 'foo', None) == 1
    assert getattr(err, 'message', None) == 'Custom error'

def test_accept_number_string_object():
    err = createError(400, 'Bad', {'detail': 'foo'})
    assert err.status == 400
    assert err.statusCode == 400
    assert getattr(err, 'detail', None) == 'foo'
    assert getattr(err, 'message', None) == 'Bad'

def test_throw_on_unsupported_type():
    # Simulate JS BigInt: use SimulatedBigInt
    with pytest.raises(TypeError, match="unsupported type bigint"):
        createError(400, createError.SimulatedBigInt(123))

def test_non_number_status_fallback_to_500():
    err = createError({'foo': 'bar'}, 'MyMsg')
    assert err.status == 500
    assert err.statusCode == 500
    assert getattr(err, 'message', None) == 'MyMsg'
    assert getattr(err, 'foo', None) == 'bar'

def test_not_add_props_with_forbidden_keys():
    err = createError(404, 'foo', {'status': 401, 'statusCode': 402, 'x': 1})
    assert err.status == 404
    assert err.statusCode == 404
    assert getattr(err, 'x', None) == 1
    assert err.status == err.statusCode

def test_create_custom_error_classes_via_named_export():
    NotFound = createError.NotFound
    err = NotFound('Nope')
    assert err.status == 404
    assert err.statusCode == 404
    assert getattr(err, 'message', None) == 'Nope'
    assert getattr(err, 'name', None) == 'NotFoundError'

def test_expose_and_name_correct_properties_for_client_errors():
    BadRequest = createError.BadRequest
    err = BadRequest()
    assert err.status == 400
    assert getattr(err, 'name', None) == 'BadRequestError'
    assert getattr(err, 'expose', None) is True

def test_expose_and_name_correct_properties_for_server_errors():
    InternalServerError = createError.InternalServerError
    err = InternalServerError()
    assert err.status == 500
    assert getattr(err, 'name', None) == 'InternalServerError'
    assert getattr(err, 'expose', None) is False

def test_use_custom_error_class_for_specific_status_codes():
    err = createError(404)
    assert err.status == 404
    assert getattr(err, 'name', None) == 'NotFoundError'
    assert getattr(err, 'message', None) == 'Not Found'

# -------- isHttpError tests --------

def test_isHttpError_false_for_nonobjects_and_null():
    isHttpError = createError.isHttpError
    for v in [None, 0, '', False]:
        assert not isHttpError(v)

def test_isHttpError_true_for_instance_of_HttpError():
    err = createError.NotFound()
    assert createError.isHttpError(err) is True

def test_isHttpError_true_for_generic_error_with_status_statusCode_expose():
    err = Exception('foo')
    err.status = 410
    err.statusCode = 410
    err.expose = True
    assert createError.isHttpError(err) is True

def test_isHttpError_false_for_error_lacking_required_shape():
    err = Exception('bar')
    err.status = 410
    assert createError.isHttpError(err) is False