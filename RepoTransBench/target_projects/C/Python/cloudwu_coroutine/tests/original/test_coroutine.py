import pytest

# --- Coroutine stub/mock definitions ---

# Status codes
COROUTINE_READY = 0
COROUTINE_SUSPEND = 1
COROUTINE_DEAD = 2

class CoroutineDeadException(Exception):
    pass

class Schedule:
    """ Minimal coroutine scheduler mock for test translation """
    def __init__(self):
        self.coroutines = {}
        self.status = {}
        self.udata = {}
        self.runnings = {}
        self.next_id = 0
        self.running_id = -1

    def new(self, func, ud):
        cid = self.next_id
        self.coroutines[cid] = func
        self.status[cid] = COROUTINE_READY
        self.udata[cid] = ud
        self.next_id += 1
        return cid

    def status_of(self, cid):
        return self.status.get(cid, COROUTINE_DEAD)

    def resume(self, cid):
        if self.status[cid] == COROUTINE_DEAD:
            return
        self.running_id = cid
        func = self.coroutines[cid]
        # Run step
        try:
            finished = func(self, self.udata[cid])
            if finished:
                self.status[cid] = COROUTINE_DEAD
        except CoroutineDeadException:
            self.status[cid] = COROUTINE_DEAD
        except StopIteration:
            # simulate 'return' in func
            self.status[cid] = COROUTINE_DEAD
        finally:
            if self.status[cid] != COROUTINE_DEAD:
                if self.status[cid] == COROUTINE_READY:
                    # after first run, if yields, it's suspended
                    self.status[cid] = COROUTINE_SUSPEND
            self.running_id = -1

    def running(self):
        return self.running_id

    def close(self):
        self.coroutines.clear()
        self.status.clear()
        self.udata.clear()
        self.runnings.clear()
        self.next_id = 0
        self.running_id = -1

# Test helpers to resemble C interface
def coroutine_open():
    return Schedule()

def coroutine_close(S):
    S.close()

def coroutine_new(S, func, ud):
    return S.new(func, ud)

def coroutine_resume(S, cid):
    S.resume(cid)

def coroutine_status(S, cid):
    return S.status_of(cid)

def coroutine_running(S):
    return S.running()

def coroutine_yield(S):
    # Raises to unwind stack, as Python has no true yield between non-generators
    # We'll "simulate" by raising and catching in the Schedule.
    raise CoroutineDeadException("Yield called")  # Actually, just a place-holder for yield



# ---- Translated tests (originals) ----

class TestArg:
    def __init__(self, counter):
        self.counter = counter

def increment_func(S, ud):
    arg = ud
    arg.counter += 1
    coroutine_yield(S)
    arg.counter += 1

def death_func(S, ud):
    pass  # Dies immediately

def running_func(S, ud):
    id_ = coroutine_running(S)
    assert id_ >= 0
    coroutine_yield(S)

def test_basic_lifecycle():
    S = coroutine_open()
    arg = TestArg(0)
    co = coroutine_new(S, increment_func, arg)
    assert co >= 0

    # Should be ready initially
    assert coroutine_status(S, co) == COROUTINE_READY

    # Run first time (increments, yield)
    try:
        coroutine_resume(S, co)
    except CoroutineDeadException:
        pass
    assert arg.counter == 1
    assert coroutine_status(S, co) == COROUTINE_SUSPEND

    # Resume (increments again, done)
    try:
        coroutine_resume(S, co)
    except CoroutineDeadException:
        pass
    assert arg.counter == 2
    assert coroutine_status(S, co) == COROUTINE_DEAD

    coroutine_close(S)

def test_multiple_coroutines():
    S = coroutine_open()
    a1 = TestArg(0)
    a2 = TestArg(10)
    co1 = coroutine_new(S, increment_func, a1)
    co2 = coroutine_new(S, increment_func, a2)

    # interleave properly
    try:
        coroutine_resume(S, co1)  # a1.counter == 1
    except CoroutineDeadException:
        pass
    try:
        coroutine_resume(S, co2)  # a2.counter == 11
    except CoroutineDeadException:
        pass
    try:
        coroutine_resume(S, co1)  # a1.counter == 2
    except CoroutineDeadException:
        pass
    try:
        coroutine_resume(S, co2)  # a2.counter == 12
    except CoroutineDeadException:
        pass

    assert a1.counter == 2 and a2.counter == 12
    assert coroutine_status(S, co1) == COROUTINE_DEAD
    assert coroutine_status(S, co2) == COROUTINE_DEAD
    coroutine_close(S)

def test_coroutine_dead_status():
    S = coroutine_open()
    co = coroutine_new(S, death_func, None)
    assert coroutine_status(S, co) == COROUTINE_READY
    coroutine_resume(S, co)
    assert coroutine_status(S, co) == COROUTINE_DEAD

    # Check double resume does nothing / safe
    coroutine_resume(S, co)
    coroutine_close(S)

def test_coroutine_running():
    S = coroutine_open()
    co = coroutine_new(S, running_func, None)
    assert coroutine_running(S) == -1
    try:
        coroutine_resume(S, co)
    except CoroutineDeadException:
        pass
    assert coroutine_running(S) == -1
    try:
        coroutine_resume(S, co)
    except CoroutineDeadException:
        pass
    assert coroutine_running(S) == -1
    coroutine_close(S)

def test_coroutine_new_capacity():
    S = coroutine_open()
    spawn = 18
    ids = []
    for _ in range(spawn):
        id_ = coroutine_new(S, death_func, None)
        assert id_ >= 0
        ids.append(id_)
    for id_ in ids:
        coroutine_resume(S, id_)
    coroutine_close(S)

# The C main() test driver is omitted, as pytest will discover and run all test_* functions.