from sparts import counters
import time

def test_public_sum():
    c = counters.Sum()
    assert c() == 0.0
    c.incrementBy(3)
    assert c() == 3.0
    c.increment()
    assert c() == 4.0
    c.add(6)
    assert c() == 10.0

    # Test type conversions
    assert int(c) == 10
    assert float(c) == 10.0
    assert str(c) == '10.0'

    # Test reset API
    c.reset(5.5)
    assert float(c) == 5.5

def test_public_count():
    c = counters.Count()
    assert c() == 0
    c.add(55)
    assert c() == 1

def test_public_max():
    c = counters.Max()
    assert c() is None
    c.add(5)
    assert c() == 5
    c.add(-15)
    assert c() == 5
    c.add(15)
    assert c() == 15

def test_public_min():
    c = counters.Min()
    assert c() is None
    c.add(5)
    assert c() == 5
    c.add(-15)
    assert c() == -15
    c.add(2)
    assert c() == -15

def test_public_average():
    c = counters.Average()
    assert c() is None
    c.add(20)
    c.add(40)
    assert c() == 30.0

def test_public_callback_counter():
    l = [42.0]
    c = counters.CallbackCounter(lambda: l[0])
    assert c() == 42.0
    l[0] = 7.0
    assert c() == 7.0

def test_public_sample_names():
    c = counters.samples(name='bar', types=[counters.SampleType.SUM], windows=[50])
    c.add(10)
    assert c.getCounter('bar.sum.50') == 10

    c2 = counters.samples(types=[counters.SampleType.SUM], windows=[50])
    c2.add(3)
    assert c2.getCounter('sum.50') == 3

def test_public_samples(monkeypatch):
    c = counters.samples(
        types=[counters.SampleType.SUM, counters.SampleType.COUNT],
        windows=[10, 20])

    now = time.time()
    class FakeMock:
        pass
    f = FakeMock()
    f.return_value = now
    c._now = lambda: now

    c.add(4.0)
    c.add(6.0)

    assert c.getCounter('sum.10') == 10.0
    assert c.getCounter('sum.20') == 10.0
    assert c.getCounter('count.10') == 2
    assert c.getCounter('count.20') == 2
    assert len(c.getCounters()) == 4

    c._now = lambda: now + 5
    c.add(5.0)

    assert c.getCounter('sum.10') == 15.0
    assert c.getCounter('sum.20') == 15.0
    assert c.getCounter('count.10') == 3
    assert c.getCounter('count.20') == 3

    c._now = lambda: now + 11
    assert c.getCounter('sum.10') == 5.0
    assert c.getCounter('sum.20') == 15.0
    assert c.getCounter('count.10') == 1
    assert c.getCounter('count.20') == 3

    c._now = lambda: now + 21
    assert c.getCounter('sum.10') == 0.0
    assert c.getCounter('sum.20') == 5.0
    assert c.getCounter('count.10') == 0
    assert c.getCounter('count.20') == 1

    c._now = lambda: now + 31
    assert c.getCounter('sum.10') == 0.0
    assert c.getCounter('sum.20') == 0.0
    assert c.getCounter('count.10') == 0
    assert c.getCounter('count.20') == 0