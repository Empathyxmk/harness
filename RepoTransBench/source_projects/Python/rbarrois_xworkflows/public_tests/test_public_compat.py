from xworkflows import base

def test_public_string_type_is_str():
    # Compatibility: base.Workflow class's __name__ is str
    assert isinstance(base.Workflow.__name__, str)

def test_public_base_workflow_has_states():
    # The Workflow class should have a states attribute or subscriptable
    # We'll create a custom workflow.
    class AltCompWorkflow(base.Workflow):
        states = (('alpha', 'Alpha'), ('beta', 'Beta'))
        transitions = (('ab', 'alpha', 'beta'),)
        initial_state = 'alpha'
    workflow = AltCompWorkflow
    assert 'alpha' in workflow.states
    assert workflow.states['beta'].title == 'Beta'