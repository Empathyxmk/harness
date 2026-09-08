import pytest
from src.multispinner import Multispinner
from src.multispinner.constants import States

def test_success_and_error_set_spinner_state_different_spinner():
    m = Multispinner(['z'], {'autoStart': False})
    m.success('z')
    assert m.spinners['z'].state == States.success
    m.error('z')
    assert m.spinners['z'].state == States.error

def test_update_method_can_be_replaced_for_testing_public_different_function():
    m = Multispinner(['pub'], {'autoStart': False})
    called_arg = {'arg': None}
    def fake_update(strval):
        called_arg['arg'] = strval
    m.update = fake_update
    m.update('test public')
    assert called_arg['arg'] == 'test public'

def test_covers_posttext_pretext_assignment_in_spinners_different_key_text_prefix_suffix():
    m = Multispinner({'Y': 'OtherText'}, {'autoStart': False, 'preText': '<<', 'postText': '>>'})
    assert '<<' in m.spinners['Y'].text
    assert '>>' in m.spinners['Y'].text