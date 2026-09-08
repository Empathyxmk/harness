import pytest
import logging
from unittest import mock


class CommandLineArguments:
    def __init__(self):
        self.maxMessages = None


class Importer:
    BATCH_SIZE = 100

    def __init__(self, logger, storage_provider, gmail_syncer, args):
        self.logger = logger
        self.storage_provider = storage_provider
        self.gmail_syncer = gmail_syncer
        self.args = args

    def import_mail(self):
        storage = self.storage_provider.get()
        iterator = iter(storage)
        self.gmail_syncer.init()
        count = 0
        messages = []
        try:
            max_msgs = self.args.maxMessages
            for msg in iterator:
                messages.append(msg)
                count += 1
                if max_msgs is not None and len(messages) == max_msgs:
                    break
                if len(messages) == self.BATCH_SIZE:
                    self.gmail_syncer.sync(messages)
                    messages = []
            if messages:
                self.gmail_syncer.sync(messages)
        except Exception:
            raise


def test_imports_no_messages():
    logger = logging.getLogger("test")
    storage = []
    storage_provider = mock.Mock()
    storage_provider.get.return_value = storage
    gmail_syncer = mock.Mock()
    args = CommandLineArguments()
    importer = Importer(logger, storage_provider, gmail_syncer, args)

    importer.import_mail()

    gmail_syncer.init.assert_called_once()
    gmail_syncer.sync.assert_not_called()


def test_imports_some_messages_with_max_messages():
    logger = logging.getLogger("test")
    msg1 = mock.Mock()
    msg1.getMessageId.return_value = "1"
    msg1.getFolders.return_value = ["INBOX"]
    msg2 = mock.Mock()
    msg2.getMessageId.return_value = "2"
    msg2.getFolders.return_value = ["INBOX"]
    storage = [msg1, msg2]
    storage_provider = mock.Mock()
    storage_provider.get.return_value = storage
    gmail_syncer = mock.Mock()
    args = CommandLineArguments()
    args.maxMessages = 1
    importer = Importer(logger, storage_provider, gmail_syncer, args)

    importer.import_mail()

    gmail_syncer.init.assert_called_once()
    gmail_syncer.sync.assert_called_once()
    # The GmailSyncer sync receives the batch
    batch = gmail_syncer.sync.call_args[0][0]
    assert len(batch) == 1
    assert batch[0] == msg1


def test_batching_behavior():
    logger = logging.getLogger("test")
    batch_size = 100
    total_messages = batch_size + 10
    messages = []
    for i in range(total_messages):
        msg = mock.Mock()
        msg.getMessageId.return_value = str(i)
        msg.getFolders.return_value = ["INBOX"]
        messages.append(msg)
    storage_provider = mock.Mock()
    storage_provider.get.return_value = messages
    gmail_syncer = mock.Mock()
    args = CommandLineArguments()
    args.maxMessages = None
    importer = Importer(logger, storage_provider, gmail_syncer, args)

    importer.import_mail()

    gmail_syncer.init.assert_called_once()
    # Should call sync twice: once for batch_size, once for remaining 10
    assert gmail_syncer.sync.call_count == 2


def test_storage_provider_throws_exception():
    logger = logging.getLogger("test")
    storage_provider = mock.Mock()
    storage_provider.get.side_effect = Exception("fail")
    gmail_syncer = mock.Mock()
    args = CommandLineArguments()
    importer = Importer(logger, storage_provider, gmail_syncer, args)

    with pytest.raises(Exception) as excinfo:
        importer.import_mail()
    assert str(excinfo.value) == "fail"


def test_gmail_syncer_throws_ioerror():
    logger = logging.getLogger("test")
    storage = []
    storage_provider = mock.Mock()
    storage_provider.get.return_value = storage
    gmail_syncer = mock.Mock()
    gmail_syncer.init.side_effect = IOError("fail")
    args = CommandLineArguments()
    importer = Importer(logger, storage_provider, gmail_syncer, args)

    with pytest.raises(IOError) as excinfo:
        importer.import_mail()
    assert str(excinfo.value) == "fail"