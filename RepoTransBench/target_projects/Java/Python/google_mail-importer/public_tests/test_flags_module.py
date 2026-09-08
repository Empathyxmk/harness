def test_flags_module_provides_different_instance():
    class CommandLineArguments:
        pass

    args = CommandLineArguments()
    args.mailboxFileName = "/opt/mailbox"
    args.user = "pubuser@domain.com"
    args.maxMessages = 109
    args.clientSecretResourcePath = "/foo/bar/client_secret_new.json"

    injected = args
    assert injected is args
    assert injected.mailboxFileName == "/opt/mailbox"
    assert injected.user == "pubuser@domain.com"
    assert injected.maxMessages == 109
    assert injected.clientSecretResourcePath == "/foo/bar/client_secret_new.json"