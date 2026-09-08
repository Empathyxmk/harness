import pytest
import types

import ansibleinventorygrapher.inventory as ai

def test_no_vault_secret_found():
    ex = ai.NoVaultSecretFound()
    assert isinstance(ex, ai.NoVaultSecretFound)

class FakeCLI:
    called = False
    @staticmethod
    def setup_vault_secrets(loader, vault_ids, vault_password_files, ask_vault_pass):
        FakeCLI.called = True

class DummyLoader:
    pass

class DummyIM:
    def __init__(self):
        self._sources = ["/tmp"]
        self._loader = DummyLoader()
    def groups(self):
        return {}

class DummyGroup:
    pass

class DummyPlugin:
    # Simulate a plugin returning vars for entities
    def __init__(self):
        self.called = False
    def get_vars(self, loader, path, entities):
        self.called = True
        return {"foo": "bar"}

class DummyPluginHost(DummyPlugin):
    def get_host_vars(self, name):
        return {"x": 1}
    def get_group_vars(self, name):
        return {"y": 2}

class DummyHost:
    def __init__(self, name):
        self.name = name

def test_ansibleinventory_init(monkeypatch):
    monkeypatch.setattr("ansible.cli.CLI", FakeCLI)
    monkeypatch.setattr("ansible.inventory.manager.InventoryManager", lambda loader, sources: DummyIM())
    monkeypatch.setattr("ansible.vars.manager.VariableManager", lambda loader: types.SimpleNamespace(set_inventory=lambda x: None))
    ai_inst = ai.AnsibleInventory("invfile", True, [], [])
    assert hasattr(ai_inst, "inventory")
    assert FakeCLI.called

def test_plugins_inventory(monkeypatch):
    # Fix: Ensure _inventory is present with _sources
    dummy_im = types.SimpleNamespace(_inventory=DummyIM(), _sources=["/tmp"], _loader=DummyLoader())
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.variable_manager = dummy_im
    vi._get_plugin_vars = lambda plugin, path, entities: {"f": 1} if hasattr(plugin, "get_vars") else {}
    monkeypatch.setattr("os.path.isdir", lambda d: True)
    monkeypatch.setattr("ansible.plugins.loader.vars_loader", types.SimpleNamespace(all=lambda : [DummyPlugin()]))
    monkeypatch.setattr("ansible.utils.vars.combine_vars", lambda d1, d2: dict(list(d1.items()) + list(d2.items())))
    result = vi._plugins_inventory([DummyGroup()])
    assert isinstance(result, dict)

def test_get_plugin_vars_host(monkeypatch):
    from types import SimpleNamespace
    plugin = DummyPluginHost()
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    dummy_loader = DummyLoader()
    vi.variable_manager = SimpleNamespace(_loader=dummy_loader)
    entities = [DummyHost("h")]
    monkeypatch.setattr("ansible.inventory.host.Host", DummyHost)
    # Patch plugin.get_vars to raise AttributeError to trigger fallback logic
    class NoGetVars:
        def get_host_vars(self, name):
            return {"x": 1}
        def get_group_vars(self, name):
            return {"y": 2}
    plugin2 = NoGetVars()
    out = ai.AnsibleInventory._get_plugin_vars(vi, plugin2, "/", entities)
    assert "x" in out

def test_get_group_vars(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi._plugins_inventory = lambda e: {"some": "groupvar"}
    assert vi.get_group_vars("g") == {"some": "groupvar"}

def test_get_host_vars_magic(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    class DummyVM:
        def get_vars(self, host, include_hostvars):
            return {
                "keep": 1,
                "omit": "omit",
                "ansible_version": "xxx"
            }
    vi.variable_manager = DummyVM()
    import ansibleinventorygrapher.inventory as ai2
    res = vi.get_host_vars("h")
    assert "omit" not in res
    assert "ansible_version" not in res
    assert "keep" in res

def test_get_host_vars_ansible_error(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    class DummyVM:
        def get_vars(self, **kwargs):
            import ansible
            class DummyError(Exception): pass
            raise ai.ansible.errors.AnsibleParserError("fail")
    vi.variable_manager = DummyVM()
    # Patch ansible.errors.AnsibleParserError to Exception
    ai.ansible.errors.AnsibleParserError = Exception
    with pytest.raises(ai.NoVaultSecretFound):
        vi.get_host_vars("h")

def test_get_group(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.inventory = types.SimpleNamespace(groups={"g": 1})
    assert vi.get_group("g") == 1

def test_get_host(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.inventory = types.SimpleNamespace(get_host=lambda h: "host1")
    assert vi.get_host("foo") == "host1"

def test_list_hosts(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.inventory = types.SimpleNamespace(list_hosts=lambda p: ["h"])
    assert vi.list_hosts("p") == ["h"]

def test_inventorymanager(monkeypatch):
    monkeypatch.setattr("ansibleinventorygrapher.inventory.AnsibleInventory", lambda *a, **k: "invobj")
    im = ai.InventoryManager("foo", vault_password_files=None, vault_ids=None)
    assert im.inventory == "invobj"

    im2 = ai.InventoryManager("foo", vault_password_files=["vp"], vault_ids=["vid"])
    assert im2.inventory == "invobj"