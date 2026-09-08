import pytest

import copy

class FakeVue:
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
    orig_fn = getattr(obj, fn_name)
    call_records = []
    def wrapper(*args, **kwargs):
        call_records.append((args, kwargs))
        return orig_fn(*args, **kwargs)
    wrapper.call_records = call_records
    setattr(obj, fn_name, wrapper)
    return wrapper

def test_registers_models_with_another_dataset():
    from src.VueModel import VueModel
    spy_on_fn(VueModel, 'register')
    fake_vue = FakeVue()
    def fake_vue_use(plugin, *args):
        plugin.install(fake_vue, *args)
    base_route = '/mywidgets'
    fake_vue_use(VueModel)
    setattr(fake_vue.models, "register", VueModel.register)
    fake_vue.models.register('foo', {"http": {"baseRoute": base_route}})
    assert hasattr(VueModel.register, "call_records")
    assert len(VueModel.register.call_records) == 1
    assert 'foo' in VueModel.registry
    assert VueModel.registry['foo']['http']['baseRoute'] == base_route

def test_registers_models_with_vue_use_other_input():
    from src.VueModel import VueModel
    spy_on_fn(VueModel, 'register')
    fake_vue = FakeVue()
    def fake_vue_use(plugin, *args):
        plugin.install(fake_vue, *args)
    base_route = '/barwidgets'
    options = {'qux': {'http': {'baseRoute': base_route}}}
    fake_vue_use(VueModel, options)
    setattr(fake_vue.models, "register", VueModel.register)
    assert len(VueModel.register.call_records) == 1
    assert 'qux' in VueModel.registry
    assert VueModel.registry['qux']['http']['baseRoute'] == base_route