from pytest_watcher.trigger import Trigger

def test_trigger_import_and_instantiation():
    trigger = Trigger()
    # triggered/once methods may be absent, but class should be instantiable
    assert isinstance(trigger, Trigger)