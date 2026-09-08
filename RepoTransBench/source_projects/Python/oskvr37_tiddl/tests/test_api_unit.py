import pytest
from types import SimpleNamespace
import tiddl.api as api_mod

class DummyResponse:
    def __init__(self, data, status_code=200, from_cache=False):
        self._data = data
        self.status_code = status_code
        self.from_cache = from_cache
    def json(self):
        return self._data

class DummySession:
    def __init__(self):
        self.req = None
        self.headers = {}
    def get(self, url, params=None, expire_after=None):
        self.req = (url, params, expire_after)
        # minimal fields for BaseModel model_validate
        data = {"id": 123}
        return DummyResponse(data)

def dummy_model_validate(cls, data):
    # for all dummy BaseModel
    obj = SimpleNamespace(**data)
    return obj

def test_ensureLimit_warns(monkeypatch, caplog):
    with caplog.at_level("WARNING"):
        assert api_mod.ensureLimit(111, 5) == 5
        assert "Max limit is 5" in caplog.text
    assert api_mod.ensureLimit(3, 5) == 3

def test_TidalApi_fetch_success(monkeypatch):
    dummy_class = type("DummyModel", (), {"model_validate": classmethod(dummy_model_validate)})
    api = api_mod.TidalApi("token", "uid", "cc")
    api.session = DummySession()
    ret = api.fetch(dummy_class, "endpoint/1", {"foo": 5})
    assert hasattr(ret, "id")
    assert api.session.req[0].endswith("endpoint/1")

def test_TidalApi_fetch_failure(monkeypatch):
    dummy_class = type("DummyModel", (), {"model_validate": classmethod(dummy_model_validate)})
    api = api_mod.TidalApi("token", "uid", "cc")
    class ErrSession(DummySession):
        def get(self, *a, **k):
            return DummyResponse({"status": 401, "userMessage": "Auth fail"}, status_code=401)
    api.session = ErrSession()
    with pytest.raises(api_mod.ApiError) as e:
        api.fetch(dummy_class, "endpoint/1")
    assert "Auth fail" in str(e.value)

def test_TidalApi_methods(monkeypatch):
    # Patch fetch to record calls
    api = api_mod.TidalApi("token", "uid", "cc")
    called = []
    def fake_fetch(model, endpoint, params={}, expire_after=None):
        called.append((model, endpoint, dict(params)))
        return model
    api.fetch = fake_fetch
    # Should call fetch with proper endpoints
    result = api.getAlbum(55)
    assert result == api_mod.Album
    result = api.getAlbumItems(55, limit=5, offset=1)
    assert result == api_mod.AlbumItems
    result = api.getAlbumItemsCredits(5, limit=2)
    assert result == api_mod.AlbumItemsCredits
    result = api.getArtist(4)
    assert result == api_mod.Artist
    result = api.getArtistAlbums(5)
    assert result == api_mod.ArtistAlbumsItems