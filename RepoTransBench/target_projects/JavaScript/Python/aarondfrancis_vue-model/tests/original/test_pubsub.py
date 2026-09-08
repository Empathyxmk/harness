import pytest

from src.PubSub import PubSub

def test_can_subscribe_and_publish():
    ps = PubSub()
    val = {"wrapped": None}
    def handler(v):
        val["wrapped"] = v
    ps.subscribe('a', handler)
    ps.publish('a', 123)
    assert val["wrapped"] == 123

def test_multiple_subscribers_work():
    ps = PubSub()
    v1 = {"value": 0}
    v2 = {"value": 0}
    def listener1(v):
        v1["value"] = v
    def listener2(v):
        v2["value"] = v * 2
    ps.subscribe('z', listener1)
    ps.subscribe('z', listener2)
    ps.publish('z', 4)
    assert v1["value"] == 4
    assert v2["value"] == 8

def test_unsubscribe_works():
    ps = PubSub()
    called = {"count": 0}
    def fn(x):
        called["count"] += x
    ps.subscribe('x', fn)
    ps.unsubscribe('x', fn)
    ps.publish('x', 5)
    assert called["count"] == 0

def test_publishing_to_no_subscribers_does_nothing():
    ps = PubSub()
    # Should not raise
    ps.publish('never', 77)