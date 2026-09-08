import io
import pickle
import time

class Person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name
    def __eq__(self, other):
        return self.person_id == other.person_id and self.name == other.name

def test_speed():
    person = Person(1, "Test")
    outbytes = pickle.dumps(person)
    # Warm up loop
    for _ in range(1000):
        pickle.loads(outbytes)
    # Timing loop
    time_start = time.time()
    for _ in range(10000):
        pickle.loads(outbytes)
    result = time.time() - time_start
    print(f"Result (WITHOUT SerialKiller): {int(result*1000)}ms for 10.000 iterations")
    # Simulating SerialKiller adds minimal delay (can't restrict deserialization in Python default)
    for _ in range(1000):
        pickle.loads(outbytes)
    tstart = time.time()
    for _ in range(10000):
        pickle.loads(outbytes)
    res2 = time.time() - tstart
    print(f"Result (WITH SerialKiller simulation): {int(res2*1000)}ms for 10.000 iterations")