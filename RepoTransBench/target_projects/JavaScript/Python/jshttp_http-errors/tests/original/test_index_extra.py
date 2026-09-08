import pytest
import sys
sys.path.insert(0, 'src')
from http_errors import createError

def test_throws_for_unsupported_argument_type_symbol():
    # Simulate JS Symbol: use SimulatedSymbol
    with pytest.raises(TypeError, match="unsupported type symbol"):
        createError(404, createError.SimulatedSymbol('test'))

def test_default_to_500_when_given_unknown_status():
    err = createError(9999)
    assert err.status == 500
    assert err.statusCode == 500
    assert getattr(err, 'message', None) == 'Internal Server Error'

def test_deprecate_status_below_400_still_works():
    err = createError(200)
    assert err.status == 200
    assert err.statusCode == 200
    assert getattr(err, 'message', None) == 'OK'

def test_create_abstract_HttpError_constructor_cannot_be_instantiated():
    with pytest.raises(TypeError):
        createError.HttpError()

def test_constructors_for_standard_status_codes_as_properties():
    e = createError.NotFound()
    assert e.status == 404
    assert e.statusCode == 404
    assert getattr(e, 'message', None) == 'Not Found'
    assert isinstance(e, createError.HttpError)

def test_not_overwrite_status_statusCode_from_props_argument():
    err = createError(404, 'Message', {'status': 401, 'statusCode': 402})
    assert err.status == 404
    assert err.statusCode == 404

def test_allow_properties_through_props():
    err = createError(404, 'foo', {'expose': False, 'custom': True})
    assert getattr(err, 'message', None) == 'foo'
    assert getattr(err, 'expose', None) is False
    assert getattr(err, 'custom', None) is True

class Test_isHttpError_group:
    def test_returns_false_for_non_object(self):
        assert createError.isHttpError(None) is False

    def test_returns_false_for_plain_error(self):
        assert createError.isHttpError(Exception('fail')) is False