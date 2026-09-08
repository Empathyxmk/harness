import pytest

class DummyPsqlProcess:
    def __init__(self):
        self.started = False
    def start(self):
        self.started = True

class DummyAbstractPsqlTest:
    def __init__(self):
        self.process = DummyPsqlProcess()
        self.conn = object()
        self._started = False
    def setUp(self):
        self.process.start()
        self._started = True
    def tearDown(self):
        self._started = False

def test_setup_and_teardown():
    t = DummyAbstractPsqlTest()
    t.setUp()
    assert t.process.started
    assert t._started
    t.tearDown()
    assert not t._started