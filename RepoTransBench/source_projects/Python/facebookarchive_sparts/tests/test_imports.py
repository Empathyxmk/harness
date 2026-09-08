import importlib
import pkgutil

def test_import_all_sparts_modules():
    # Try to import all modules in sparts and sparts.tasks as a basic sanity check
    import sparts
    package_names = [
        'collections', 'compat', 'counters', 'ctx', 'daemon', 'deps',
        'fileutils', 'runit', 'sparts', 'tasks', 'timer', 'vservice', 'vtask'
    ]
    for name in package_names:
        importlib.import_module(f"sparts.{name}")

    # Submodules in sparts.tasks
    import sparts.tasks
    task_modules = [
        'dbus', 'fb303', 'file', 'periodic', 'poller', 'queue',
        'select', 'tornado', 'tornado_thrift', 'tui',
        'twisted', 'twisted_command'
    ]
    for name in task_modules:
        importlib.import_module(f"sparts.tasks.{name}")

def test_import_all_submodules():
    import sparts
    for _, name, ispkg in pkgutil.iter_modules(sparts.__path__, sparts.__name__ + "."):
        importlib.import_module(name)