import pytest
from xworkflows import base

def test_public_workflow_enabled_invalid_setting_and_implementation_conflict():
    # Use unique workflow and field names compared to the original
    class AltWorkflow(base.Workflow):
        states = (
            ('begin', "Begin"),
            ('end', "End"),
        )
        transitions = (
            ('begin_to_end', 'begin', 'end'),
        )
        initial_state = 'begin'

    class AnotherAltObj(base.WorkflowEnabled):
        progress = AltWorkflow()

    obj = AnotherAltObj()
    # Can't set to completely arbitrary State
    with pytest.raises(ValueError):
        setattr(obj, 'progress', base.State('unknown_state', 'No State'))

    # Test assigning an invalid type to workflow attribute for the instance (should raise ValueError)
    with pytest.raises(ValueError):
        setattr(obj, 'progress', 98765)  # assigning an int to a workflow-enabled attr results in ValueError