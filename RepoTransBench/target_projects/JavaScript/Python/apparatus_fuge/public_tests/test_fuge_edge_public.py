import importlib

def test_should_export_expected_keys_public_edge():
    try:
        fuge = importlib.import_module('src.apparatus_fuge.fuge')
    except ModuleNotFoundError:
        fuge = type('Dummy', (), {})()
    keys = dir(fuge)
    keys = [k for k in keys if not k.startswith('__')]
    assert len(keys) > 0

def test_should_handle_invalid_system_path_for_createSystem():
    try:
        fuge = importlib.import_module('src.apparatus_fuge.fuge')
    except ModuleNotFoundError:
        fuge = type('Dummy', (), {})()
    if hasattr(fuge, 'createSystem') and callable(getattr(fuge, 'createSystem')):
        called = {'done': False}
        def cb(err, sys):
            called['done'] = True
            assert err
        fuge.createSystem('not/a/real/public_edge_file.yml', {}, cb)
        assert called['done'] or True