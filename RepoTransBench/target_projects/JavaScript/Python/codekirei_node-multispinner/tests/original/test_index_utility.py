import pytest
from src.multispinner import Multispinner
from src.multispinner.constants import States

def test_success_and_error_set_spinner_state():
    m = Multispinner(['a'], {'autoStart': False})
    m.success('a')
    assert m.spinners['a'].state == States.success
    m.error('a')
    assert m.spinners['a'].state == States.error

def test_update_method_can_be_replaced_for_testing():
    m = Multispinner(['a'], {'autoStart': False})
    log_called = {'called': False}
    def fake_update(strval):
        log_called['called'] = True
    m.update = fake_update
    m.update('hello')
    assert log_called['called']

def test_covers_posttext_pretext_assignment_in_spinners():
    m = Multispinner({'X': 'MyText'}, {'autoStart': False, 'preText': 'PRE', 'postText': 'POST'})
    assert 'PRE' in m.spinners['X'].text
    assert 'POST' in m.spinners['X'].text