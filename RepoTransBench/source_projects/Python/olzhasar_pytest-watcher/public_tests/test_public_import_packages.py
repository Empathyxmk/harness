def test_import_each_pytest_watcher_module_directly():
    # Try to import each module separately to check for import errors or side effects
    import pytest_watcher
    import pytest_watcher.__main__ as main_mod
    import pytest_watcher.commands as commands_mod
    import pytest_watcher.config as config_mod
    import pytest_watcher.constants as const_mod
    import pytest_watcher.event_handler as eh_mod
    import pytest_watcher.parse as parse_mod
    import pytest_watcher.terminal as terminal_mod
    import pytest_watcher.trigger as trg_mod
    import pytest_watcher.watcher as watcher_mod
    # Ensure the names are present
    assert hasattr(main_mod, "__name__")
    assert hasattr(commands_mod, "__file__")