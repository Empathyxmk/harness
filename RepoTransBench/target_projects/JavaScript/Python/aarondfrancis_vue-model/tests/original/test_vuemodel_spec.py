import pytest

import copy

class FakeVue:
    """Very minimal stub for Vue for test"""
    def __init__(self):
        self.models = type('models', (), {"register": None})()

@pytest.fixture(autouse=True)
def use_clean_vuemodel(monkeypatch):
    # Run before each test, reset registry and spy
    from src.VueModel import VueModel
    VueModel.registry = {}
    try:
        VueModel.register.call_records = []
    except Exception:
        pass
    yield

def spy_on_fn(obj, fn_name):
    # Monkeypatch record calls
    orig_fn = getattr(obj, fn_name)
    call_records = []
    def wrapper(*args, **kwargs):
        call_records.append((args, kwargs))
        return orig_fn(*args, **kwargs)
    wrapper.call_records = call_records
    setattr(obj, fn_name, wrapper)
    return wrapper

def test_register_models():
    from src.VueModel import VueModel
    spy_on_fn(VueModel, 'register')
    fake_vue = FakeVue()
    def fake_vue_use(plugin, *args):
        plugin.install(fake_vue, *args)
    base_route = '/test'
    fake_vue_use(VueModel)
    setattr(fake_vue.models, 'register', VueModel.register)
    fake_vue.models.register('users', {"http": {"baseRoute": base_route}})
    # Now check
    assert hasattr(VueModel.register, "call_records")
    assert len(VueModel.register.call_records) == 1
    assert 'users' in VueModel.registry
    assert VueModel.registry['users']['http']['baseRoute'] == base_route

def test_register_models_when_vue_use_with_options():
    from src.VueModel import VueModel
    spy_on_fn(VueModel, 'register')
    fake_vue = FakeVue()
    def fake_vue_use(plugin, *args):
        plugin.install(fake_vue, *args)
    base_route = '/test2'
    options = {"users": {"http": {"baseRoute": base_route}}}
    fake_vue_use(VueModel, options)
    setattr(fake_vue.models, 'register', VueModel.register)
    assert len(VueModel.register.call_records) == 1
    assert 'users' in VueModel.registry
    assert VueModel.registry['users']['http']['baseRoute'] == base_route