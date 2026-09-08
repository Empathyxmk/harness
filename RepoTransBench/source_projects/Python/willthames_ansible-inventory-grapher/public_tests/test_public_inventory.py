import pytest
import types

import ansibleinventorygrapher.inventory as ai

def test_no_vault_secret_found_public():
    ex = ai.NoVaultSecretFound()
    assert isinstance(ex, ai.NoVaultSecretFound)

class FakeCLIPublic:
    called = False
    @staticmethod
    def setup_vault_secrets(loader, vault_ids, vault_password_files, ask_vault_pass):
        FakeCLIPublic.called = True

class DummyLoaderPublic:
    pass

class DummyIMPublic:
    def __init__(self):
        self._sources = ["/var/xyz"]
        self._loader = DummyLoaderPublic()
    def groups(self):
        return {}

class DummyGroupPublic:
    pass

class DummyPluginPublic:
    def __init__(self):
        self.called = False
    def get_vars(self, loader, path, entities):
        self.called = True
        return {"baz": "qux"}

class DummyPluginHostPublic(DummyPluginPublic):
    def get_host_vars(self, name):
        return {"a": 82}
    def get_group_vars(self, name):
        return {"b": 99}

class DummyHostPublic:
    def __init__(self, name):
        self.name = name

def test_ansibleinventory_public_init(monkeypatch):
    monkeypatch.setattr("ansible.cli.CLI", FakeCLIPublic)
    monkeypatch.setattr("ansible.inventory.manager.InventoryManager", lambda loader, sources: DummyIMPublic())
    monkeypatch.setattr("ansible.vars.manager.VariableManager", lambda loader: types.SimpleNamespace(set_inventory=lambda x: None))
    ai_inst = ai.AnsibleInventory("invfile2", True, [], [])
    assert hasattr(ai_inst, "inventory")
    assert FakeCLIPublic.called

def test_plugins_inventory_public(monkeypatch):
    dummy_im = types.SimpleNamespace(_inventory=DummyIMPublic(), _sources=["/var/xyz"], _loader=DummyLoaderPublic())
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.variable_manager = dummy_im
    vi._get_plugin_vars = lambda plugin, path, entities: {"p": 99} if hasattr(plugin, "get_vars") else {}
    monkeypatch.setattr("os.path.isdir", lambda d: True)
    monkeypatch.setattr("ansible.plugins.loader.vars_loader", types.SimpleNamespace(all=lambda : [DummyPluginPublic()]))
    monkeypatch.setattr("ansible.utils.vars.combine_vars", lambda d1, d2: dict(list(d1.items()) + list(d2.items())))
    result = vi._plugins_inventory([DummyGroupPublic()])
    assert isinstance(result, dict)

def test_get_plugin_vars_host_public(monkeypatch):
    from types import SimpleNamespace
    plugin = DummyPluginHostPublic()
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    dummy_loader = DummyLoaderPublic()
    vi.variable_manager = SimpleNamespace(_loader=dummy_loader)
    entities = [DummyHostPublic("hh")]
    monkeypatch.setattr("ansible.inventory.host.Host", DummyHostPublic)
    class NoGetVarsPublic:
        def get_host_vars(self, name):
            return {"a": 99}
        def get_group_vars(self, name):
            return {"b": 88}
    plugin2 = NoGetVarsPublic()
    out = ai.AnsibleInventory._get_plugin_vars(vi, plugin2, "/", entities)
    assert "a" in out

def test_get_group_vars_public(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi._plugins_inventory = lambda e: {"other": "groupvar2"}
    assert vi.get_group_vars("gx") == {"other": "groupvar2"}

def test_get_host_vars_magic_public(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    class DummyVM2:
        def get_vars(self, host, include_hostvars):
            return {
                "persist": 42,
                "omit": "remove",
                "ansible_version": "yyy"
            }
    vi.variable_manager = DummyVM2()
    res = vi.get_host_vars("hh")
    assert "omit" not in res
    assert "ansible_version" not in res
    assert "persist" in res

def test_get_host_vars_ansible_error_public(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    class DummyVM3:
        def get_vars(self, **kwargs):
            import ansible
            class DummyError(Exception): pass
            raise ai.ansible.errors.AnsibleParserError("fail!")
    vi.variable_manager = DummyVM3()
    ai.ansible.errors.AnsibleParserError = Exception
    with pytest.raises(ai.NoVaultSecretFound):
        vi.get_host_vars("hh")

def test_get_group_public(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.inventory = types.SimpleNamespace(groups={"gx": 501})
    assert vi.get_group("gx") == 501

def test_get_host_public(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.inventory = types.SimpleNamespace(get_host=lambda h: "hostX")
    assert vi.get_host("baz") == "hostX"

def test_list_hosts_public(monkeypatch):
    vi = ai.AnsibleInventory.__new__(ai.AnsibleInventory)
    vi.inventory = types.SimpleNamespace(list_hosts=lambda p: ["h2"])
    assert vi.list_hosts("p2") == ["h2"]

def test_inventorymanager_public(monkeypatch):
    monkeypatch.setattr("ansibleinventorygrapher.inventory.AnsibleInventory", lambda *a, **k: "public_invobj")
    im = ai.InventoryManager("wtf", vault_password_files=None, vault_ids=None)
    assert im.inventory == "public_invobj"
    im2 = ai.InventoryManager("wtf", vault_password_files=["vpX"], vault_ids=["vidX"])
    assert im2.inventory == "public_invobj"