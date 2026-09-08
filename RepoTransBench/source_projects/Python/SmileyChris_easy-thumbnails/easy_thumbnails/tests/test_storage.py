import pytest
from unittest.mock import patch, MagicMock

import easy_thumbnails.storage

def test_thumbnail_filesystem_storage_defaults(monkeypatch):
    class DummySettings:
        THUMBNAIL_MEDIA_ROOT = ''
        THUMBNAIL_MEDIA_URL = ''
    monkeypatch.setattr(easy_thumbnails.storage, 'settings', DummySettings)
    storage = easy_thumbnails.storage.ThumbnailFileSystemStorage()
    assert storage is not None

def test_thumbnail_filesystem_storage_with_custom(monkeypatch):
    class DummySettings:
        THUMBNAIL_MEDIA_ROOT = '/some/path'
        THUMBNAIL_MEDIA_URL = '/some/url/'
    monkeypatch.setattr(easy_thumbnails.storage, 'settings', DummySettings)
    storage = easy_thumbnails.storage.ThumbnailFileSystemStorage()
    assert storage.location == '/some/path'
    assert storage.base_url == '/some/url/'

def test_get_storage_returns_from_storages(monkeypatch):
    dummy_storage = object()
    # patch django.core.files.storage.storages dict
    with patch('django.core.files.storage.storages', {'aliasname': dummy_storage}):
        class DummySettings:
            THUMBNAIL_DEFAULT_STORAGE_ALIAS = 'aliasname'
        monkeypatch.setattr(easy_thumbnails.storage, 'settings', DummySettings)
        result = easy_thumbnails.storage.get_storage()
        assert result is dummy_storage

def test_get_storage_raises_when_alias_missing(monkeypatch):
    # This will test the KeyError path
    with patch('django.core.files.storage.storages', {}):
        class DummySettings:
            THUMBNAIL_DEFAULT_STORAGE_ALIAS = 'no_such_alias'
        monkeypatch.setattr(easy_thumbnails.storage, 'settings', DummySettings)
        with pytest.raises(KeyError):
            easy_thumbnails.storage.get_storage()