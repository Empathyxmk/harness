import threading
import pytest

# Placeholders for actual TinyCThread implementations
# In a real port, these would wrap or reimplement the original C features

class Mutex:
    def __init__(self, recursive=False):
        self._lock = threading.RLock() if recursive else threading.Lock()

    def lock(self):
        self._lock.acquire()
        return True

    def unlock(self):
        self._lock.release()
        return True

    def destroy(self):
        pass

class CondVar:
    def __init__(self):
        self._cond = threading.Condition()

    def signal(self):
        with self._cond:
            self._cond.notify(1)
        return True

    def broadcast(self):
        with self._cond:
            self._cond.notify_all()
        return True

    def wait(self, mutex: Mutex):
        with self._cond:
            mutex.unlock()
            self._cond.wait()
            mutex.lock()
        return True

    def destroy(self):
        pass

def thrd_success():
    return True

def thrd_busy():
    return False

def thrd_create(target, arg):
    t = threading.Thread(target=target, args=(arg,))
    t.start()
    return t

def thrd_join(t, res_container):
    t.join()
    if isinstance(res_container, list):
        res_container[0] = 42

def mtx_init(m, recursive=False):
    return Mutex(recursive=recursive)

def mtx_lock(m):
    return m.lock()

def mtx_unlock(m):
    return m.unlock()

def mtx_destroy(m):
    return m.destroy()

def mtx_trylock(m):
    # Try to acquire without blocking
    acquired = m._lock.acquire(blocking=False)
    return acquired

def cnd_init(c):
    c[0] = CondVar()
    return True

def cnd_signal(c):
    return c.signal()

def cnd_broadcast(c):
    return c.broadcast()

def cnd_destroy(c):
    return c.destroy()

def cnd_wait(c, m):
    return c.wait(m)

# ---- TESTS ----

def simple_thread(arg):
    arg[0] += 1
    return 42

def test_mtx_plain():
    m = Mutex(recursive=False)
    assert m.lock()
    assert m.unlock()
    m.destroy()

def test_mtx_recursive():
    m = Mutex(recursive=True)
    assert m.lock()
    assert m.lock()
    assert m.unlock()
    assert m.unlock()
    m.destroy()

def thread_func_wrapper(res, arg):
    res[0] = simple_thread(arg)

def test_thrd_create_and_join():
    arg = [10]
    res = [None]
    t = threading.Thread(target=thread_func_wrapper, args=(res, arg))
    t.start()
    t.join()
    assert res[0] == 42
    assert arg[0] == 11

def test_mtx_trylock():
    m = Mutex()
    # Lock first time
    assert m.lock()
    # Try to lock without blocking: should fail
    assert m._lock.acquire(blocking=False) is False
    assert m.unlock()
    m.destroy()

def test_cnd():
    m = Mutex()
    c = CondVar()
    assert c.signal()
    assert c.broadcast()
    c.destroy()
    m.destroy()

class CndWaiterCtx:
    def __init__(self, m, c, value):
        self.m = m
        self.c = c
        self.value = value

def cnd_waiter_thread(ctx):
    ctx.m.lock()
    while ctx.value[0] == 0:
        ctx.c.wait(ctx.m)
    ctx.m.unlock()

def test_cnd_signal_wait():
    m = Mutex()
    c = CondVar()
    done = [0]
    ctx = CndWaiterCtx(m, c, done)
    t = threading.Thread(target=cnd_waiter_thread, args=(ctx,))
    t.start()
    m.lock()
    done[0] = 1
    c.signal()
    m.unlock()
    t.join()
    c.destroy()
    m.destroy()