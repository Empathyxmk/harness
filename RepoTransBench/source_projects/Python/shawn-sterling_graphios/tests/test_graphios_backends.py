import graphios_backends
import pytest

def test_load_backend_invalid(monkeypatch):
    with pytest.raises(ValueError):
        graphios_backends.load_backend("doesnotexist")

def test_load_backend_file(monkeypatch):
    backend = graphios_backends.load_backend("file", "/tmp/testfile")
    assert backend.__class__.__name__ == "FileBackend"

def test_load_backend_carbon(monkeypatch):
    backend = graphios_backends.load_backend("carbon", "host", 1234)
    assert backend.__class__.__name__ == "CarbonBackend"

def test_load_backend_udp(monkeypatch):
    backend = graphios_backends.load_backend("udp", "host", 1001)
    assert backend.__class__.__name__ == "UDPSendBackend"

def test_filebackend_send_metric(tmp_path):
    metric = type(
        "FakeMetric",
        (),
        dict(host="a", service="b", metric="c", value="1", timestamp="2"),
    )()
    fpath = tmp_path / "outfile"
    back = graphios_backends.FileBackend(str(fpath))
    back.send_metric(metric)
    with open(fpath) as f:
        data = f.read()
    assert "a b c 1 2" in data

def test_carbonbackend_send_metric(monkeypatch):
    results = {}
    class DummySocket:
        def connect(self, addr): results["connect"] = addr
        def sendall(self, data): results["sendall"] = data
        def close(self): results["closed"] = True
    monkeypatch.setattr("socket.socket", lambda *a, **k: DummySocket())
    metric = type("FakeMetric", (), dict(host="h", service="s", metric="m", value=5, timestamp=18))()
    back = graphios_backends.CarbonBackend("test.host", 2003)
    back.send_metric(metric)
    assert results["connect"] == ("test.host", 2003)
    assert b"h.s.m 5 18\n" in results["sendall"]
    assert results["closed"]

def test_udpbackend_send_metric(monkeypatch):
    results = {}
    class DummySocket:
        def sendto(self, data, addr): results["sendto"] = (data, addr)
        def close(self): results["closed"] = True
    monkeypatch.setattr("socket.socket", lambda *a, **k: DummySocket())
    metric = type("FakeMetric", (), dict(host="hosty", service="svc", metric="metric", value=3, timestamp=6))()
    back = graphios_backends.UDPSendBackend("testhost", 2222)
    back.send_metric(metric)
    assert results["sendto"][1] == ("testhost", 2222)
    assert b"hosty.svc.metric 3 6" in results["sendto"][0]
    assert results["closed"]