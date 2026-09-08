import os

def test_tslint_json_config_exists_public():
    assert os.path.exists('tslint.json'), 'tslint.json missing'