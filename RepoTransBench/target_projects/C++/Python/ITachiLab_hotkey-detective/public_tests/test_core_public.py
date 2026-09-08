from src.hotkey_detective.core import Core

def test_core_initializes_with_alternate_state():
    core = Core()
    assert not core.is_running()

    core.start()
    assert core.is_running()

    core.stop()
    assert not core.is_running()

def test_core_handles_multiple_start_stops_alternate_sequence():
    core = Core()
    # alternate logic
    core.start()
    core.stop()
    core.start()
    assert core.is_running()
    core.stop()
    assert not core.is_running()