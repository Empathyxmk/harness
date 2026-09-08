import threading
import pytest
from switchml.barrier import Barrier

def test_barrier_all_threads_sync():
    barrier = Barrier(3)
    passed = []
    def thread_func():
        barrier.Wait()
        passed.append(1)
    t1 = threading.Thread(target=thread_func)
    t2 = threading.Thread(target=thread_func)
    t1.start()
    t2.start()
    barrier.Wait()
    t1.join()
    t2.join()
    assert len(passed) == 2

def test_barrier_multiple_rounds():
    barrier = Barrier(2)
    rounds = []
    def thread_func():
        for _ in range(5):
            barrier.Wait()
            rounds.append(1)
    t = threading.Thread(target=thread_func)
    t.start()
    for _ in range(5):
        barrier.Wait()
    t.join()
    assert len(rounds) == 5

def test_barrier_destroy_wakeups():
    barrier = Barrier(2)
    caught = []
    def thread_func():
        try:
            barrier.Wait()
        except Exception:
            caught.append(1)
    t = threading.Thread(target=thread_func)
    t.start()
    barrier.Destroy()
    t.join()
    assert len(caught) == 1

def test_barrier_wait_after_destroy_throws():
    barrier = Barrier(1)
    barrier.Destroy()
    with pytest.raises(RuntimeError):
        barrier.Wait()