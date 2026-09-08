import pytest
from celery_dyrygent.workflows import Workflow, WorkflowNode, WorkflowException

def test_workflow_can_be_initialized_public():
    # Use a different definition dict than existing
    definition = {'name': 'public_wf', 'nodes': [{'id': 100, 'kind': 'start'}]}
    wf = Workflow(definition)
    assert wf.definition['name'] == 'public_wf'

def test_workflownode_attribute_assignment_public():
    # Use different attributes in node definition
    node_def = {'id': 57, 'kind': 'special', 'attr': 'xyz'}
    node = WorkflowNode(node_def)
    assert node.kind == 'special'
    assert node.attr == 'xyz'
    assert node.id == 57

def test_workflow_exception_message_public():
    try:
        raise WorkflowException("public workflow error")
    except WorkflowException as e:
        assert 'public' in str(e)

def test_workflow_from_dict_and_to_dict_public(mocker):
    # Use different values for the workflow dict
    wf_dict = {'name': 'other', 'nodes': []}
    m = mocker.patch("celery_dyrygent.workflows.WorkflowNode")
    wf = Workflow.from_dict(wf_dict)
    d = wf.to_dict()
    assert d['name'] == 'other'

def test_workflow_tick_and_state_public(mocker):
    # Mocking internals to test tick and state
    wf = Workflow({'name': 'ticktest', 'nodes': []})
    wf._state = 'waiting'
    assert wf.state == 'waiting'
    wf._state = 'running'
    assert wf.state == 'running'

def test_workflownode_repr_public():
    # Test that __repr__ yields informative string (with different data)
    node = WorkflowNode({'id': 30, 'kind': 'action', 'label': 'LabelX'})
    rep = repr(node)
    assert "action" in rep or "LabelX" in rep