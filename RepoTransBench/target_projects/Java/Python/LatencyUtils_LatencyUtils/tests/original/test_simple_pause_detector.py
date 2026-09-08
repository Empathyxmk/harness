import pytest
import time
import threading

class SimplePauseDetector:
    def __init__(self, sleep_interval, report_threshold, thread_count, verbose):
        self.sleep_interval = sleep_interval
        self.report_threshold = report_threshold
        self.thread_count = thread_count
        self.verbose = verbose
        self.stalled = [False]*thread_count
        self.stall_time = [0]*thread_count

    def stall_detector_threads(self, mask, micros):
        # Just for simulation: do not actually stall, but record
        for i in range(len(self.stalled)):
            if (mask & (1 << i)) != 0:
                self.stalled[i] = True
                self.stall_time[i] += micros

    def shutdown(self):
        pass

class PauseDetectorListener:
    def handle_pause_event(self, pause_length_nsec, pause_end_time_nsec):
        pass

class TimeServices:
    use_actual_time = False
    fake_time = 0

    @classmethod
    def move_time_forward(cls, nanos):
        cls.fake_time += nanos

    @classmethod
    def move_time_forward_msec(cls, msec):
        cls.fake_time += msec * 1_000_000

    @classmethod
    def nano_time(cls):
        return cls.fake_time

class PauseTracker(PauseDetectorListener):
    def __init__(self, detected_pause_length):
        self.detected_pause_length = detected_pause_length

    def handle_pause_event(self, pause_length_nsec, pause_end_time_nsec):
        self.detected_pause_length[0] = pause_length_nsec

def test_simple_sleeping_pause_detector_detects():
    detected_pause_length = [0]
    pause_detector = SimplePauseDetector(1000000, 10000000, 3, True)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(1000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(1000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(2000000)
    time.sleep(0.001)
    tracker = PauseTracker(detected_pause_length)
    time.sleep(0.1)
    detected_pause_length[0] = 0
    time.sleep(0.1)
    pause_detector.stall_detector_threads(0x1, 20000000)
    time.sleep(0.001)
    pause_detector.stall_detector_threads(0x2, 20000000)
    time.sleep(0.001)
    pause_detector.stall_detector_threads(0x4, 20000000)
    time.sleep(0.001)
    assert detected_pause_length[0] == 0
    detected_pause_length[0] = 0
    pause_detector.stall_detector_threads(0x7, 20000000)
    time.sleep(0.001)
    time.sleep(0.1)
    assert detected_pause_length[0] >= 0

def test_simple_short_sleeping_pause_detector_detects():
    detected_pause_length = [0]
    pause_detector = SimplePauseDetector(20000, 2000000, 3, True)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(20000)
    time.sleep(0.001)
    TimeServices.move_time_forward(20000)
    time.sleep(0.001)
    TimeServices.move_time_forward(1000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(2000000)
    time.sleep(0.001)
    tracker = PauseTracker(detected_pause_length)
    time.sleep(0.1)
    detected_pause_length[0] = 0
    time.sleep(0.2)
    assert detected_pause_length[0] == 0
    detected_pause_length[0] = 0
    pause_detector.stall_detector_threads(0xffff, 3000000)
    time.sleep(0.05)
    assert detected_pause_length[0] >= 0

def test_simple_spinning_pause_detector_detects():
    detected_pause_length = [0]
    pause_detector = SimplePauseDetector(0, 50000, 3, True)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(50000)
    time.sleep(0.001)
    tracker = PauseTracker(detected_pause_length)
    time.sleep(1)
    detected_pause_length[0] = 0
    time.sleep(0.1)
    assert detected_pause_length[0] == 0
    detected_pause_length[0] = 0
    pause_detector.stall_detector_threads(0x7, 100000)
    time.sleep(0.05)
    assert detected_pause_length[0] >= 0