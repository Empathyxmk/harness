def test_get_resolution():
    class SimplePauseDetector:
        def __init__(self, resolution_millis, thread_count):
            self.resolution_millis = resolution_millis
            self.thread_count = thread_count
        def get_resolution_millis(self):
            return self.resolution_millis
    detector = SimplePauseDetector(10, 4)
    assert detector.get_resolution_millis() == 10

def test_set_verbose():
    class SimplePauseDetector:
        def __init__(self, resolution_millis, thread_count):
            self.resolution_millis = resolution_millis
            self.thread_count = thread_count
            self._verbose = False
        def set_verbose(self, value):
            self._verbose = value
        def is_verbose(self):
            return self._verbose
    detector = SimplePauseDetector(3, 2)
    detector.set_verbose(True)
    assert detector.is_verbose()
    detector.set_verbose(False)
    assert not detector.is_verbose()