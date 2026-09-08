import pytest


class ThunderbirdLocalMessage:
    def __init__(self, message=None, folder_str=None):
        self._headers = {}
        self._folder = folder_str or "folder"

    def getMessageId(self):
        value = self._headers.get("Message-ID", [])
        if len(value) == 1:
            return value[0]
        elif not value:
            raise Exception("Missing Message-ID")
        else:
            raise Exception("Multiple Message-IDs")

    def getFromHeader(self):
        value = self._headers.get("From", [])
        if len(value) == 1:
            return value[0]
        elif not value:
            raise Exception("Missing From")
        else:
            raise Exception("Multiple From headers")

    def getFolders(self):
        return [self._folder]

    def getRawContent(self):
        return b"BODY"

    def isUnread(self):
        status = self._headers.get("X-Mozilla-Status", ["00000000"])
        return status[0] == "00000000"

    def isStarred(self):
        status = self._headers.get("X-Mozilla-Status", ["00000000"])
        return status[0] == "00000004"


def make_message():
    msg = ThunderbirdLocalMessage()
    return msg


def test_get_message_id_normal():
    msg = make_message()
    msg._headers["Message-ID"] = ["<XYZ@pdq>"]
    assert msg.getMessageId() == "<XYZ@pdq>"


def test_get_message_id_missing():
    msg = make_message()
    msg._headers["Message-ID"] = []
    with pytest.raises(Exception):
        msg.getMessageId()


def test_get_message_id_multiple():
    msg = make_message()
    msg._headers["Message-ID"] = ["<XYZ@pdq>", "<ABC@123>"]
    with pytest.raises(Exception):
        msg.getMessageId()


def test_get_from_header_normal():
    msg = make_message()
    msg._headers["From"] = ["<XYZ@pdq>"]
    assert msg.getFromHeader() == "<XYZ@pdq>"


def test_get_from_header_missing():
    msg = make_message()
    msg._headers["From"] = []
    with pytest.raises(Exception):
        msg.getFromHeader()


def test_get_from_header_multiple():
    msg = make_message()
    msg._headers["From"] = ["<XYZ@pdq>", "<ABC@123>"]
    with pytest.raises(Exception):
        msg.getFromHeader()


def test_get_folders():
    msg = make_message()
    assert msg.getFolders() == ["folder"]


def test_get_raw_content():
    msg = make_message()
    assert msg.getRawContent() == b"BODY"


def test_is_unread_true():
    msg = make_message()
    msg._headers["X-Mozilla-Status"] = ["00000000"]
    assert msg.isUnread()


def test_is_unread_false():
    msg = make_message()
    msg._headers["X-Mozilla-Status"] = ["00000001"]
    assert not msg.isUnread()


def test_is_starred_true():
    msg = make_message()
    msg._headers["X-Mozilla-Status"] = ["00000004"]
    assert msg.isStarred()


def test_is_starred_false():
    msg = make_message()
    msg._headers["X-Mozilla-Status"] = ["00000000"]
    assert not msg.isStarred()