import pytest

import ansibleinventorygrapher.__init__ as aig

class DummyVault:
    def __init__(self, ciphertext=None):
        self._ciphertext = ciphertext

class DummyGroup:
    def __init__(self, name, parent_groups=None, ancestors=None):
        self.name = name
        self.parent_groups = parent_groups or []
        self._ancestors = ancestors or []
    def get_ancestors(self):
        return self._ancestors

class DummyHost:
    def __init__(self, name, groups=None, host_vars=None):
        self.name = name
        self.groups = groups or []
        self._host_vars = host_vars or {}
    def get_groups(self):
        return self.groups

class DummyInventoryManager:
    def __init__(self, group_vars=None, host_vars=None):
        self.group_vars = group_vars or {}
        self.host_vars = host_vars or {}
        class Inv:
            def get_group_vars(inv, group):
                return self.group_vars.get(group, {})
            def get_host_vars(inv, host):
                return self.host_vars.get(host, {})
        self.inventory = Inv()

def test_edge_public_repr_eq_hash():
    e1 = aig.Edge("x", "y")
    e2 = aig.Edge("x", "y")
    e3 = aig.Edge("x", "z")
    assert repr(e1) == "x -> y"
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) == hash(e2)
    assert hash(e1) != hash(e3)

def test_node_public_repr_eq_hash():
    n1 = aig.Node("nn")
    n2 = aig.Node("nn")
    n3 = aig.Node("yy")
    assert repr(n1) == "nn"
    assert n1 == n2
    assert n1 != n3
    assert hash(n1) == hash(n2)
    assert hash(n1) != hash(n3)

def test_parent_graphs_public_simple(monkeypatch):
    aig._parents.clear()
    # G10 parent of G20, G20 parent of child2
    g10 = DummyGroup("G10", parent_groups=[])
    g20 = DummyGroup("G20", parent_groups=[g10])
    child2 = DummyGroup("CHILD2", parent_groups=[g20])
    groups = [g10, g20]
    results = aig.parent_graphs(child2, groups)
    assert all(isinstance(e, aig.Edge) for e in results)
    assert any(e.source == "G10" or e.source == "G20" for e in results)

def test_remove_inherited_and_overridden_vars_public_nomatch(monkeypatch):
    aig._vars = {}
    group = 'g_public'
    vars = {"key9": "value2", "key8": DummyVault(ciphertext="lmn")}
    mgr = DummyInventoryManager(group_vars={group: {"key1": "otherval"}})
    aig.remove_inherited_and_overridden_vars(vars.copy(), group, mgr)

def test_remove_inherited_and_overridden_vars_public_vault(monkeypatch):
    aig._vars = {}
    group = 'g_public'
    k = "topsecret"
    v1 = DummyVault(ciphertext="shh")
    v2 = DummyVault(ciphertext="shh")
    vars = {k: v2}
    mgr = DummyInventoryManager(group_vars={group: {k: v1}})
    aig.remove_inherited_and_overridden_vars(vars, group, mgr)
    v3 = DummyVault(ciphertext="totallydifferent")
    vars2 = {k: v3}
    aig.remove_inherited_and_overridden_vars(vars2, group, mgr)

def test_remove_inherited_and_overridden_vars_public_mixed(monkeypatch):
    aig._vars = {}
    group = 'group_public'
    k = "vaultish"
    v1 = DummyVault(ciphertext="1xyz")
    v2 = "no_secret"
    vars = {k: v1}
    mgr = DummyInventoryManager(group_vars={group: {k: v2}})
    aig.remove_inherited_and_overridden_vars(vars, group, mgr)

def test_remove_inherited_and_overridden_group_vars_public(monkeypatch):
    aig._vars = {}
    group = DummyGroup("groupx")
    ancestor1 = DummyGroup("ancestor99")
    group.get_ancestors = lambda: [ancestor1]
    mgr = DummyInventoryManager(group_vars={"groupx": {"alpha": 19}, ancestor1: {"beta": 23}})
    aig._vars["groupx"] = {"alpha": 19}
    aig.remove_inherited_and_overridden_group_vars(group, mgr)

def test_tidy_all_the_variables_public(monkeypatch):
    aig._vars = None
    host = DummyHost("host_public")
    mgr = DummyInventoryManager(host_vars={host: {"varA": "b"}}, group_vars={})
    # Host with no groups
    d = aig.tidy_all_the_variables(host, mgr)
    assert host in d
    # Host with groups
    g2 = DummyGroup("g2z")
    host.groups = [g2]
    mgr.group_vars = {g2: {"sample": 505}}
    aig.tidy_all_the_variables(host, mgr)

def test_generate_graph_for_host_public(monkeypatch):
    host = DummyHost("hh2")
    g = DummyGroup("gg2")
    host.groups = [g]
    mgr = DummyInventoryManager(host_vars={host: {}}, group_vars={g: {}})
    edges, nodes = aig.generate_graph_for_host(host, mgr)
    assert isinstance(edges, set)
    assert any(isinstance(e, aig.Edge) for e in edges)
    assert isinstance(nodes, set)
    assert any(isinstance(n, aig.Node) for n in nodes)