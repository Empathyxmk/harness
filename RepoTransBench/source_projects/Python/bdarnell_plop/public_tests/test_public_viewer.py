import pytest
import tempfile
import types
from tornado.options import options
import plop.viewer
from plop.viewer import IndexHandler, ViewHandler, ViewFlatHandler, DataHandler, profile_to_json

class DummyNodeP:
    def __init__(self, id, attr='y', calls=2):
        self.id = id
        self.attrs = {"attr": attr}
        self.weights = {"calls": calls}
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id == other.id

class DummyStackP:
    def __init__(self, nodes, calls=2):
        self.nodes = nodes
        self.weights = {"calls": calls}

class DummyEdgeP:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.weights = {"bar": 3}

class DummyCallGraphP:
    def __init__(self):
        self.stacks = [
            DummyStackP([DummyNodeP(11, "aa", 13)], 13),
            DummyStackP([DummyNodeP(22, "bb", 17)], 17),
        ]
        self.edges = {
            1: DummyEdgeP(DummyNodeP(11, "aa", 13), DummyNodeP(22, "bb", 17)),
            2: DummyEdgeP(DummyNodeP(22, "bb", 17), DummyNodeP(11, "aa", 13)),
        }
    @staticmethod
    def load(filename):
        return DummyCallGraphP()

def patch_callgraph_load_p(monkeypatch):
    monkeypatch.setattr(plop.viewer.CallGraph, "load", DummyCallGraphP.load)

@pytest.fixture
def temp_profile_dir_p(tmp_path):
    d = tmp_path
    filenames = []
    for i in range(3):
        f = d / f"sample_{i}.prof"
        f.write_text("data")
        filenames.append(f.name)
    yield str(d), filenames

def test_public_index_handler_sorted(monkeypatch, temp_profile_dir_p):
    temp_dir, filenames = temp_profile_dir_p
    monkeypatch.setattr(options, "datadir", temp_dir)
    class DummyHandler(IndexHandler):
        def __init__(self):
            pass
        def render(self, tpl, files):
            self.files_rendered = files
    handler = DummyHandler()
    handler.get()
    assert sorted(handler.files_rendered) == sorted(filenames)

def test_public_view_handler(monkeypatch):
    class DummyHandler(ViewHandler):
        def __init__(self):
            self.arguments = {"filename": "alpha.prof"}
        def get_argument(self, name):
            return self.arguments[name]
        def render(self, tpl, filename):
            self.rendered = (tpl, filename)
    handler = DummyHandler()
    handler.get()
    assert handler.rendered == ('force.html', 'alpha.prof')

def test_public_viewflat_handler(monkeypatch):
    patch_callgraph_load_p(monkeypatch)
    class DummyHandler(ViewFlatHandler):
        def __init__(self):
            self.arguments = {"filename": "beta.prof"}
            self._settings = {"static_path": "/testpath"}
            self.rendered = None
        def get_argument(self, name):
            return self.arguments[name]
        def render(self, tpl, data=None):
            self.rendered = (tpl, data)
        @property
        def settings(self):
            return self._settings
        @settings.setter
        def settings(self, value):
            self._settings = value
    h = DummyHandler()
    h.get()
    tpl, data = h.rendered
    assert tpl == 'force-flat.html'
    assert 'nodes' in data and 'edges' in data and 'stacks' in data

def test_public_viewflat_embed_file(tmp_path):
    class Dummy(ViewFlatHandler):
        def __init__(self):
            self._settings = {"static_path": str(tmp_path)}
        @property
        def settings(self):
            return self._settings
        @settings.setter
        def settings(self, value):
            self._settings = value
    h = Dummy()
    temp_file = tmp_path / "b.txt"
    temp_file.write_text("goodbye")
    result = h.embed_file("b.txt")
    assert result == "goodbye"

def test_public_data_handler(monkeypatch):
    patch_callgraph_load_p(monkeypatch)
    class DummyHandler(DataHandler):
        def __init__(self):
            self.arguments = {"filename": "gamma.prof"}
        def get_argument(self, name):
            return self.arguments[name]
        def write(self, val):
            self.written = val
    h = DummyHandler()
    h.get()
    assert 'nodes' in h.written and 'edges' in h.written and 'stacks' in h.written

def test_public_profile_to_json(monkeypatch, tmp_path):
    patch_callgraph_load_p(monkeypatch)
    datadir = tmp_path
    monkeypatch.setattr(options, "datadir", str(datadir))
    profile = tmp_path / "run.prof"
    profile.write_text("dummy data")
    result = profile_to_json("run.prof")
    assert isinstance(result, dict)
    assert "nodes" in result and "edges" in result and "stacks" in result

def test_public_profile_to_json_path_traversal(monkeypatch, tmp_path):
    patch_callgraph_load_p(monkeypatch)
    datadir = tmp_path
    monkeypatch.setattr(options, "datadir", str(datadir))
    with pytest.raises(AssertionError):
        profile_to_json("../../out.prof")