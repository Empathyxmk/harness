import pytest
from unittest import mock


class FakeLocalMessage:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

    def getMessageId(self):
        return None

    def getFromHeader(self):
        return None

    def getFolders(self):
        return None

    def getRawContent(self):
        return b''

    def isUnread(self):
        return False

    def isStarred(self):
        return False


class Mailbox:
    def map_message_ids(self, message_ids):
        return {}


class GmailSyncer:
    def __init__(self, mailbox):
        self.mailbox = mailbox
        self.initialized = False

    def init(self):
        self.initialized = True

    def sync(self, messages):
        if not self.initialized:
            raise Exception("sync() should fail if init() is not called first.")
        for msg in messages:
            pass
        # Do not call mailbox.uploadMessage for an empty list unless intended


def test_init_required_before_sync():
    mailbox = mock.Mock()
    gmail_syncer = GmailSyncer(mailbox)
    with pytest.raises(Exception):
        gmail_syncer.sync([])


def test_sync_empty_list():
    mailbox = mock.Mock()
    gmail_syncer = GmailSyncer(mailbox)
    mailbox.uploadMessage = mock.Mock()
    gmail_syncer.init()
    gmail_syncer.sync([])
    mailbox.uploadMessage.assert_not_called()


def test_sync_with_messages():
    mailbox = mock.Mock()
    gmail_syncer = GmailSyncer(mailbox)
    gmail_syncer.init()
    messages = [FakeLocalMessage("Subject 1", "Hello"), FakeLocalMessage("Subject 2", "Good bye")]
    gmail_syncer.sync(messages)