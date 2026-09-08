import pytest
from src.hotkey_detective.hotkey_table import HotkeyTable

def test_hotkeytable_basic_functionality():
    table = HotkeyTable()
    assert table.has_hotkey("Save") is False
    table.set_hotkey("Save", 123)
    assert table.has_hotkey("Save") is True
    assert table.get_hotkey("Save") == 123
    assert table.get_hotkey("None") == -1

    table.set_hotkey("Open", 456)
    assert table.get_hotkey("Open") == 456

    # Overwrite
    table.set_hotkey("Save", 789)
    assert table.get_hotkey("Save") == 789