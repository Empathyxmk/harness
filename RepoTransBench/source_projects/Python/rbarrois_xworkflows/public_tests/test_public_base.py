import pytest
from xworkflows import base

def test_public_workflow_states_and_transitions():
    class AltWorkflow(base.Workflow):
        states = (
            ('start', 'Start'),
            ('mid', 'Middle'),
            ('end', 'End'),
        )
        transitions = (
            ('go_mid', 'start', 'mid'),
            ('finish', 'mid', 'end'),
            ('reset', 'end', 'start'),
        )
        initial_state = 'start'

    wf = AltWorkflow
    assert len(wf.states) == 3
    assert wf.states['start'].title == 'Start'
    assert wf.transitions['go_mid'].source[0].name == 'start'
    assert wf.transitions['finish'].target.name == 'end'
    # initial state
    assert wf.initial_state == wf.states['start']

def test_public_workflow_invalid_state_transition():
    class MiniWorkflow(base.Workflow):
        states = (
            ('a', 'Alpha'),
            ('b', 'Beta')
        )
        transitions = (
            ('a_to_b', 'a', 'b'),
        )
        initial_state = 'a'

    # Try referencing invalid state in transition
    def bad_wf():
        class BadWorkflow(base.Workflow):
            states = (
                ('x', 'Ex'),
                ('y', 'Why'),
            )
            transitions = (
                ('invalid', 'x', 'z'),
            )
            initial_state = 'x'
    with pytest.raises(KeyError):
        bad_wf()