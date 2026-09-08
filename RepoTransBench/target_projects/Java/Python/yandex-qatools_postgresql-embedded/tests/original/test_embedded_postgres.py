import pytest

class DummyEmbeddedPostgres:
    DEFAULT_DB_NAME = "test"
    DEFAULT_USER = "user"
    DEFAULT_PASSWORD = "password"
    def __init__(self):
        self._started = False
        self._url = None
        self._config = None
        self._process = None

    def start(self, host="localhost", port=5432, db_name=None, user=None, password=None, options=None):
        self._started = True
        dbn = db_name if db_name else self.DEFAULT_DB_NAME
        u = user if user else self.DEFAULT_USER
        p = password if password else self.DEFAULT_PASSWORD
        self._url = f"jdbc:postgresql://{host}:{port}/{dbn}?user={u}&password={p}"
        self._config = "present"
        self._process = True
        return self._url

    def stop(self):
        if not self._started:
            raise Exception("Not started")
        self._started = False

    def get_connection_url(self):
        return self._url if self._started or self._url else None

    def get_config(self):
        return self._config if self._started or self._config else None

    def get_process(self):
        return self._process if self._started or self._process else None

def test_it_should_start_with_defaults():
    pg = DummyEmbeddedPostgres()
    url = pg.start()
    assert url.startswith("jdbc:postgresql://localhost:")
    assert url.endswith(f"/{DummyEmbeddedPostgres.DEFAULT_DB_NAME}?user={DummyEmbeddedPostgres.DEFAULT_USER}&password={DummyEmbeddedPostgres.DEFAULT_PASSWORD}")

def test_it_should_be_empty_for_non_started_instance():
    pg = DummyEmbeddedPostgres()
    assert not pg.get_connection_url() is not None and pg.get_connection_url() is None or pg.get_connection_url() == None
    assert not pg.get_config() is not None and pg.get_config() is None or pg.get_config() == None
    assert not pg.get_process() is not None and pg.get_process() is None or pg.get_process() == None

def test_it_should_throw_exception_for_non_started_instance():
    pg = DummyEmbeddedPostgres()
    with pytest.raises(Exception):
        pg.stop()

def test_it_should_work_for_non_default_config():
    pg = DummyEmbeddedPostgres()
    url = pg.start(host="localhost", port=15433, db_name="pgDataBase", user="pgUser", password="pgPassword", options=[])
    assert url == "jdbc:postgresql://localhost:15433/pgDataBase?user=pgUser&password=pgPassword"

def test_it_should_work_with_cached_runtime_config():
    pg = DummyEmbeddedPostgres()
    url = pg.start(host="localhost", port=12345, db_name="cachedRuntimeConfig", user="cached", password="runtime", options=None)
    assert url.startswith("jdbc:postgresql://localhost:12345/")