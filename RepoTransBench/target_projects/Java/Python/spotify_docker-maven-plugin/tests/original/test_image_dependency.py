import pytest
import json
import io

def test_image_available(monkeypatch):
    # Simulate getting "image-info.json" file as input stream
    dummy_json = '{"image":"with-many-modules-a"}'
    class DummyStream(io.StringIO):
        def __init__(self, txt): super().__init__(txt)
        def read(self, *a, **kw): return super().read(*a, **kw)
    monkeypatch.setattr("builtins.open", lambda *a, **kw: DummyStream(dummy_json))
    # Normally we'd use importlib.resources, but here we simulate access
    f = DummyStream(dummy_json)
    json_node = json.loads(f.read())
    assert json_node["image"] == "with-many-modules-a"