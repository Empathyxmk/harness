import pytest

class DummyEmbeddedPostgres:
    def __init__(self):
        self.started = False

    def start(self, user, passwd):
        self.started = (user == "publicUser" and passwd == "publicPass")

    def is_started(self):
        return self.started

def test_can_start_with_different_credentials():
    pg = DummyEmbeddedPostgres()
    pg.start("publicUser", "publicPass")
    assert pg.is_started()

def test_fails_to_start_with_wrong_credentials():
    pg = DummyEmbeddedPostgres()
    pg.start("bad", "creds")
    assert not pg.is_started()