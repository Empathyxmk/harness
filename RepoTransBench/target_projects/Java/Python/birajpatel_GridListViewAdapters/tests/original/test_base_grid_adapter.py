import pytest

class DummyGridAdapter:
    def __init__(self):
        # Simulate base class initialization
        self.columns = 1
        self.rows = 1

    def getCount(self):
        # Dummy stub - just exercise the method
        return 0

    def getNumOfColumns(self):
        return self.columns

    def getNumOfRows(self):
        return self.rows

@pytest.fixture
def adapter():
    return DummyGridAdapter()

def test_get_count(adapter):
    adapter.getCount()

def test_get_num_of_columns(adapter):
    adapter.getNumOfColumns()

def test_get_num_of_rows(adapter):
    adapter.getNumOfRows()