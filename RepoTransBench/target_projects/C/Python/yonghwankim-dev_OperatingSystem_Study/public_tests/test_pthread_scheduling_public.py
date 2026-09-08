import threading
import time

def public_test_thread_func(arg):
    # Simulating a thread-modifying a value via reference
    arg[0] += 2
    # Simulate 20ms work
    time.sleep(0.02)

def test_scheduling_single_thread_public():
    result = [5]
    t1 = threading.Thread(target=public_test_thread_func, args=(result,))
    t1.start()
    t1.join()
    assert result[0] == 7

def test_scheduling_multi_thread_public():
    result1 = [12]
    result2 = [21]
    t1 = threading.Thread(target=public_test_thread_func, args=(result1,))
    t2 = threading.Thread(target=public_test_thread_func, args=(result2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert result1[0] == 14
    assert result2[0] == 23