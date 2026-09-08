import types
import pytest
from Chapter11 import email_facade

class DummySMTP:
    def __init__(self, host):
        self.host = host
        self.sent = False
        self.logged_in = False

    def login(self, user, pw):
        self.logged_in = (user, pw)

    def sendmail(self, from_email, to_list, msg):
        self.sent = True
        self.last_args = (from_email, to_list, msg)

class DummyIMAP4:
    def __init__(self, host):
        self.host = host
        self.logged = False
        self.selected = False
        self.fetched = False

    def login(self, user, pw):
        self.logged = (user, pw)

    def select(self):
        self.selected = True

    def search(self, *args):
        return 'OK', [b'1 2']

    def fetch(self, num, what):
        # Basic mock values
        return 'OK', [(None, bytes(f'Message{num.decode()}', 'utf8'))]

def test_send_email_monkeypatch(monkeypatch):
    ef = email_facade.EmailFacade("host.com", "user", "pw")
    dummy = DummySMTP("host.com")
    monkeypatch.setattr(email_facade.smtplib, "SMTP", lambda host: dummy)
    ef.send_email("dest@host.com", "Hi", "Message body")
    assert dummy.logged_in == ("user", "pw")
    assert dummy.sent
    assert "From: user@host.com" in dummy.last_args[2]
    assert dummy.last_args[1] == ["dest@host.com"]

def test_send_email_with_full_address(monkeypatch):
    ef = email_facade.EmailFacade("host.com", "auser@domain.com", "pw")
    dummy = DummySMTP("host.com")
    monkeypatch.setattr(email_facade.smtplib, "SMTP", lambda host: dummy)
    ef.send_email("to@host.com", "Subj", "Body")
    assert dummy.logged_in[0] == "auser@domain.com"
    assert dummy.sent
    assert "From: auser@domain.com" in dummy.last_args[2]

def test_get_inbox_monkeypatch(monkeypatch):
    ef = email_facade.EmailFacade("s", "u", "p")
    dummy = DummyIMAP4("s")

    monkeypatch.setattr(email_facade.imaplib, "IMAP4", lambda host: dummy)
    result = ef.get_inbox()
    assert dummy.logged is not False
    assert dummy.selected
    assert len(result) == 2
    assert isinstance(result[0], bytes)