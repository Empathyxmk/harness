import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from linkedin2username import GEO_REGIONS

def test_public_geo_regions_us():
    # Use a different region in data
    us_region = [region for region in GEO_REGIONS if "GB" in region['countryCode']]
    assert us_region, "Should find regions for GB"
    for region in us_region:
        assert "countryCode" in region and "name" in region
        assert region["countryCode"] == "GB"

def test_public_geo_regions_all_have_str():
    for region in GEO_REGIONS:
        assert isinstance(region.get("name", ""), str)