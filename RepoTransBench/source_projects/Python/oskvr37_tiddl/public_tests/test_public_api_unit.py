import pytest
from types import SimpleNamespace
import tiddl.api as api_mod

class DummyResponsePublic:
    def __init__(self, data, status_code=201, from_cache=False):
        self._data = data
        self.status_code = status_code
        self.from_cache = from_cache
    def json(self):
        return self._data

class DummySessionPublic:
    def __init__(self):
        self.req = None
        self.headers = {}
    def get(self, url, params=None, expire_after=None):
        self.req = (url, params, expire_after)
        # Use different id for public test
        data = {"id": 321}
        return DummyResponsePublic(data)

def dummy_model_validate_public(cls, data):
    obj = SimpleNamespace(**data)
    return obj

def test_ensureLimit_warns_public(monkeypatch, caplog):
    with caplog.at_level("WARNING"):
        assert api_mod.ensureLimit(99, 10) == 10
        assert "Max limit is 10" in caplog.text
    assert api_mod.ensureLimit(8, 10) == 8

def test_TidalApi_fetch_success_public(monkeypatch):
    dummy_class = type("DummyModelPublic", (), {"model_validate": classmethod(dummy_model_validate_public)})
    api = api_mod.TidalApi("tok", "uid_pub", "country")
    api.session = DummySessionPublic()
    ret = api.fetch(dummy_class, "endpoint/42", {"bar": 10})
    assert hasattr(ret, "id")
    assert api.session.req[0].endswith("endpoint/42")

def test_TidalApi_fetch_failure_public(monkeypatch):
    dummy_class = type("DummyModelPublic", (), {"model_validate": classmethod(dummy_model_validate_public)})
    api = api_mod.TidalApi("tok", "uid_pub", "country")
    class ErrSession(DummySessionPublic):
        def get(self, *a, **k):
            return DummyResponsePublic({"status": 403, "userMessage": "Forbidden"}, status_code=403)
    api.session = ErrSession()
    with pytest.raises(api_mod.ApiError) as e:
        api.fetch(dummy_class, "endpoint/42")
    assert "Forbidden" in str(e.value)

def test_TidalApi_methods_public(monkeypatch):
    api = api_mod.TidalApi("tok", "uid_pub", "country")
    called = []
    def fake_fetch(model, endpoint, params={}, expire_after=None):
        called.append((model, endpoint, dict(params)))
        return model
    api.fetch = fake_fetch
    # Use different IDs
    result = api.getAlbum(77)
    assert result == api_mod.Album
    result = api.getAlbumItems(77, limit=3, offset=2)
    assert result == api_mod.AlbumItems
    result = api.getAlbumItemsCredits(2, limit=1)
    assert result == api_mod.AlbumItemsCredits
    result = api.getArtist(99)
    assert result == api_mod.Artist
    result = api.getArtistAlbums(44)
    assert result == api_mod.ArtistAlbumsItems