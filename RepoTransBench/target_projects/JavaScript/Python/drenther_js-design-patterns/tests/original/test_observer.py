import pytest

def import_observer():
    from src.Behavioral.Observer import Subject, Observer
    return Subject, Observer

@pytest.fixture
def sub_and_obs():
    Subject, Observer = import_observer()
    sub = Subject()
    obs1 = Observer(1)
    obs2 = Observer(20)
    yield sub, obs1, obs2
    # No explicit cleanup needed

def test_increment_should_work(sub_and_obs):
    sub, obs1, obs2 = sub_and_obs
    sub.subscribe(obs1)
    sub.subscribe(obs2)
    sub.fire('INC')
    assert obs1.state == 2
    assert obs2.state == 21
    sub.unsubscribe(obs1)
    sub.unsubscribe(obs2)

def test_decrement_should_work(sub_and_obs):
    sub, obs1, obs2 = sub_and_obs
    sub.subscribe(obs1)
    sub.subscribe(obs2)
    sub.fire('DEC')
    sub.fire('DEC')
    assert obs1.state == 0
    assert obs2.state == 19
    sub.unsubscribe(obs1)
    sub.unsubscribe(obs2)

def test_reset_should_work(sub_and_obs):
    sub, obs1, obs2 = sub_and_obs
    sub.subscribe(obs1)
    sub.subscribe(obs2)
    sub.fire('DEC')
    sub.fire('DEC')
    sub.fire('DEC')
    sub.fire()
    assert obs1.state == 1
    assert obs2.state == 20
    sub.unsubscribe(obs1)
    sub.unsubscribe(obs2)

def test_unsubscribe_should_work(sub_and_obs):
    sub, obs1, obs2 = sub_and_obs
    sub.subscribe(obs1)
    sub.subscribe(obs2)
    sub.unsubscribe(obs2)
    sub.fire('INC')
    assert obs1.state == 2
    assert obs2.state == 20
    sub.subscribe(obs2)
    sub.unsubscribe(obs1)
    sub.unsubscribe(obs2)