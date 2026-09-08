import pytest

from src.aegis1980.hotspot.hotspot_manager import HotSpotManager

class TestHotSpotManagerPublic:
    def test_initial_state_public(self):
        manager = HotSpotManager()
        assert not manager.is_enabled()
        assert manager.get_ssid() == "defaultSSID"
        assert manager.get_password() == "password"

    def test_enable_hotspot_valid_public(self):
        manager = HotSpotManager()
        result = manager.enable_hotspot("PublicSSID", "Another123")
        assert result
        assert manager.is_enabled()
        assert manager.get_ssid() == "PublicSSID"
        assert manager.get_password() == "Another123"

    def test_enable_hotspot_invalid_ssid_public(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot(None, "publicpass")
        assert not manager.enable_hotspot("", "publicpass")
        assert not manager.is_enabled()

    def test_enable_hotspot_invalid_password_public(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot("MyNetwork", None)
        assert not manager.enable_hotspot("MyNetwork", "short1")
        assert not manager.is_enabled()

    def test_disable_hotspot_public(self):
        manager = HotSpotManager()
        manager.enable_hotspot("Network42", "SuperPass9")
        assert manager.is_enabled()
        manager.disable_hotspot()
        assert not manager.is_enabled()

    def test_enable_hotspot_password_exactly_8_public(self):
        manager = HotSpotManager()
        password8 = "abcdefgh"  # Exactly 8 chars, different from original test
        result = manager.enable_hotspot("SSID_Public", password8)
        assert result
        assert manager.is_enabled()
        assert manager.get_ssid() == "SSID_Public"
        assert manager.get_password() == password8

    def test_disabling_twice_public(self):
        manager = HotSpotManager()
        manager.disable_hotspot()
        assert not manager.is_enabled()
        manager.enable_hotspot("PublicSSID2", "ExtraPass2")
        assert manager.is_enabled()
        manager.disable_hotspot()
        assert not manager.is_enabled()
        manager.disable_hotspot()
        assert not manager.is_enabled()

    def test_enable_hotspot_password_with_8_but_null_ssid_public(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot(None, "abcdefgh")
        assert not manager.is_enabled()

    def test_enable_hotspot_null_password_public(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot("AnotherNet", None)
        assert not manager.is_enabled()

    def test_multiple_enables_public(self):
        manager = HotSpotManager()
        assert manager.enable_hotspot("FirstSSID", "initPass99")
        assert manager.get_ssid() == "FirstSSID"
        assert manager.get_password() == "initPass99"
        assert manager.is_enabled()

        assert manager.enable_hotspot("SecondSSID", "reNewPass0")
        assert manager.get_ssid() == "SecondSSID"
        assert manager.get_password() == "reNewPass0"
        assert manager.is_enabled()

    def test_enable_hotspot_empty_password_public(self):
        manager = HotSpotManager()
        assert not manager.enable_hotspot("MyNet", "")
        assert not manager.is_enabled()