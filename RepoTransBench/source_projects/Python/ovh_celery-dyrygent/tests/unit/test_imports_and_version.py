from celery_dyrygent import VERSION
import celery_dyrygent.workflows
import celery_dyrygent.workflows.exceptions

def test_version_value():
    assert VERSION == "0.8.0"

def test_workflows_all_exports():
    from celery_dyrygent.workflows import Workflow, WorkflowException, WorkflowNode
    assert Workflow
    assert WorkflowNode
    assert WorkflowException

def test_exception_is_exception():
    from celery_dyrygent.workflows.exceptions import WorkflowException
    try:
        raise WorkflowException("msg")
    except WorkflowException as e:
        assert str(e) == "msg"