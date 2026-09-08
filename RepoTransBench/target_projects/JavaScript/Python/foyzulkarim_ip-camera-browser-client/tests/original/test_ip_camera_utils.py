import pytest
from src.ip_camera_utils import get_snapshot_url, is_online

class TestGetSnapshotUrl:
    def test_builds_snapshot_url_correctly(self):
        assert get_snapshot_url('http://host', 'cam1') == 'http://host/camera/cam1/snapshot'

    def test_throws_if_base_url_missing(self):
        with pytest.raises(ValueError, match="Missing arguments"):
            get_snapshot_url(None, 'cam1')

    def test_throws_if_camera_id_missing(self):
        with pytest.raises(ValueError, match="Missing arguments"):
            get_snapshot_url('http://host', None)

    def test_throws_on_invalid_base_url(self):
        with pytest.raises(ValueError, match="Invalid baseUrl"):
            get_snapshot_url('ftp://host', 'cam1')
        with pytest.raises(ValueError, match="Invalid baseUrl"):
            get_snapshot_url('host', 'cam1')


class TestIsOnline:
    def test_returns_true_for_connected_camera(self):
        assert is_online({'connected': True, 'lastPing': 1234}) is True

    def test_returns_false_if_not_connected(self):
        assert is_online({'connected': False, 'lastPing': 1234}) is False

    def test_returns_false_for_missing_connected(self):
        assert is_online({}) is False
        assert is_online(None) is False
        assert is_online(None) is False  # test with None for both undefined and null equivalent in Python