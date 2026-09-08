def test_defaults_public():
    class CommandLineArguments:
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


def test_set_arguments_public():
    class CommandLineArguments:
        def __init__(self):
            self.mailboxFileName = None
            self.user = "me"
            self.maxMessages = None
            self.clientSecretResourcePath = "/resources/client_secret.json"

    args = CommandLineArguments()
    args.mailboxFileName = "/var/mail"
    args.user = "anotheruser@domain.com"
    args.maxMessages = 42
    args.clientSecretResourcePath = "/different/path/secret_v2.json"
    assert args.mailboxFileName == "/var/mail"
    assert args.user == "anotheruser@domain.com"
    assert args.maxMessages == 42
    assert args.clientSecretResourcePath == "/different/path/secret_v2.json"