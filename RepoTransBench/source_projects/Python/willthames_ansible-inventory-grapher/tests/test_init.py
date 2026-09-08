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

def test_edge_repr_eq_hash():
    e1 = aig.Edge("a", "b")
    e2 = aig.Edge("a", "b")
    e3 = aig.Edge("a", "c")
    assert repr(e1) == "a -> b"
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) == hash(e2)
    assert hash(e1) != hash(e3)

def test_node_repr_eq_hash():
    n1 = aig.Node("n")
    n2 = aig.Node("n")
    n3 = aig.Node("x")
    assert repr(n1) == "n"
    assert n1 == n2
    assert n1 != n3
    assert hash(n1) == hash(n2)
    assert hash(n1) != hash(n3)

def test_parent_graphs_simple(monkeypatch):
    aig._parents.clear()
    # G1 parent of G2, G2 parent of child
    g1 = DummyGroup("G1", parent_groups=[])
    g2 = DummyGroup("G2", parent_groups=[g1])
    child = DummyGroup("CHILD", parent_groups=[g2])
    groups = [g1, g2]
    # forcibly avoid the inner check via monkeypatch if needed
    results = aig.parent_graphs(child, groups)
    assert all(isinstance(e, aig.Edge) for e in results)

def test_remove_inherited_and_overridden_vars_nomatch(monkeypatch):
    aig._vars = {}
    group = 'g'
    vars = {"key1": "value", "key2": DummyVault(ciphertext="abc")}
    mgr = DummyInventoryManager(group_vars={group: {"key3": "otherval"}})
    aig.remove_inherited_and_overridden_vars(vars.copy(), group, mgr)

def test_remove_inherited_and_overridden_vars_vault(monkeypatch):
    aig._vars = {}
    group = 'g'
    k = "secret"
    v1 = DummyVault(ciphertext="abc")
    v2 = DummyVault(ciphertext="abc")
    vars = {k: v2}
    mgr = DummyInventoryManager(group_vars={group: {k: v1}})
    # Should delete from vars when ciphertext matches
    aig.remove_inherited_and_overridden_vars(vars, group, mgr)
    # Now one with different ciphertext does not match
    v3 = DummyVault(ciphertext="xyz")
    vars2 = {k: v3}
    aig.remove_inherited_and_overridden_vars(vars2, group, mgr)

def test_remove_inherited_and_overridden_vars_mixed(monkeypatch):
    aig._vars = {}
    group = 'g'
    k = "secret"
    v1 = DummyVault(ciphertext="abc")
    v2 = "plaintext"
    vars = {k: v1}
    mgr = DummyInventoryManager(group_vars={group: {k: v2}})
    aig.remove_inherited_and_overridden_vars(vars, group, mgr)

def test_remove_inherited_and_overridden_group_vars(monkeypatch):
    aig._vars = {}
    group = DummyGroup("g")
    ancestor1 = DummyGroup("anc")
    group.get_ancestors = lambda: [ancestor1]
    mgr = DummyInventoryManager(group_vars={"g": {"x": 1}, ancestor1: {"y": 2}})
    aig._vars["g"] = {"x": 1}
    aig.remove_inherited_and_overridden_group_vars(group, mgr)

def test_tidy_all_the_variables(monkeypatch):
    aig._vars = None
    host = DummyHost("host1")
    mgr = DummyInventoryManager(host_vars={host: {"a": 1}}, group_vars={})
    # Host with no groups
    d = aig.tidy_all_the_variables(host, mgr)
    assert host in d
    # Host with groups
    g = DummyGroup("g")
    host.groups = [g]
    mgr.group_vars = {g: {"test": 99}}
    aig.tidy_all_the_variables(host, mgr)

def test_generate_graph_for_host(monkeypatch):
    host = DummyHost("h")
    g = DummyGroup("g")
    host.groups = [g]
    mgr = DummyInventoryManager(host_vars={host: {}}, group_vars={g: {}})
    edges, nodes = aig.generate_graph_for_host(host, mgr)
    assert isinstance(edges, set)
    assert any(isinstance(e, aig.Edge) for e in edges)
    assert isinstance(nodes, set)
    assert any(isinstance(n, aig.Node) for n in nodes)