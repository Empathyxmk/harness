import threading, time

class OrderedThreadSession:
    def __init__(self):
        self._id = 0
    def getId(self):
        return self._id
    def setId(self, val):
        self._id = val

def test_thread_loop_counter_consistency():
    session1 = OrderedThreadSession()
    session2 = OrderedThreadSession()
    counter = {"product": 0, "total": 0}
    lock = threading.Lock()
    def producer(session, count):
        for _ in range(count):
            with lock:
                session.setId(session.getId() + 1)
                counter["product"] += 1
    def consumer(session, count):
        for _ in range(count):
            with lock:
                counter["total"] += 1
    threads = []
    for _ in range(2):
        t = threading.Thread(target=producer, args=(session1, 500))
        t.start()
        threads.append(t)
    for _ in range(2):
        t = threading.Thread(target=producer, args=(session2, 500))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    assert counter["product"] == 2000
    # simulate consumer
    consumer(session1, 1000)
    consumer(session2, 1000)
    assert counter["total"] == 2000