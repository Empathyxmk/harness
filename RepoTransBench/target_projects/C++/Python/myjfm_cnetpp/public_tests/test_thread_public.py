import pytest
import threading

# Simple Thread mock, just runs callable and waits
class Thread:
    def __init__(self, func):
        self.func = func
        self.t = None

    def Start(self):
        self.t = threading.Thread(target=self.func)
        self.t.start()

    def Join(self):
        if self.t:
            self.t.join()

def test_start_and_join():
    finished = {"value": False}
    def mark_finished():
        finished["value"] = True
    th = Thread(mark_finished)
    th.Start()
    th.Join()
    assert finished["value"]