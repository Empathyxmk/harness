import pytest

from src.aegis1980.hotspot.hotspot_manager import HotSpotManager

class TestHotSpotManagerOriginal:
    def test_initial_state(self):
        manager = HotSpotManager()
        assert not manager.is_enabled()
        assert manager.get_ssid() == "defaultSSID"
        assert manager.get_password() == "password"

    def test_enable_hotspot_valid(self):
        manager = HotSpotManager()
        result = manager.enable_hotspot("MySSID", "MyPass123")
        assert result
        assert manager.is_enabled()
        assert manager.get_ssid() == "MySSID"
        assert manager.get_password() == "MyPass123"

    def test_enable_hotspot_invalid_ssid(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot(None, "password123")
        assert not manager.enable_hotspot("", "password123")
        assert not manager.is_enabled()

    def test_enable_hotspot_invalid_password(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot("SSID", None)
        assert not manager.enable_hotspot("SSID", "short")
        assert not manager.is_enabled()

    def test_disable_hotspot(self):
        manager = HotSpotManager()
        manager.enable_hotspot("SSID", "password123")
        assert manager.is_enabled()
        manager.disable_hotspot()
        assert not manager.is_enabled()

    # NEW TESTS FOR FULL BRANCH COVERAGE

    def test_enable_hotspot_password_exactly_8(self):
        manager = HotSpotManager()
        password8 = "12345678"  # Exactly 8 chars
        result = manager.enable_hotspot("SSID2", password8)
        assert result
        assert manager.is_enabled()
        assert manager.get_ssid() == "SSID2"
        assert manager.get_password() == password8

    def test_disabling_twice(self):
        manager = HotSpotManager()
        # Disable even if not enabled, should not throw or change state
        manager.disable_hotspot()
        assert not manager.is_enabled()
        manager.enable_hotspot("SSID", "password123")
        assert manager.is_enabled()
        manager.disable_hotspot()
        assert not manager.is_enabled()
        # Try disabling twice in a row
        manager.disable_hotspot()
        assert not manager.is_enabled()

    def test_enable_hotspot_password_with_8_but_null_ssid(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot(None, "12345678")
        assert not manager.is_enabled()

    def test_enable_hotspot_null_password(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot("SSID", None)
        assert not manager.is_enabled()

    # Defensive: try changing SSID/password after hotspot enabled
    def test_multiple_enables(self):
        manager = HotSpotManager()
        assert manager.enable_hotspot("SSID", "password123")
        assert manager.get_ssid() == "SSID"
        assert manager.get_password() == "password123"
        assert manager.is_enabled()

        # Enable with new values
        assert manager.enable_hotspot("SSID2", "password456")
        assert manager.get_ssid() == "SSID2"
        assert manager.get_password() == "password456"
        assert manager.is_enabled()

    # Blank password but valid SSID
    def test_enable_hotspot_empty_password(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot("SSID", "")
        assert not manager.is_enabled()