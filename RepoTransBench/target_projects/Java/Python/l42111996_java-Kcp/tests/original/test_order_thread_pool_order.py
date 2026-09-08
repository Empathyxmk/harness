import threading, time

class OrderedThreadSession:
    def __init__(self):
        self._id = 0
    def getId(self):
        return self._id
    def setId(self, val):
        self._id = val

def test_ordered_thread_pool_invariants():
    sessions = [OrderedThreadSession() for _ in range(4)]
    total = 0
    lock = threading.Lock()
    def producer(session, count):
        nonlocal total
        for _ in range(count):
            with lock:
                session.setId(session.getId()+1)
                total += 1
    threads = []
    for i in range(4):
        t = threading.Thread(target=producer, args=(sessions[i], 1000))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    assert sum([s.getId() for s in sessions]) == 4000
    assert total == 4000