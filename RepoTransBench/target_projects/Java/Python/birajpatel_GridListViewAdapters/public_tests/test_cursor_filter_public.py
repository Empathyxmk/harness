import pytest
from unittest.mock import Mock

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
            pass

@pytest.fixture
def setup_public(mocker):
    client = Mock()
    cursor = Mock()
    return client, cursor

def test_convert_result_to_string_public(setup_public):
    client, cursor = setup_public
    client.convertToString.return_value = "publicTest"
    filt = DummyCursorFilter(client)
    assert filt.convertResultToString(cursor) == "publicTest"

def test_perform_filtering_with_cursor_public(setup_public):
    client, cursor = setup_public
    client.runQueryOnBackgroundThread.return_value = cursor
    cursor.getCount.return_value = 7
    filt = DummyCursorFilter(client)
    results = filt.performFiltering("xyz")
    assert results.count == 7
    assert results.values == cursor

def test_perform_filtering_null_cursor_public(setup_public):
    client, cursor = setup_public
    client.runQueryOnBackgroundThread.return_value = None
    filt = DummyCursorFilter(client)
    results = filt.performFiltering("nullcase")
    assert results.count == 0
    assert results.values is None

def test_publish_results_with_non_null_cursor_different_from_old_public(setup_public):
    client, cursor = setup_public
    old_cursor = Mock()
    results = DummyFilterResults()
    results.values = cursor
    client.getCursor.return_value = old_cursor
    filt = DummyCursorFilter(client)
    filt.publishResults("z", results)
    client.changeCursor.assert_called_with(cursor)

def test_publish_results_with_null_values_public(setup_public):
    client, cursor = setup_public
    results = DummyFilterResults()
    results.values = None
    client.getCursor.return_value = cursor
    filt = DummyCursorFilter(client)
    filt.publishResults("z", results)
    client.changeCursor.assert_not_called()

def test_publish_results_with_same_cursor_public(setup_public):
    client, cursor = setup_public
    results = DummyFilterResults()
    results.values = cursor
    client.getCursor.return_value = cursor
    filt = DummyCursorFilter(client)
    filt.publishResults("z", results)
    client.changeCursor.assert_not_called()