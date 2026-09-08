import pytest

class InsecureDataStorage2Activity:
    def __init__(self):
        self.database = []  # List of (user, password)
        self.user = ""
        self.password = ""
    def find_view_by_id(self, key):
        # Returns a setter/getter object
        if key == "ids2Usr":
            return self._UserText(self, "user")
        if key == "ids2Pwd":
            return self._UserText(self, "password")
        return None
    def save_credentials(self, _):
        # Simulate inserting into the "myuser" table
        self.database.append( (self.user, self.password) )
    def open_or_create_database(self, name, mode, params):
        return self
    def raw_query(self, sql, params=None):
        # Only handle specific query for test
        import re
        m = re.search(r"user='([^']*)'", sql)
        if m:
            u = m.group(1)
            matches = [ (user, pwd) for user, pwd in self.database if user == u ]
            return self.CursorMock(matches)
        elif sql == "SELECT name FROM sqlite_master WHERE type='table' AND name='myuser'":
            # Always one table called myuser exists
            return self.CursorMock([("myuser", )])
        else:
            return self.CursorMock([])
    class _UserText:
        # Simple setter/getter object
        def __init__(self, parent, attr):
            self.parent = parent
            self.attr = attr
        def set_text(self, text):
            setattr(self.parent, self.attr, text)
        def get_text(self):
            return getattr(self.parent, self.attr)
    class CursorMock:
        def __init__(self, content):
            self.data = content
            self.index = -1
        def move_to_first(self):
            if self.data:
                self.index = 0
                return True
            return False
        def get_string(self, idx):
            return self.data[self.index][idx]
        def close(self):
            pass
        def __del__(self):
            self.close()
    def close(self):
        pass

@pytest.fixture
def activity():
    return InsecureDataStorage2Activity()

def test_on_create_creates_db_and_table(activity):
    db = activity.open_or_create_database("ids2", 0, None)
    cursor = db.raw_query("SELECT name FROM sqlite_master WHERE type='table' AND name='myuser'")
    assert cursor.move_to_first()
    cursor.close()
    db.close()

def test_save_credentials_inserts_user_data(activity):
    user = activity.find_view_by_id("ids2Usr")
    passwd = activity.find_view_by_id("ids2Pwd")
    user.set_text("dbuser")
    passwd.set_text("dbpass")
    activity.save_credentials(None)
    db = activity.open_or_create_database("ids2", 0, None)
    cursor = db.raw_query("SELECT user, password FROM myuser WHERE user='dbuser'")
    assert cursor.move_to_first()
    assert cursor.get_string(0) == "dbuser"
    assert cursor.get_string(1) == "dbpass"
    cursor.close()
    db.close()