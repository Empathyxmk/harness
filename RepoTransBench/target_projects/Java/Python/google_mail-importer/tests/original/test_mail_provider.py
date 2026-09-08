import pytest


class DummyMailProvider:
    def __init__(self, throw_exception):
        self.throw_exception = throw_exception

    def get(self):
        if self.throw_exception:
            raise Exception("fail")  # Mimics javax.mail.MessagingException
        return "success"


def test_get_success():
    mail_provider = DummyMailProvider(False)
    assert mail_provider.get() == "success"


def test_get_throws_exception():
    mail_provider = DummyMailProvider(True)
    with pytest.raises(Exception) as excinfo:
        mail_provider.get()
    assert str(excinfo.value) == "fail"