import os
import sys
import json
import pytest

from pathlib import Path
import types
import importlib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src' / 'tools'))

import src.tools.housekeeper as hk

@pytest.fixture(autouse=True)
def public_utils(monkeypatch, tmp_path):
    # Mocking for utils module used in housekeeper
    class UtilsMock(types.SimpleNamespace):
        GEOJSON_EXT = '.geojson'
        ROOT_DIR = str(tmp_path)
        cities = ['publicunittestcity']
        @staticmethod
        def getCityGeoJSON(city):
            return os.path.join(str(tmp_path), f"{city}.geojson")
    sys.modules['src.tools.utils'] = UtilsMock
    sys.modules['src.tools.lint'] = types.SimpleNamespace(updateCafeNumbers=lambda: None)
    yield

def test_run_build_marker_colors_and_symbols(monkeypatch, tmp_path):
    city = 'publicunittestcity'
    geo_path = tmp_path / f'{city}.geojson'
    geo_path.write_text(
        json.dumps({
            "type": "FeatureCollection",
            "features": [
                {"properties": {"下载速度": "1.0 Mbps", "营业状态": "营业"}},
                {"properties": {"下载速度": ["6.0 Mbps", "8.0 Mbps"], "营业状态": "营业"}},
                {"properties": {"下载速度": ["20 Mbps", "30 Mbps"], "营业状态": "营业"}},
                {"properties": {"下载速度": "25 Mbps", "营业状态": "停业"}},
            ]
        }, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    output_data = []
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: output_data.append(" ".join(map(str, args))))
    importlib.reload(hk)
    with open(geo_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert len(data['features']) == 4
    marker_colors = {
        "GRAY": "#BEBEBE",
        "RED": "#C24740",
        "YELLOW": "#F3AE1A",
        "GREEN": "#50C240"
    }
    assert data['features'][0]['properties'].get('marker-color') == marker_colors["RED"]
    assert data['features'][1]['properties'].get('marker-color') == marker_colors["YELLOW"]
    assert data['features'][2]['properties'].get('marker-color') == marker_colors["GREEN"]
    assert data['features'][3]['properties'].get('marker-color') == marker_colors["GRAY"]
    for feat in data['features']:
        assert feat['properties'].get('marker-symbol') == 'cafe'
    matched = [line for line in output_data if 'publicunittestcity: Done with 4 records!' in line]
    assert matched

def test_should_throw_error_on_invalid_speed(monkeypatch, tmp_path):
    city = 'publicunittestcity'
    geo_path = tmp_path / f'{city}.geojson'
    geo_path.write_text(json.dumps({
        "type": "FeatureCollection",
        "features": [
            {"properties": {"下载速度": "oops", "营业状态": "营业"}}
        ]
    }), encoding='utf-8')
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
    with pytest.raises(Exception):
        importlib.reload(hk)