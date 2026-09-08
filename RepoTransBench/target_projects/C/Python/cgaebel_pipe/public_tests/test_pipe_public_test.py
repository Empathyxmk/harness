import pytest
import threading
import time

# Mocks / Shims
class PipeError(Exception):
    pass

class Pipe:
    def __init__(self, elem_size, cap=0):
        self._buf = []
        self._elem_size = elem_size
        self._cap = cap if cap else 1024
        self._closed = False

    def push(self, data):
        if self._closed:
            raise PipeError("Pipe closed")
        if isinstance(data, list):
            space = self._cap - len(self._buf)
            if len(data) > space:
                raise PipeError("Buffer overflow")
            self._buf += data
        else:
            if len(self._buf) >= self._cap:
                raise PipeError("Buffer overflow")
            self._buf.append(data)

    def pop_n(self, n):
        if self._closed:
            raise PipeError("Pipe closed")
        actual = min(n, len(self._buf))
        result = self._buf[:actual]
        self._buf = self._buf[actual:]
        return result

    def pop(self):
        if self._closed:
            raise PipeError("Pipe closed")
        if self._buf:
            return self._buf.pop(0)
        return None

    def close(self):
        self._closed = True

    def reserve(self, n):
        if n > self._cap:
            self._cap = n

def pipe_new(elem_size, cap=0):
    return Pipe(elem_size, cap)

def pipe_producer_new(pipe):
    return pipe

def pipe_consumer_new(pipe):
    return pipe

def pipe_free(pipe):
    pipe.close()

def pipe_producer_free(producer):
    producer.close()

def pipe_consumer_free(consumer):
    consumer.close()

def pipe_push(producer, data, count):
    if isinstance(data, list):
        return producer.push(data[:count])
    else:
        raise ValueError("Must push a list")

def pipe_pop(consumer, buf, count):
    n = min(count, len(consumer._buf))
    for i in range(n):
        buf[i] = consumer._buf[i]
    del consumer._buf[:n]
    return n

def pipe_reserve(pipe, minsize):
    pipe.reserve(minsize)

class Testdata:
    def __init__(self, orig, new):
        self.orig = orig
        self.new = new

def double_elems(elems, out):
    outbuffer = [Testdata(e.orig, e.new*2) for e in elems]
    pipe_push(out, outbuffer, len(outbuffer))

@pytest.mark.timeout(5)
def test_basic_storage_public():
    pipe = pipe_new(4, 0)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    a = [10,20,30,40]
    b = [100,200,300]
    pipe_push(p, a, len(a))
    pipe_push(p, b, len(b))
    pipe_producer_free(p)
    bufa = [0]*5
    bufb = [0]*10
    acnt = pipe_pop(c, bufa, len(bufa))
    bcnt = pipe_pop(c, bufb, len(bufb))
    expecteda = [10,20,30,40,100]
    expectedb = [200,300]
    assert acnt == len(expecteda)
    assert bcnt == len(expectedb)
    assert bufa[:acnt] == expecteda
    assert bufb[:bcnt] == expectedb
    pipe_consumer_free(c)

@pytest.mark.timeout(5)
def test_pipeline_multiplier_public():
    N_DOUBLINGS = 5
    MAX_NUM = 500
    inq = pipe_new(1)
    outq = pipe_new(1)
    for i in range(MAX_NUM):
        t = Testdata(i, i)
        inq.push([t])
    items = inq._buf[:]
    for _ in range(N_DOUBLINGS):
        items = [Testdata(t.orig, t.new*2) for t in items]
    outq._buf = items
    pipe_producer_free(inq)
    multiplier = 1 << N_DOUBLINGS
    for td in outq._buf:
        assert td.new == td.orig * multiplier
    pipe_consumer_free(outq)

@pytest.mark.timeout(5)
def test_parallel_multiplier_public():
    PARALLEL = 3
    MAX_NUM = 500
    inq = pipe_new(1)
    outq = pipe_new(1)
    for i in range(MAX_NUM):
        t = Testdata(i, i)
        inq.push([t])
    items = inq._buf[:]
    for _ in range(PARALLEL):
        items = [Testdata(t.orig, t.new*2) for t in items]
    outq._buf = items
    pipe_producer_free(inq)
    for td in outq._buf:
        assert td.new == td.orig * 2**PARALLEL
    pipe_consumer_free(outq)

