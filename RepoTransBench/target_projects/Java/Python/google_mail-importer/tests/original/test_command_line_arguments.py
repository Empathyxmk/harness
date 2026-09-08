def test_defaults():
    class CommandLineArguments:
        mailboxFileName = None
        user = "me"
        maxMessages = None
        clientSecretResourcePath = "/resources/client_secret.json"

        def __init__(self):
            self.mailboxFileName = None
            self.user = "me"
            self.maxMessages = None
            self.clientSecretResourcePath = "/resources/client_secret.json"

    args = CommandLineArguments()
    assert args.mailboxFileName is None
    assert args.user == "me"
    assert args.maxMessages is None
    assert args.clientSecretResourcePath == "/resources/client_secret.json"


def test_set_arguments():
    class CommandLineArguments:
        def __init__(self):
            self.mailboxFileName = None
            self.user = "me"
            self.maxMessages = None
            self.clientSecretResourcePath = "/resources/client_secret.json"

    args = CommandLineArguments()
    args.mailboxFileName = "/tmp/mail"
    args.user = "user@example.com"
    args.maxMessages = 10
    args.clientSecretResourcePath = "/custom/path/secret.json"
    assert args.mailboxFileName == "/tmp/mail"
    assert args.user == "user@example.com"
    assert args.maxMessages == 10
    assert args.clientSecretResourcePath == "/custom/path/secret.json"