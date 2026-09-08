import pytest

class DangerZone:
    def __init__(self, code):
        self.code = code
        self.is_clean = False

    def clean(self):
        self.is_clean = True

@pytest.fixture
def danger_zone_public():
    dz = DangerZone("DZ-909")
    yield dz
    dz.clean()

def test_cleanup_action_public(danger_zone_public):
    # Make sure object is not clean before
    assert not danger_zone_public.is_clean

def test_cleanup_finalize_public(danger_zone_public):
    danger_zone_public.clean()
    assert danger_zone_public.is_clean