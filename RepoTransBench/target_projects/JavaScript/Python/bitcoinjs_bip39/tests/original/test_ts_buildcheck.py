import os

def test_tsconfig_json_file_exists():
    assert os.path.exists('tsconfig.json'), "tsconfig.json missing"