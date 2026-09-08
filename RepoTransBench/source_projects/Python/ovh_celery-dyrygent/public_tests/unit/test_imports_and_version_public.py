from celery_dyrygent import VERSION
import celery_dyrygent.workflows
import celery_dyrygent.workflows.exceptions

def test_version_value_public():
    # Use the version string in a different way for comparison
    assert VERSION.split(".") == ["0", "8", "0"]

def test_workflows_all_exports_public():
    # Check for types instead of direct reference
    from celery_dyrygent.workflows import Workflow, WorkflowException, WorkflowNode
    assert isinstance(Workflow.__name__, str)
    assert isinstance(WorkflowNode.__name__, str)
    assert issubclass(WorkflowException, Exception)

def test_exception_is_exception_public():
    from celery_dyrygent.workflows.exceptions import WorkflowException
    try:
        raise WorkflowException("different message")
    except WorkflowException as e:
        assert "different" in str(e)