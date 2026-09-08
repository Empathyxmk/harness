import pytest
from unittest.mock import Mock

class DummyCursor:
    def getCount(self):
        return 0

class DummyCursorFilterClient:
    def convertToString(self, cursor):
        return "test"
    def runQueryOnBackgroundThread(self, val):
        return None
    def getCursor(self):
        return None
    def changeCursor(self, cursor):
        self.changed = cursor

class DummyFilterResults:
    def __init__(self):
        self.count = 0
        self.values = None

class DummyCursorFilter:
    def __init__(self, client):
        self.client = client

    def convertResultToString(self, cursor):
        return self.client.convertToString(cursor)

    def performFiltering(self, query):
        cursor = self.client.runQueryOnBackgroundThread(query)
        results = DummyFilterResults()
        if cursor is not None:
            results.count = cursor.getCount()
            results.values = cursor
        else:
            results.count = 0
            results.values = None
        return results

    def publishResults(self, constraint, results):
        oldCursor = self.client.getCursor()
        if results.values is not None and results.values != oldCursor:
            self.client.changeCursor(results.values)
        else:
            # Should not call changeCursor
            pass

@pytest.fixture
def setup_mocks(mocker):
    client = Mock()
    cursor = Mock()
    return client, cursor

def test_convert_result_to_string(setup_mocks):
    client, cursor = setup_mocks
    client.convertToString.return_value = "test"
    filt = DummyCursorFilter(client)
    assert filt.convertResultToString(cursor) == "test"

def test_perform_filtering_with_cursor(setup_mocks):
    client, cursor = setup_mocks
    client.runQueryOnBackgroundThread.return_value = cursor
    cursor.getCount.return_value = 5

    filt = DummyCursorFilter(client)
    results = filt.performFiltering("abc")

    assert results.count == 5
    assert results.values == cursor

def test_perform_filtering_null_cursor(setup_mocks):
    client, cursor = setup_mocks
    client.runQueryOnBackgroundThread.return_value = None

    filt = DummyCursorFilter(client)
    results = filt.performFiltering("none")
    assert results.count == 0
    assert results.values is None

def test_publish_results_with_non_null_cursor_different_from_old(setup_mocks):
    client, cursor = setup_mocks
    old_cursor = Mock()
    results = DummyFilterResults()
    results.values = cursor
    client.getCursor.return_value = old_cursor

    filt = DummyCursorFilter(client)
    filt.publishResults("c", results)
    client.changeCursor.assert_called_with(cursor)

def test_publish_results_with_null_values(setup_mocks):
    client, cursor = setup_mocks
    results = DummyFilterResults()
    results.values = None
    client.getCursor.return_value = cursor

    filt = DummyCursorFilter(client)
    filt.publishResults("c", results)
    client.changeCursor.assert_not_called()

def test_publish_results_with_same_cursor(setup_mocks):
    client, cursor = setup_mocks
    results = DummyFilterResults()
    results.values = cursor
    client.getCursor.return_value = cursor

    filt = DummyCursorFilter(client)
    filt.publishResults("c", results)
    client.changeCursor.assert_not_called()