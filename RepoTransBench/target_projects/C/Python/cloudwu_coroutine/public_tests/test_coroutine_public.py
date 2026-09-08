import pytest

# --- Coroutine stub/mock definitions (duplicate so public tests run stand-alone too) ---
COROUTINE_READY = 0
COROUTINE_SUSPEND = 1
COROUTINE_DEAD = 2

class CoroutineDeadException(Exception):
    pass

class Schedule:
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
        try:
            finished = func(self, self.udata[cid])
            if finished:
                self.status[cid] = COROUTINE_DEAD
        except CoroutineDeadException:
            self.status[cid] = COROUTINE_DEAD
        except StopIteration:
            self.status[cid] = COROUTINE_DEAD
        finally:
            if self.status[cid] != COROUTINE_DEAD:
                if self.status[cid] == COROUTINE_READY:
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
    raise CoroutineDeadException("Yield called")

# --- Translated public tests ---

class TestArgPub:
    def __init__(self, counter):
        self.counter = counter

def add_two_func(S, ud):
    arg = ud
    arg.counter += 2
    coroutine_yield(S)
    arg.counter += 3

def dead_func_public(S, ud):
    pass

def running_func_public(S, ud):
    id_ = coroutine_running(S)
    assert id_ >= 0
    coroutine_yield(S)

def test_basic_lifecycle_public():
    S = coroutine_open()
    arg = TestArgPub(5)
    co = coroutine_new(S, add_two_func, arg)
    assert co >= 0

    assert coroutine_status(S, co) == COROUTINE_READY

    # Resume first (add 2, yields)
    try:
        coroutine_resume(S, co)
    except CoroutineDeadException:
        pass
    assert arg.counter == 7
    assert coroutine_status(S, co) == COROUTINE_SUSPEND

    # Resume again (add 3, finish)
    try:
        coroutine_resume(S, co)
    except CoroutineDeadException:
        pass
    assert arg.counter == 10
    assert coroutine_status(S, co) == COROUTINE_DEAD

    coroutine_close(S)

def test_multiple_coroutines_public():
    S = coroutine_open()
    a1 = TestArgPub(5)
    a2 = TestArgPub(20)
    co1 = coroutine_new(S, add_two_func, a1)
    co2 = coroutine_new(S, add_two_func, a2)

    try:
        coroutine_resume(S, co1)  # a1.counter == 7
    except CoroutineDeadException:
        pass
    try:
        coroutine_resume(S, co2)  # a2.counter == 22
    except CoroutineDeadException:
        pass
    try:
        coroutine_resume(S, co1)  # a1.counter == 10
    except CoroutineDeadException:
        pass
    try:
        coroutine_resume(S, co2)  # a2.counter == 25
    except CoroutineDeadException:
        pass

    assert a1.counter == 10 and a2.counter == 25
    assert coroutine_status(S, co1) == COROUTINE_DEAD
    assert coroutine_status(S, co2) == COROUTINE_DEAD
    coroutine_close(S)

def test_coroutine_dead_status_public():
    S = coroutine_open()
    co = coroutine_new(S, dead_func_public, None)
    assert coroutine_status(S, co) == COROUTINE_READY
    coroutine_resume(S, co)
    assert coroutine_status(S, co) == COROUTINE_DEAD

    # double resume, safe
    coroutine_resume(S, co)
    coroutine_close(S)

def test_coroutine_running_public():
    S = coroutine_open()
    co = coroutine_new(S, running_func_public, None)
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

def test_coroutine_new_capacity_public():
    S = coroutine_open()
    spawn = 20
    ids = []
    for _ in range(spawn):
        id_ = coroutine_new(S, dead_func_public, None)
        assert id_ >= 0
        ids.append(id_)
    for id_ in ids:
        coroutine_resume(S, id_)
    coroutine_close(S)