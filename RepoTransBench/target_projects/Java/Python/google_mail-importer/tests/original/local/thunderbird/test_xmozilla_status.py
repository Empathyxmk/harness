import pytest


class XMozillaStatus:
    def __init__(self, statuses):
        self.statuses = statuses

    def is_read(self):
        return any(s == "00000001" or s == "00000005" for s in self.statuses)

    def is_marked(self):
        return any(s == "00000004" or s == "00000005" for s in self.statuses)


class XMozillaStatusParser:
    def parse(self, message):
        headers = getattr(message, "headers", [])
        if len(headers) == 0:
            return XMozillaStatus(["00000000"])
        elif len(headers) > 1:
            raise Exception("Multiple Status headers")
        else:
            return XMozillaStatus([headers[0]])


class JavaxMailMessage:
    def __init__(self, headers):
        self.headers = headers


def test_no_status_header():
    parser = XMozillaStatusParser()
    status = parser.parse(JavaxMailMessage([]))
    assert status is not None


def test_multiple_status_headers_throws_exception():
    parser = XMozillaStatusParser()
    with pytest.raises(Exception):
        parser.parse(JavaxMailMessage(["00000000", "00000000"]))


def test_is_read():
    parser = XMozillaStatusParser()
    status = parser.parse(JavaxMailMessage(["00000001"]))
    assert status.is_read()


def test_is_marked():
    parser = XMozillaStatusParser()
    status = parser.parse(JavaxMailMessage(["00000004"]))
    assert status.is_marked()


def test_is_marked_and_read():
    parser = XMozillaStatusParser()
    status = parser.parse(JavaxMailMessage(["00000005"]))
    assert status.is_read()
    assert status.is_read()  # Intentional (mimic test)