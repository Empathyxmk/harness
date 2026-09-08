def test_import_all_pytest_watcher_modules():
    # Try to import all main modules to check for import errors or side effects
    import pytest_watcher
    import pytest_watcher.__main__
    import pytest_watcher.commands
    import pytest_watcher.config
    import pytest_watcher.constants
    import pytest_watcher.event_handler
    import pytest_watcher.parse
    import pytest_watcher.terminal
    import pytest_watcher.trigger
    import pytest_watcher.watcher