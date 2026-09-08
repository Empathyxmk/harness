import os

def test_typescript_entrypoint_index_exists():
    ts_index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_src', 'index.ts'))
    assert os.path.exists(ts_index_path)

def test_type_definitions_exist():
    dts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'types', 'index.d.ts'))
    assert os.path.exists(dts_path)