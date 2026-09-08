import time
import random
import uuid
import pytest
import pythonflow as pf
from pythonflow import pfmq

@pytest.fixture
def backend_address_public():
    return f'inproc://{uuid.uuid4().hex}_pubtest'

@pytest.fixture
def broker_public(backend_address_public):
    b = pfmq.Broker(backend_address_public)
    b.run_async()
    yield b
    b.cancel()

@pytest.fixture
def workers_public(broker_public):
    with pf.Graph() as graph:
        x = pf.placeholder('x')
        y = pf.placeholder('y')
        sleep = pf.func_op(time.sleep, pf.func_op(random.uniform, 0, .05))
        with pf.control_dependencies([sleep]):
            (x + y).set_name('s')
        pf.constant(object).set_name('not_pickleable_pub')

    _workers = []
    while len(_workers) < 5:
        worker = pfmq.Worker.from_graph(graph, broker_public.backend_address)
        worker.run_async()
        _workers.append(worker)
    yield _workers
    for worker in _workers:
        worker.cancel()

@pytest.fixture
def requests_public():
    return [{'fetches': 's', 'context': {'x': 2, 'y': 4 + i}} for i in range(25)]

def test_workers_running_public(workers_public):
    time.sleep(1)
    for worker in workers_public:
        assert worker.is_alive

def test_apply_public(broker_public, workers_public):
    request = {'fetches': 's', 'context': {'x': 3, 'y': 8}}
    result = broker_public.apply(request)
    assert result == 3 + 8

def test_apply_error_public(broker_public, workers_public):
    request = {'fetches': 's', 'context': {'x': None, 'y': 5}}
    with pytest.raises(TypeError):
        broker_public.apply(request)

def test_apply_batch_public(broker_public, workers_public):
    request = {'fetches': 's', 'contexts': [{'x': 5, 'y': 10 + i} for i in range(3)]}
    result = broker_public.apply(request)
    assert result == [5 + (10 + i) for i in range(3)]

def test_cancel_task_public():
    task = pfmq.Task([], 'inproc://missing_pub')
    task.cancel()
    task._thread.join()

def test_imap_public(broker_public, workers_public, requests_public):
    task = broker_public.imap(requests_public)
    for i, result in enumerate(task):
        assert result == 2 + (4 + i)
    task._thread.join()

def test_task_context_public(broker_public, workers_public, requests_public):
    with broker_public.imap(requests_public, max_results=2) as task:
        pass
    task._thread.join()

def test_task_context_not_started_public(broker_public, workers_public, requests_public):
    with broker_public.imap(requests_public, start=False) as task:
        assert task.is_alive
    task._thread.join()

def test_worker_timeout_public(backend_address_public):
    worker = pfmq.Worker(lambda: None, backend_address_public, timeout=.05, max_retries=2)
    start = time.time()
    worker.run()
    duration = time.time() - start
    assert duration > .1

def test_task_timeout_public(backend_address_public):
    task = pfmq.Task([0, 1, 2], backend_address_public, timeout=.05, max_retries=2)
    start = time.time()
    task.run()
    duration = time.time() - start
    assert duration > .1
    with pytest.raises(TimeoutError):
        list(task)

def test_cancel_not_running_public(broker_public):
    broker_public.cancel()
    assert not broker_public.is_alive
    broker_public.cancel()

def test_imap_not_running_public(broker_public):
    broker_public.cancel()
    with pytest.raises(RuntimeError):
        broker_public.imap([])

def test_apply_not_running_public(broker_public):
    broker_public.cancel()
    with pytest.raises(RuntimeError):
        broker_public.apply(None)

def test_not_pickleable_public(broker_public, workers_public):
    with pytest.raises(pfmq.SerializationError):
        broker_public.apply({'fetches': 'not_pickleable_pub', 'context': {}})

def test_no_context_public(broker_public, workers_public):
    with pytest.raises(KeyError):
        broker_public.apply({})