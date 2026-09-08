import threading
import time

def api_public_thread_func(sum_arg):
    time.sleep(0.009) # 9ms
    sum_arg[0] += 5
    return 42

def test_api_public_thread_func():
    sum_val = [33]
    ret_val = [None]
    def thread_wrapper():
        ret_val[0] = api_public_thread_func(sum_val)
    t = threading.Thread(target=thread_wrapper)
    t.start()
    t.join()
    assert sum_val[0] == 38
    assert ret_val[0] == 42

def test_thrd_yield():
    # Should always succeed; in Python, time.sleep(0) yields
    time.sleep(0)
    assert True

def test_thrd_current():
    self = threading.current_thread()
    assert self is not None