import pytest
import sys
sys.path.insert(0, 'src')
from http_errors import createError

def test_throw_for_unsupported_argument_type_bigint():
    # Simulate JS BigInt: use SimulatedBigInt
    with pytest.raises(TypeError, match="unsupported type bigint"):
        createError(400, createError.SimulatedBigInt(10))

def test_default_to_500_when_given_another_unknown_status():
    err = createError(12345)
    assert err.status == 500
    assert err.statusCode == 500
    assert getattr(err, 'message', None) == 'Internal Server Error'

def test_deprecate_status_below_400_status_304():
    err = createError(304)
    assert err.status == 304
    assert err.statusCode == 304
    assert getattr(err, 'message', None) == 'Not Modified'

def test_create_abstract_HttpError_constructor_cannot_be_instantiated_public():
    with pytest.raises(TypeError):
        createError.HttpError()

def test_constructors_for_standard_status_codes_as_properties_gone():
    e = createError.Gone()
    assert e.status == 410
    assert e.statusCode == 410
    assert getattr(e, 'message', None) == 'Gone'
    assert isinstance(e, createError.HttpError)

def test_not_overwrite_status_statusCode_from_props_argument_gone():
    err = createError(410, 'Other Message', {'status': 412, 'statusCode': 413})
    assert err.status == 410
    assert err.statusCode == 410

def test_allow_properties_through_props_allow_info_extra():
    err = createError(401, 'oops', {'expose': True, 'info': 'extra'})
    assert getattr(err, 'message', None) == 'oops'
    assert getattr(err, 'expose', None) is True
    assert getattr(err, 'info', None) == 'extra'

class TestCreateError_isHttpError_public:
    def test_returns_false_for_undefined(self):
        assert createError.isHttpError(None) is False

    def test_returns_false_for_generic_object(self):
        assert createError.isHttpError({}) is False

    def test_returns_false_for_error_with_only_statusCode(self):
        err = Exception('fail')
        err.statusCode = 404
        assert createError.isHttpError(err) is False