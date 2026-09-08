import pytest


class AnotherDummyMailProvider:
    def __init__(self, should_throw):
        self.should_throw = should_throw

    def get(self):
        if self.should_throw:
            raise Exception("provider fail")
        return 12345


def test_get_different_success():
    mail_provider = AnotherDummyMailProvider(False)
    assert mail_provider.get() == 12345


def test_get_throws_messaging_exception_public():
    mail_provider = AnotherDummyMailProvider(True)
    with pytest.raises(Exception) as excinfo:
        mail_provider.get()
    assert str(excinfo.value) == "provider fail"