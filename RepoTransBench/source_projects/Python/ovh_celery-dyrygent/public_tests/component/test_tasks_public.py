import pytest

from celery_dyrygent.tasks import workflow_processor

def test_workflow_processor_with_different_ids(mocker):
    # Setup a different id, test different edge
    task_obj = mocker.Mock()
    task_obj.request.id = "feed-face"
    task_obj.request.retries = 4

    wf = mocker.Mock()
    wf.tick.return_value = False
    wf.to_dict.return_value = {}
    wf.get_retry_countdown.return_value = 123
    wf.workflow_options = {}
    from celery_dyrygent.workflows import Workflow
    mocker.patch.object(Workflow, "from_dict", return_value=wf)

    # Different dict provided
    workflow_processor(task_obj, {"foo": "bar"})
    task_obj.retry.assert_not_called()

    # Now tick True triggers retry (simulate a different countdown)
    wf.tick.return_value = True
    wf.get_retry_countdown.return_value = 10
    workflow_processor(task_obj, {"foo": "bar"})
    task_obj.retry.assert_called_once_with(
        kwargs=dict(workflow_dict={}),
        countdown=10
    )
    assert task_obj.request.retries == 3