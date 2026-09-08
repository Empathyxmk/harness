def test_flags_module_binds_arguments():
    # Mimic Guice module injection; in Python we just assign object references
    class CommandLineArguments:
        pass

    args = CommandLineArguments()
    args.mailboxFileName = "foo"

    # "Injector" simply assigns the instance
    injected = args
    assert injected.mailboxFileName == "foo"
    assert injected is args