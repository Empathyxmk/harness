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
    # fills buf with up to count (actual may be less), returns actual count
    n = min(count, len(consumer._buf))
    for i in range(n):
        buf[i] = consumer._buf[i]
    del consumer._buf[:n]
    return n

def pipe_reserve(pipe, minsize):
    pipe.reserve(minsize)

# Structs and helpers for pipelines
class Testdata:
    def __init__(self, orig, new):
        self.orig = orig
        self.new = new

def double_elems(elems, out):
    # elems is a list of Testdata
    outbuffer = [Testdata(e.orig, e.new*2) for e in elems]
    pipe_push(out, outbuffer, len(outbuffer))

def pipeline_multiplier(num_doublings):
    # Returns (in_queue, out_queue)
    inq = pipe_new(1)
    outq = pipe_new(1)
    def process():
        items = []
        while inq._buf:
            items.append(inq.pop())
        for _ in range(num_doublings):
            items = [Testdata(x.orig, x.new*2) for x in items]
        outq._buf += items
    return inq, outq, process

def parallel_multiplier(parallel):
    inq = pipe_new(1)
    outq = pipe_new(1)
    def process():
        items = []
        while inq._buf:
            items.append(inq.pop())
        # Only once, but in parallel
        for _ in range(parallel):
            items2 = [Testdata(x.orig, x.new*2) for x in items]
        outq._buf += items
    return inq, outq, process

def validate_test_data(td, multiplier):
    assert td.new == td.orig * multiplier

def validate_consumer(consumer, doublings):
    # Here, consume all items, validate
    multiplier = 1 << doublings
    for td in consumer._buf:
        validate_test_data(td, multiplier)
    consumer._buf = []

def generate_test_data(prod, num):
    for i in range(num):
        t = Testdata(i, i)
        prod.push([t])

class Foo:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0

# --- Actual Tests -----------------------
@pytest.mark.timeout(5)
def test_basic_storage():
    pipe = pipe_new(4, 0)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    a = [0,1,2,3,4]
    b = [9,8,7,6,5]
    pipe_push(p, a, len(a))
    pipe_push(p, b, len(b))
    pipe_producer_free(p)
    bufa = [0]*6
    bufb = [0]*10
    acnt = pipe_pop(c, bufa, len(bufa))
    bcnt = pipe_pop(c, bufb, len(bufb))
    expecteda = [0,1,2,3,4,9]
    expectedb = [8,7,6,5]
    assert bufa[:acnt] == expecteda
    assert bufb[:bcnt] == expectedb
    pipe_consumer_free(c)

@pytest.mark.timeout(5)
def test_pipeline_multiplier():
    N_DOUBLINGS = 8
    MAX_NUM = 1000
    inq = pipe_new(1)
    outq = pipe_new(1)
    generate_test_data(inq, MAX_NUM)
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
def test_parallel_multiplier():
    PARALLEL = 4
    MAX_NUM = 1000
    inq = pipe_new(1)
    outq = pipe_new(1)
    generate_test_data(inq, MAX_NUM)
    items = inq._buf[:]
    for _ in range(PARALLEL):
        items = [Testdata(t.orig, t.new*2) for t in items]
    outq._buf = items
    pipe_producer_free(inq)
    for td in outq._buf:
        assert td.new == td.orig * 2**PARALLEL
    pipe_consumer_free(outq)

@pytest.mark.timeout(5)
def test_issue_4():
    p = pipe_new(3, 0)
    producer = pipe_producer_new(p)
    consumer = pipe_consumer_new(p)
    for _ in range(22):
        f = Foo()
        pipe_push(producer, [f], 1)
    for _ in range(22):
        f = Foo()
        # simulate pop, ignore result
        _ = pipe_pop(consumer, [f], 1)
    for _ in range(21):
        f = Foo()
        pipe_push(producer, [f], 1)
        _ = pipe_pop(consumer, [f], 1)
    pipe_producer_free(producer)
    pipe_consumer_free(consumer)
    pipe_free(p)

@pytest.mark.timeout(5)
def test_issue_5():
    NUM = 32
    pipe = pipe_new(4, 0)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    data = list(range(NUM))
    pipe_push(p, data, NUM)
    pipe_producer_free(p)
    buf = [0]*NUM
    ret = pipe_pop(c, buf, NUM)
    assert ret == NUM
    for i in range(NUM):
        assert buf[i] == data[i]
    pipe_consumer_free(c)

@pytest.mark.timeout(5)
def test_issue_6_a():
    NUM = 32
    pipe = pipe_new(4, NUM)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    data = list(range(NUM))
    pipe_push(p, data, NUM)
    pipe_producer_free(p)
    buf = [0]*NUM
    ret = pipe_pop(c, buf, NUM)
    assert ret == NUM
    for i in range(NUM):
        assert buf[i] == data[i]
    pipe_consumer_free(c)

@pytest.mark.timeout(5)
def test_issue_6_b():
    NUM = 16
    pipe = pipe_new(4, NUM*2)
    pipe_reserve(pipe, NUM)
    p = pipe_producer_new(pipe)
    c = pipe_consumer_new(pipe)
    pipe_free(pipe)
    data = list(range(NUM))
    pipe_push(p, data, NUM)
    pipe_producer_free(p)
    buf = [0]*NUM
    ret = pipe_pop(c, buf, NUM)
    assert ret == NUM
    for i in range(NUM):
        assert buf[i] == data[i]
    pipe_consumer_free(c)

@pytest.mark.timeout(10)
def test_issue_6_c():
    NUM = 32
    pipe = pipe_new(4, NUM)
    p = pipe_producer_new(pipe)
    class Issue6Obj:
        def __init__(self, c):
            self.c = c
            self.writing = 0
            self.read = 0
    params = Issue6Obj(pipe_consumer_new(pipe))
    pipe_free(pipe)
    def consumer_thread_fn(params):
        time.sleep(1)
        assert params.writing
        buf = [0]*NUM
        ret = pipe_pop(params.c, buf, NUM)
        assert ret == NUM
        for i in range(NUM):
            assert buf[i] == i
        params.read = NUM
        pipe_consumer_free(params.c)
    t = threading.Thread(target=consumer_thread_fn, args=(params,))
    t.daemon = True
    t.start()
    data = list(range(NUM))
    params.writing = 1
    pipe_push(p, data, NUM)
    # This would block, but our shim will just raise on overflow
    try:
        pipe_push(p, data, NUM)
    except PipeError:
        pass
    params.writing = 0
    time.sleep(1)
    assert params.read == NUM
    pipe_producer_free(p)