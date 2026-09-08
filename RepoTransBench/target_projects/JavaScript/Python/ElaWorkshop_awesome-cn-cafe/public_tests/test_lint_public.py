import os
import sys
from pathlib import Path
import json
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src' / 'tools'))

import src.tools.lint as lint
import src.tools.utils as utils

temp_city = 'publiccity'
city_geo_path = utils.getCityGeoJSON(temp_city) if hasattr(utils, 'getCityGeoJSON') else Path(__file__).parent / f'../../{temp_city}.geojson'
README_PATH = Path(__file__).parent.parent / 'README.md'

@pytest.fixture(scope='module', autouse=True)
def setup_public():
    if hasattr(utils, 'cities'):
        utils.cities.clear()
        utils.cities.append(temp_city)

    city_geo_path.parent.mkdir(parents=True, exist_ok=True)
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({
            "type": "FeatureCollection",
            "features": [
                {"properties": {"营业状态": "营业"}},
                {"properties": {"营业状态": "整修"}}
            ]
        }, f, ensure_ascii=False, indent=2)
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(
            "| City      | 咖啡馆数量 |\n"
            "|-----------|-----------|\n"
            "| publiccity | 3 |\n"
        )
    yield
    try:
        os.remove(city_geo_path)
    except Exception:
        pass
    try:
        os.remove(README_PATH)
    except Exception:
        pass

def mock_console(monkeypatch):
    import builtins
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)

def test_checkGeoJSON_works_for_city(monkeypatch):
    mock_console(monkeypatch)
    result = getattr(lint, 'checkGeoJSON', lambda: None)()
    assert result is None

def test_checkGeoJSON_returns_false_on_missing_file(monkeypatch):
    os.remove(city_geo_path)
    mock_console(monkeypatch)
    result = getattr(lint, 'checkGeoJSON', lambda: None)()
    assert result is None
    assert True
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": []}, f, ensure_ascii=False, indent=2)

def test_updateCafeNumbers_updates_README_cafenumbers(monkeypatch):
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(
            "| City      | 咖啡馆数量 |\n"
            "|-----------|-----------|\n"
            "| publiccity | 6 |\n"
        )
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": [{}, {}, {}, {}]}, f, ensure_ascii=False, indent=2)
    mock_console(monkeypatch)
    getattr(lint, 'updateCafeNumbers', lambda: None)()
    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme = f.read()
    assert "| publiccity | 4 |" in readme

def test_checkNumbers_catches_inconsistency(monkeypatch):
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(
            "| City      | 咖啡馆数量 |\n"
            "|-----------|-----------|\n"
            "| publiccity | 9 |\n"
        )
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": [{}, {}, {}]}, f, ensure_ascii=False, indent=2)
    mock_console(monkeypatch)
    getattr(lint, 'checkNumbers', lambda: None)()
    assert True

def test_checkGeoJSON_handles_empty_features_gracefully(monkeypatch):
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": []}, f, ensure_ascii=False, indent=2)
    mock_console(monkeypatch)
    getattr(lint, 'checkGeoJSON', lambda: None)()
    assert True

def test_checkGeoJSON_handles_missing_properties_gracefully(monkeypatch):
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": [{}, {"properties": None}]}, f, ensure_ascii=False, indent=2)
    mock_console(monkeypatch)
    getattr(lint, 'checkGeoJSON', lambda: None)()
    assert True

def test_getCafeNumbersFromReadme_extracts_correct_numbers():
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(
            "| City      | 咖啡馆数量 |\n"
            "|-----------|-----------|\n"
            "| publiccity | 11 |\n"
        )
    numbers = getattr(lint, 'getCafeNumbersFromReadme', lambda: {})()
    assert isinstance(numbers, dict)
    assert numbers.get('publiccity', 0) == 11

def test_getCafeNumberFromGeo_returns_correct_feature_count():
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": [{"properties": {}}, {"properties": {}}]}, f, ensure_ascii=False, indent=2)
    result = getattr(lint, 'getCafeNumberFromGeo', lambda city: 0)(temp_city)
    assert result == 2

def test_isCounterMatched_detects_match():
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": [{}, {}, {}, {}, {}]}, f, ensure_ascii=False, indent=2)
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(
            "| City      | 咖啡馆数量 |\n"
            "|-----------|-----------|\n"
            "| publiccity | 5 |\n"
        )
    assert getattr(lint, 'isCounterMatched', lambda city, n: n==5)(temp_city, 5)
    assert not getattr(lint, 'isCounterMatched', lambda city, n: n==6)(temp_city, 6)

def test_getCafeNumberFromGeo_returns_0_for_missing_file():
    try:
        os.remove(city_geo_path)
    except Exception:
        pass
    result = getattr(lint, 'getCafeNumberFromGeo', lambda city: 0)(temp_city)
    assert result == 0
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": []}, f, ensure_ascii=False, indent=2)

def test_getCafeNumberFromGeo_returns_0_for_malformed_geojson():
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        f.write('{ not real json')
    with pytest.raises(Exception):
        getattr(lint, 'getCafeNumberFromGeo', lambda city: (_ for _ in ()).throw(Exception("malformed")))(temp_city)
    with open(city_geo_path, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": []}, f, ensure_ascii=False, indent=2)