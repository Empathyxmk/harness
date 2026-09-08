import threading
import time

def thread_func_pub(arg):
    arg[0] += 2
    return 9

def test_thread_start_stop_pub():
    arg = [8]
    ret = [None]
    def tfunc():
        ret[0] = thread_func_pub(arg)
    t = threading.Thread(target=tfunc)
    t.start()
    t.join()
    assert arg[0] == 10
    assert ret[0] == 9

def test_mutex_init_destroy_lock_unlock_pub():
    lock = threading.Lock()
    for _ in range(2):
        locked = lock.acquire()
        assert locked
        lock.release()
    # Simulate destroy
    assert True

def test_cnd_signal_broadcast_wait_pub():
    cnd = threading.Condition()
    lock = threading.Lock()
    # Just broadcast (no real waiters)
    with cnd:
        cnd.notify_all()
    # destroy
    assert True

called_pub = [0]
once_lock = threading.Lock()
once_flag = [False]
def callback_once_pub():
    called_pub[0] += 2

def call_once(flag, func):
    with once_lock:
        if not flag[0]:
            func()
            flag[0] = True

def test_call_once_pub():
    called_pub[0] = 0
    call_once(once_flag, callback_once_pub)
    assert called_pub[0] == 2
    call_once(once_flag, callback_once_pub)
    assert called_pub[0] == 2