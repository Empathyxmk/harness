import pytest
from pywizlight.discovery import _wiz_mdns_name, _default_mac

def test_wiz_mdns_name_public():
    # Use a different MAC address not in original
    mac = "11:22:33:44:55:66"
    assert _wiz_mdns_name(mac) == "WIZ_112233445566._wiz._udp.local."

def test_default_mac_public():
    # Use a different IP address not in original test
    ip = "192.168.2.22"
    port = 9020
    # Expect a specific formatted mac
    mac = _default_mac(ip, port)
    # The result should always be 12 hex digits in upper case
    assert mac == "C0A80216" + "232C"  # 192 = C0, 168 = A8, 2 = 02, 22 = 16, 9020 = 232C