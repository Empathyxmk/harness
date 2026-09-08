import pytest

class Card:
    pass

class CursorGridAdapter:
    def __init__(self, context, totalCardsInRow, cursor):
        self.mCursor = cursor
        self.mFilterQueryProvider = None

    def getCursor(self):
        return self.mCursor

    def changeCursor(self, cursor):
        old = self.mCursor
        if old is not None and old != cursor:
            old.close()
        self.mCursor = cursor

    def swapCursor(self, cursor):
        if self.mCursor == cursor:
            return None
        old = self.mCursor
        self.mCursor = cursor
        return old

    def convertToString(self, cursor):
        return "" if cursor is None else str(cursor)

    def runQueryOnBackgroundThread(self, constraint):
        if self.mFilterQueryProvider:
            return self.mFilterQueryProvider.runQuery(constraint)
        else:
            return self.mCursor

class FilterQueryProvider:
    def runQuery(self, query):
        pass

class ConcreteCursorGridAdapter(CursorGridAdapter):
    def __init__(self, context, totalCardsInRow, cursor):
        super().__init__(context, totalCardsInRow, cursor)
    def getView(self, position, convertView, parent):
        return None
    def getNewCard(self, cardPositionInRow):
        return None

@pytest.fixture
def adapter(mocker):
    mock_context = mocker.Mock()
    mock_cursor = mocker.Mock()
    # Provide display metrics on chained calls
    mock_context.getSystemService.return_value = None
    dm = mocker.Mock()
    dm.widthPixels = 240
    dm.heightPixels = 320
    mock_context.getResources.return_value.getDisplayMetrics.return_value = dm
    mock_cursor.getCount.return_value = 5
    return ConcreteCursorGridAdapter(mock_context, 2, mock_cursor), mock_cursor, mock_context

def test_returns_same_cursor_from_get_cursor(adapter):
    a, mock_cursor, _ = adapter
    assert a.getCursor() == mock_cursor

def test_change_cursor_closes_old(mocker, adapter):
    a, mock_cursor, _ = adapter
    old = mocker.Mock()
    a.mCursor = old
    new_cursor = mocker.Mock()
    new_cursor.getCount.return_value = 3
    a.changeCursor(new_cursor)
    old.close.assert_called_once()
    assert a.getCursor() == new_cursor

def test_swap_cursor_returns_null_when_same(adapter):
    a, mock_cursor, _ = adapter
    a.mCursor = mock_cursor
    assert a.swapCursor(mock_cursor) is None

def test_swap_cursor_returns_old_and_updates(mocker, adapter):
    a, _, _ = adapter
    old = mocker.Mock()
    newC = mocker.Mock()
    newC.getCount.return_value = 4
    a.mCursor = old
    result = a.swapCursor(newC)
    assert result == old
    assert a.getCursor() == newC

def test_swap_cursor_to_null(adapter, mocker):
    a, mock_cursor, _ = adapter
    a.mCursor = mock_cursor
    returned = a.swapCursor(None)
    assert returned == mock_cursor
    assert a.getCursor() is None

def test_convert_to_string_handles_null(adapter):
    a, _, _ = adapter
    assert a.convertToString(None) == ""

def test_convert_to_string_handles_non_null(mocker, adapter):
    a, _, _ = adapter
    c = mocker.Mock()
    c.__str__ = lambda s: "CURSORSTR"
    assert a.convertToString(c) == "CURSORSTR"

def test_run_query_on_background_thread_with_provider(mocker, adapter):
    a, _, _ = adapter
    cursor = mocker.Mock()
    provider = mocker.Mock(spec=FilterQueryProvider)
    provider.runQuery.return_value = cursor
    a.mFilterQueryProvider = provider
    assert a.runQueryOnBackgroundThread("kkk") == cursor

def test_run_query_on_background_thread_no_provider(adapter):
    a, mock_cursor, _ = adapter
    a.mCursor = mock_cursor
    a.mFilterQueryProvider = None
    assert a.runQueryOnBackgroundThread("z") == mock_cursor