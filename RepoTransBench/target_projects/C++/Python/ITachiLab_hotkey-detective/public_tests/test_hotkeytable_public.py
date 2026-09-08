from src.hotkey_detective.hotkey_table import HotkeyTable

def test_hotkeytable_set_and_get_different_hotkey_values():
    table = HotkeyTable()
    key1 = "Save"
    val1 = 77
    key2 = "Open"
    val2 = 22

    assert not table.has_hotkey(key1)
    assert not table.has_hotkey(key2)

    table.set_hotkey(key1, val1)
    table.set_hotkey(key2, val2)

    assert table.has_hotkey(key1)
    assert table.has_hotkey(key2)

    assert table.get_hotkey(key1) == val1
    assert table.get_hotkey(key2) == val2

def test_hotkeytable_replace_with_different_key_and_value():
    table = HotkeyTable()
    key = "Close"
    first = 10
    second = 99

    assert not table.has_hotkey(key)
    table.set_hotkey(key, first)
    assert table.has_hotkey(key)
    assert table.get_hotkey(key) == first

    table.set_hotkey(key, second)
    assert table.has_hotkey(key)
    assert table.get_hotkey(key) == second