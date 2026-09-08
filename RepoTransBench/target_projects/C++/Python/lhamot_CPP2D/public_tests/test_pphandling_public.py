import pytest

class CPP2DPPHandling:
    pass

def test_CPP2DPPHandling_type_public():
    can_reference = False
    can_reference = getattr(CPP2DPPHandling, '__name__', None) is not None
    assert can_reference