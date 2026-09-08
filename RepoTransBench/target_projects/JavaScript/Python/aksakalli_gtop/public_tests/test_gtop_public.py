import sys
import types
import pytest
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def blessed_and_contrib_mocks(monkeypatch):
    screen_mock = MagicMock()
    mocked_blessed = MagicMock()
    mocked_blessed.screen.return_value = screen_mock
    mocked_blessed.box.return_value = {}
    sys.modules['blessed'] = mocked_blessed

    table_instance = MagicMock()
    mocked_contrib = MagicMock()
    grid_mock = MagicMock()
    grid_mock.set.return_value = table_instance
    mocked_contrib.grid.return_value = grid_mock
    mocked_contrib.donut = MagicMock()
    mocked_contrib.line = MagicMock()
    mocked_contrib.table.return_value = table_instance
    mocked_contrib.sparkline = MagicMock()
    sys.modules['blessed-contrib'] = mocked_contrib

    yield
    del sys.modules['blessed']
    del sys.modules['blessed-contrib']

def test_gtop_import_public():
    try:
        import importlib
        importlib.import_module("gtop")
    except Exception as e:
        pytest.fail(f"Importing gtop (public) raised: {e}")