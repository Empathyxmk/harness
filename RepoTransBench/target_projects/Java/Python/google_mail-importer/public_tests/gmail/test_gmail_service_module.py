def test_different_provides_mailbox_name():
    class GmailServiceModule:
        def __init__(self, mailbox_name):
            self.mailbox_name = mailbox_name

    module = GmailServiceModule("PublicMailboxName")
    assert module.mailbox_name == "PublicMailboxName"