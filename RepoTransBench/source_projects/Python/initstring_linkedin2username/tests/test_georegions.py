import pytest
from linkedin2username import GEO_REGIONS

def test_geo_regions_us():
    assert GEO_REGIONS["us"] == "103644278"

def test_geo_regions_all_have_str():
    for code, val in GEO_REGIONS.items():
        assert isinstance(code, str)
        assert isinstance(val, str)
        assert val.isdigit()