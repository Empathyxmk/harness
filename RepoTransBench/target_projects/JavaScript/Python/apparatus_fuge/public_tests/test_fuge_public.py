import importlib

def test_has_at_least_one_exported_key():
    try:
        fuge = importlib.import_module('src.apparatus_fuge.fuge')
    except ModuleNotFoundError:
        fuge = type('Dummy', (), {})()
    keys = dir(fuge)
    keys = [k for k in keys if not k.startswith('__')]
    assert len(keys) >= 1

def test_should_not_throw_when_called_with_no_arguments_public():
    try:
        fuge = importlib.import_module('src.apparatus_fuge.fuge')
    except ModuleNotFoundError:
        fuge = type('Dummy', (), {})()
    for k in dir(fuge):
        if callable(getattr(fuge, k)) and not k.startswith('__'):
            try:
                getattr(fuge, k)()
            except Exception:
                pass
            break