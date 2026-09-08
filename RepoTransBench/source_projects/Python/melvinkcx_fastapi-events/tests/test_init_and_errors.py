import pytest
from fastapi_events import handler_store, event_store, in_req_res_cycle, middleware_identifier
import fastapi_events.errors as errors

def test_init_vars():
    assert isinstance(handler_store, dict)
    # event_store and others are ContextVar
    assert hasattr(event_store, 'set')
    assert hasattr(in_req_res_cycle, 'set')
    assert hasattr(middleware_identifier, 'set')

def test_FastapiEventError_is_raised():
    with pytest.raises(errors.FastapiEventError):
        raise errors.FastapiEventError("an error")

def test_ConfigurationError_is_raised():
    with pytest.raises(errors.ConfigurationError):
        raise errors.ConfigurationError("bad config")

def test_MissingEventNameError_is_raised():
    with pytest.raises(errors.MissingEventNameError):
        raise errors.MissingEventNameError("missing name")

def test_MissingEventNameDuringRegistration():
    with pytest.raises(errors.MissingEventNameDuringRegistration) as e:
        raise errors.MissingEventNameDuringRegistration()
    assert "__event_name__" in str(e.value)

def test_MissingEventNameDuringDispatch():
    with pytest.raises(errors.MissingEventNameDuringDispatch) as e:
        raise errors.MissingEventNameDuringDispatch()
    assert "'event_name'" in str(e.value)

def test_MultiplePayloadsDetectedDuringDispatch():
    with pytest.raises(errors.MultiplePayloadsDetectedDuringDispatch) as e:
        raise errors.MultiplePayloadsDetectedDuringDispatch()
    assert "Multiple payloads" in str(e.value)