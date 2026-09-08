import threading
import time

def test_run_immediately():
    called = []
    def set_bool():
        called.append(True)
    t = threading.Thread(target=set_bool)
    t.start()
    t.join(timeout=0.1)
    assert called

def test_run_many():
    results = []
    lock = threading.Lock()
    def cb(val):
        with lock:
            results.append(val)
    threads = []
    for id in range(1, 5):
        t = threading.Thread(target=cb, args=(id,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join(timeout=0.2)
    assert results == [1,2,3,4]

def test_start_thread():
    state = {"val": 0, "num_running": 3}
    lock = threading.Lock()
    def body():
        with lock:
            state["val"] += 1
            state["num_running"] -= 1
    threads = []
    for _ in range(3):
        t = threading.Thread(target=body)
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=0.2)
    assert state["val"] == 3
    assert state["num_running"] == 0