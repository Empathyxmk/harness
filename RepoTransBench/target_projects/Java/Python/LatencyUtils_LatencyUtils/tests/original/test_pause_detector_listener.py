class PauseDetectorListener:
    def handle_pause_event(self, pause_length, pause_end_time):
        pass

class TestListener(PauseDetectorListener):
    def __init__(self):
        self.received_length = -1
        self.received_time = -1
    def handle_pause_event(self, pause_length, pause_end_time):
        self.received_length = pause_length
        self.received_time = pause_end_time

def test_pause_event_is_handled_correctly():
    listener = TestListener()
    listener.handle_pause_event(555, 999)
    assert listener.received_length == 555
    assert listener.received_time == 999