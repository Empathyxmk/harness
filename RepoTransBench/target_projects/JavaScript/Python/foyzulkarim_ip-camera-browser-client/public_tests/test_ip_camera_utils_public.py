import pytest
from src.ip_camera_utils import get_snapshot_url, is_online

class TestGetSnapshotUrlPublic:
    def test_builds_snapshot_url_correctly_with_different_data(self):
        assert get_snapshot_url('https://example.com', 'cam42') == 'https://example.com/camera/cam42/snapshot'

    def test_throws_if_base_url_empty_string(self):
        with pytest.raises(ValueError, match="Missing arguments"):
            get_snapshot_url('', 'camx')

    def test_throws_if_camera_id_empty_string(self):
        with pytest.raises(ValueError, match="Missing arguments"):
            get_snapshot_url('https://yoursite.org', '')

    def test_throws_on_invalid_base_url_no_protocol(self):
        with pytest.raises(ValueError, match="Invalid baseUrl"):
            get_snapshot_url('localhost:5555', 'mycam')
        with pytest.raises(ValueError, match="Invalid baseUrl"):
            get_snapshot_url('ftp://myhost', 'mycam')


class TestIsOnlinePublic:
    def test_returns_true_for_a_different_connected_camera(self):
        assert is_online({'connected': True, 'lastPing': 9876}) is True

    def test_returns_false_if_connected_false_different_data(self):
        assert is_online({'connected': False, 'lastPing': 0}) is False

    def test_returns_false_for_object_with_no_connected_field(self):
        assert is_online({'foo': 'bar'}) is False
        assert is_online(None) is False
        assert is_online(None) is False  # None for both undefined/null