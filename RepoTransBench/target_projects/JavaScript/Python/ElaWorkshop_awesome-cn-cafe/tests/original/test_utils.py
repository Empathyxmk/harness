import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'src' / 'tools'))

import src.tools.utils as utils

def test_cities_should_be_array():
    assert isinstance(utils.cities, list)
    assert len(utils.cities) > 0

def test_getCityGeoJSON_path():
    file_name = utils.getCityGeoJSON('beijing')
    assert file_name.endswith('beijing.geojson')

def test_ROOT_DIR_and_GEOJSON_EXT_are_correct():
    assert isinstance(utils.ROOT_DIR, str)
    assert utils.GEOJSON_EXT == '.geojson'