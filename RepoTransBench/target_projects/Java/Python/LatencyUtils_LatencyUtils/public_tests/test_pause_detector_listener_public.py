def test_listener_is_called_with_different_args():
    was_called = [False]
    class Listener:
        def handle_pause_event(self, pause_length, pause_end_time):
            was_called[0] = (pause_length == 777 and pause_end_time == 5555)
    listener = Listener()
    listeners = [listener]
    for l in listeners:
        l.handle_pause_event(777, 5555)
    assert was_called[0]