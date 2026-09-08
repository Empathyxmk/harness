from pytest_watcher.trigger import Trigger

def test_trigger_toggle_and_str():
    trig = Trigger()
    trig.toggle()
    assert trig.is_running is not None
    assert isinstance(str(trig), str)

def test_trigger_pause_resume():
    trig = Trigger()
    trig.pause()
    assert trig.is_running is False
    trig.resume()
    assert trig.is_running is True