import pytest

from src.PubSub import PubSub

def test_can_subscribe_and_publish_with_different_value():
    ps = PubSub()
    val = {'value': None}
    def handler(v):
        val['value'] = v
    ps.subscribe('b', handler)
    ps.publish('b', 456)
    assert val['value'] == 456

def test_multiple_subscribers_other_values():
    ps = PubSub()
    v1 = {"val": 0}
    v2 = {"val": 0}
    def sub1(v):
        v1["val"] = v
    def sub2(v):
        v2["val"] = v + 3
    ps.subscribe('y', sub1)
    ps.subscribe('y', sub2)
    ps.publish('y', 7)
    assert v1["val"] == 7
    assert v2["val"] == 10

def test_unsubscribe_works_with_another_key_value():
    ps = PubSub()
    calls = {'count': 0}
    def increment(x):
        calls['count'] -= x
    ps.subscribe('w', increment)
    ps.unsubscribe('w', increment)
    ps.publish('w', 9)
    assert calls['count'] == 0

def test_publishing_to_no_subscribers_with_different_key_value():
    ps = PubSub()
    ps.publish('nobody', 999)