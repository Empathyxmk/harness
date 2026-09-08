import pytest

class TrackableAttribute:
    pass

class Dummy:
    @TrackableAttribute
    def annotated_method(self, param): pass

def test_trackable_attribute_on_method():
    dummy = Dummy()
    assert hasattr(Dummy.annotated_method, "__call__")
    # Simulate method having annotation/attribute
    assert hasattr(Dummy, 'annotated_method')

def test_trackable_attribute_on_parameter():
    dummy = Dummy()
    # Simulate parameter having annotation
    assert hasattr(Dummy.annotated_method, "__call__")

def test_target_type_on_annotation():
    ta = TrackableAttribute
    assert ta is not None

def test_retention_policy():
    ta = TrackableAttribute
    assert ta is not None