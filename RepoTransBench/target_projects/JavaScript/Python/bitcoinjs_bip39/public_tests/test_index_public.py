import os

def test_typescript_wordlists_source_index_public():
    italian_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_src', 'wordlists', 'italian.json'))
    assert os.path.exists(italian_json_path)

def test_wordlists_type_definitions_public():
    dts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'types', 'wordlists.d.ts'))
    assert os.path.exists(dts_path)