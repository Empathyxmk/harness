import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src' / 'tools'))

import src.tools.utils as utils

def test_cities_array_and_contains_beijing():
    assert isinstance(utils.cities, list)
    assert 'beijing' in utils.cities

def test_getCityGeoJSON_path_for_wuhan():
    file_name = utils.getCityGeoJSON('wuhan')
    assert file_name.endswith('wuhan.geojson')

def test_ROOT_DIR_and_GEOJSON_EXT_still_correct():
    assert isinstance(utils.ROOT_DIR, str)
    assert utils.GEOJSON_EXT.startswith('.geo')