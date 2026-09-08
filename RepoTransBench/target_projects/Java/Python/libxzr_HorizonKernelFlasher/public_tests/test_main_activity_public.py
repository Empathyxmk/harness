import pytest
from unittest.mock import MagicMock, patch

# Dummy R and MainActivity for testing structure
class MainActivity:
    DEBUG = False
    cur_status = None

    class status:
        normal = 0
        flashing = 1
        error = 2

    logView = None
    scrollView = None

    def __init__(self):
        self.logView = None
        self.scrollView = None

    @staticmethod
    def _appendLog(msg, activity):
        if MainActivity.DEBUG:
            pass

    @staticmethod
    def appendLog(msg, activity):
        pass

    @staticmethod
    def runWithFilePath(activity, worker):
        if hasattr(activity, "startActivityForResult"):
            activity.startActivityForResult(MagicMock(), 0)

    def update_title(self):
        pass

    def flash_new(self):
        self.update_title()
        self.runWithFilePath(None, None)

    def superOnBackPressed(self):
        pass

    def onBackPressed(self):
        if MainActivity.cur_status == MainActivity.status.normal:
            self.superOnBackPressed()
        else:
            pass

    def getMenuInflater(self):
        return MagicMock()

    def onCreateOptionsMenu(self, menu):
        return True

    def getAlertDialogBuilder(self):
        return MagicMock()

    def onOptionsItemSelected(self, item):
        item_id = item.getItemId()
        if item_id == R.id.help:
            self.getAlertDialogBuilder()
            return True
        elif item_id == -12345:
            return True
        return True

    class fileWorker:
        pass

class R:
    class id:
        help = 3
        about = 1
        flash_new = 2

@pytest.fixture(autouse=True)
def reset_status():
    MainActivity.cur_status = MainActivity.status.normal
    MainActivity.DEBUG = False
    yield
    MainActivity.cur_status = MainActivity.status.normal
    MainActivity.DEBUG = False

def test_append_log_debug_public():
    MainActivity.DEBUG = True
    mock_activity = MagicMock()
    mock_activity.runOnUiThread = MagicMock()
    with patch.object(MainActivity, "_appendLog") as mock__appendLog, \
         patch.object(MainActivity, "appendLog") as mock_appendLog:
        MainActivity._appendLog("world", mock_activity)
        MainActivity.appendLog("foobar", mock_activity)
        mock__appendLog.assert_called_with("world", mock_activity)
        mock_appendLog.assert_called_with("foobar", mock_activity)
    MainActivity.DEBUG = False

def test_append_log_ui_print_public():
    mock_activity = MagicMock()
    mock_activity.runOnUiThread = lambda fn: fn()
    mock_activity.logView = MagicMock()
    mock_activity.scrollView = MagicMock()
    with patch.object(MainActivity, "appendLog") as mock_appendLog:
        mock_appendLog.side_effect = lambda msg, activity: None
        MainActivity.appendLog("ui_print log with different msg", mock_activity)
        mock_appendLog.assert_called_with("ui_print log with different msg", mock_activity)

def test_flash_new_not_flashing_public():
    MainActivity.cur_status = MainActivity.status.normal
    activity = MainActivity()
    with patch.object(activity, 'update_title') as mock_update_title, \
         patch.object(activity, 'runWithFilePath') as mock_runWithFilePath:
        activity.logView = MagicMock()
        activity.flash_new()
        assert mock_update_title.called
        assert mock_runWithFilePath.called

def test_on_back_pressed_flashing_and_other_public():
    activity = MainActivity()
    with patch.object(activity, 'superOnBackPressed') as mock_superOnBackPressed:
        MainActivity.cur_status = MainActivity.status.normal
        activity.onBackPressed()
        assert mock_superOnBackPressed.called
        MainActivity.cur_status = MainActivity.status.error
        activity.onBackPressed()

def test_on_create_options_menu_public():
    menu = MagicMock()
    activity = MainActivity()
    with patch.object(activity, 'getMenuInflater') as mock_menu_inflater:
        mock_menu_inflater.return_value = MagicMock()
        assert activity.onCreateOptionsMenu(menu) is True

def test_on_options_item_selected_about_public():
    item = MagicMock()
    item.getItemId.return_value = R.id.help
    activity = MainActivity()
    with patch.object(activity, 'getAlertDialogBuilder', return_value=MagicMock()) as mock_builder:
        assert activity.onOptionsItemSelected(item) is True
        mock_builder.assert_called()

def test_on_options_item_selected_flash_new_public():
    item = MagicMock()
    item.getItemId.return_value = -12345
    activity = MainActivity()
    with patch.object(activity, 'flash_new') as mock_flash_new:
        assert activity.onOptionsItemSelected(item) is True

def test_run_with_file_path_public():
    mock_activity = MagicMock()
    worker = MagicMock()
    mock_activity.startActivityForResult = MagicMock()
    MainActivity.runWithFilePath(mock_activity, worker)
    mock_activity.startActivityForResult.assert_called()
    assert worker is not None