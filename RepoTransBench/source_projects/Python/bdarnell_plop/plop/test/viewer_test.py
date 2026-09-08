import os
import tempfile
import shutil
import types
import pytest

import tornado.web
from tornado.options import options
import six

import plop.viewer
from plop.viewer import IndexHandler, ViewHandler, ViewFlatHandler, DataHandler, profile_to_json

# Dummy CallGraph and stack for mocking
class DummyNode:
    def __init__(self, id, attr='x', calls=1):
        self.id = id
        self.attrs = {"attr": attr}
        self.weights = {"calls": calls}
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id == other.id

class DummyStack:
    def __init__(self, nodes, calls=1):
        self.nodes = nodes
        self.weights = {"calls": calls}

class DummyEdge:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.weights = {"foo": 1}

class DummyCallGraph:
    def __init__(self):
        # 3 nodes and 2 edges
        self.stacks = [
            DummyStack([DummyNode(1, "a", 10)], 10),
            DummyStack([DummyNode(2, "b", 20)], 20),
        ]
        self.edges = {
            1: DummyEdge(DummyNode(1, "a", 10), DummyNode(2, "b", 20)),
            2: DummyEdge(DummyNode(2, "b", 20), DummyNode(1, "a", 10)),
        }
    @staticmethod
    def load(filename):
        return DummyCallGraph()

def patch_callgraph_load(monkeypatch):
    monkeypatch.setattr(plop.viewer.CallGraph, "load", DummyCallGraph.load)

@pytest.fixture
def temp_profile_dir(tmp_path):
    # Create a temp dir with some files to act as profiles.
    d = tmp_path
    filenames = []
    for i in range(2):
        f = d / f"profile_{i}.prof"
        f.write_text("dummy")
        filenames.append(f.name)
    yield str(d), filenames

def test_index_handler_sorted(monkeypatch, temp_profile_dir):
    temp_dir, filenames = temp_profile_dir
    monkeypatch.setattr(options, "datadir", temp_dir)
    
    class DummyHandler(IndexHandler):
        def __init__(self):
            pass
        def render(self, tpl, files):
            self.files_rendered = files
    
    handler = DummyHandler()
    handler.get()
    assert sorted(handler.files_rendered) == sorted(filenames)

def test_view_handler(monkeypatch):
    class DummyHandler(ViewHandler):
        def __init__(self):
            self.arguments = {"filename": "file1.prof"}
        def get_argument(self, name):
            return self.arguments[name]
        def render(self, tpl, filename):
            self.rendered = (tpl, filename)
    handler = DummyHandler()
    handler.get()
    assert handler.rendered == ('force.html', 'file1.prof')

def test_viewflat_handler(monkeypatch):
    patch_callgraph_load(monkeypatch)
    # Patch settings property to allow assignment
    class DummyHandler(ViewFlatHandler):
        def __init__(self):
            self.arguments = {"filename": "f.prof"}
            self._settings = {"static_path": "/tmp"}
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

def test_viewflat_embed_file(tmp_path):
    # Patch settings property to allow assignment
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
    temp_file = tmp_path / "a.txt"
    temp_file.write_text("hello world")
    result = h.embed_file("a.txt")
    assert result == "hello world"

def test_data_handler(monkeypatch):
    patch_callgraph_load(monkeypatch)
    class DummyHandler(DataHandler):
        def __init__(self):
            self.arguments = {"filename": "f.prof"}
        def get_argument(self, name):
            return self.arguments[name]
        def write(self, val):
            self.written = val
    h = DummyHandler()
    h.get()
    assert 'nodes' in h.written and 'edges' in h.written and 'stacks' in h.written

def test_profile_to_json(monkeypatch, tmp_path):
    patch_callgraph_load(monkeypatch)
    datadir = tmp_path
    monkeypatch.setattr(options, "datadir", str(datadir))
    profile = tmp_path / "prof.prof"
    profile.write_text("dummy")
    result = profile_to_json("prof.prof")
    assert isinstance(result, dict)
    assert "nodes" in result and "edges" in result and "stacks" in result

def test_profile_to_json_path_traversal(monkeypatch, tmp_path):
    patch_callgraph_load(monkeypatch)
    datadir = tmp_path
    monkeypatch.setattr(options, "datadir", str(datadir))
    # Should raise assertion (path traversal)
    with pytest.raises(AssertionError):
        profile_to_json("../foo.prof")