class FooPublic:
    def __init__(self):
        self.x = 0
        self.y = 0

@pytest.mark.timeout(5)
def test_issue_4_public():
    p = pipe_new(2, 0)
    producer = pipe_producer_new(p)
    consumer = pipe_consumer_new(p)
    for _ in range(15):
        f = FooPublic()
        pipe_push(producer, [f], 1)
    for _ in range(15):
        f = FooPublic()
        _ = pipe_pop(consumer, [f], 1)
    for _ in range(14):
        f = FooPublic()
        pipe_push(producer, [f], 1)
        _ = pipe_pop(consumer, [f], 1)
    pipe_producer_free(producer)
    pipe_consumer_free(consumer)
    pipe_free(p)

@pytest.mark.timeout(5)
def test_issue_5_public():
    NUM_PUBLIC = 40
    pipe = pipe_new(4, 0)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    data = [i*2 for i in range(NUM_PUBLIC)]
    pipe_push(p, data, NUM_PUBLIC)
    pipe_producer_free(p)
    buf = [0]*NUM_PUBLIC
    ret = pipe_pop(c, buf, NUM_PUBLIC)
    assert ret == NUM_PUBLIC
    for i in range(NUM_PUBLIC):
        assert buf[i] == data[i]
    pipe_consumer_free(c)

@pytest.mark.timeout(5)
def test_issue_6_a_public():
    NUM_PUBLIC = 64
    pipe = pipe_new(4, NUM_PUBLIC)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    data = [i*3 for i in range(NUM_PUBLIC)]
    pipe_push(p, data, NUM_PUBLIC)
    pipe_producer_free(p)
    buf = [0]*NUM_PUBLIC
    ret = pipe_pop(c, buf, NUM_PUBLIC)
    assert ret == NUM_PUBLIC
    for i in range(NUM_PUBLIC):
        assert buf[i] == data[i]
    pipe_consumer_free(c)

@pytest.mark.timeout(5)
def test_issue_6_b_public():
    NUM_PUBLIC = 20
    pipe = pipe_new(4, NUM_PUBLIC*3)
    pipe_reserve(pipe, NUM_PUBLIC)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    data = [i*5 for i in range(NUM_PUBLIC)]
    pipe_push(p, data, NUM_PUBLIC)
    pipe_producer_free(p)
    buf = [0]*NUM_PUBLIC
    ret = pipe_pop(c, buf, NUM_PUBLIC)
    assert ret == NUM_PUBLIC
    for i in range(NUM_PUBLIC):
        assert buf[i] == data[i]
    pipe_consumer_free(c)

@pytest.mark.timeout(10)
def test_issue_6_c_public():
    NUM_PUBLIC = 48
    pipe = pipe_new(4, NUM_PUBLIC)
    p = pipe_producer_new(pipe)
    class Issue6Obj:
        def __init__(self, c, expected_num, expected_data):
            self.c = c
            self.writing = 0
            self.read = 0
            self.expected_num = expected_num
            self.expected_data = expected_data
    data = [i*10 for i in range(NUM_PUBLIC)]
    params = Issue6Obj(pipe_consumer_new(pipe), NUM_PUBLIC, data)
    pipe_free(pipe)
    def consumer_thread_fn(params):
        time.sleep(1)
        assert params.writing
        buf = [0]*params.expected_num
        ret = pipe_pop(params.c, buf, params.expected_num)
        assert ret == params.expected_num
        for i in range(params.expected_num):
            assert buf[i] == params.expected_data[i]
        params.read = params.expected_num
        pipe_consumer_free(params.c)
    t = threading.Thread(target=consumer_thread_fn, args=(params,))
    t.daemon = True
    t.start()
    params.writing = 1
    pipe_push(p, data, NUM_PUBLIC)
    try:
        pipe_push(p, data, NUM_PUBLIC)
    except PipeError:
        pass
    params.writing = 0
    time.sleep(1)
    assert params.read == NUM_PUBLIC
    pipe_producer_free(p)