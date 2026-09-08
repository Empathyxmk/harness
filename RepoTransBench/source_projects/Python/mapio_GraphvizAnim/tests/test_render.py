import pytest
import os
from gvanim import render

def test_render_tmp(monkeypatch, tmp_path):
    # Patch Popen and Pool for render
    class DummyPipe:
        def communicate(self, input=None):
            return (None, None)
    class DummyPopen:
        def __init__(self, *a, **k):
            self.stdout = None
        def communicate(self, input=None):
            return (None, None)
    monkeypatch.setattr(render, "Popen", lambda *a, **k: DummyPopen())
    monkeypatch.setattr(render, "cpu_count", lambda : 1)
    monkeypatch.setattr(render, "Pool", lambda processes: type("Dummy", (), {'map':map}))
    # Prepare dummy graphs
    p = tmp_path / "g0.dot"
    files = render.render(["digraph{}", "digraph{}"], str(tmp_path / "myanim"), fmt="dot", size=10)
    assert len(files) == 2
    # Files "exist" because open was real
    for file in files:
        assert os.path.exists(file)

def test_gif(monkeypatch, tmp_path):
    files = []
    for i in range(2):
        f = tmp_path / ("f%d.png" % i)
        f.write_bytes(b"test")
        files.append(str(f))
    called = []
    def dummy_call(args):
        called.append(list(args))
    monkeypatch.setattr(render, "call", dummy_call)
    render.gif(files, str(tmp_path / "anim"), delay=123, size=11)
    # call is called for each file and convert
    assert any("convert" in c for c in called)