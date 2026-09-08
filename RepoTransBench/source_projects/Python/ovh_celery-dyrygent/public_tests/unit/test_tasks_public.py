import mock
import pytest

from celery_dyrygent import tasks
from celery_dyrygent.workflows import Workflow

class TestTasksPublic(object):
    @pytest.fixture
    def task_obj(self):
        # Use a different id and different initial retries
        return mock.Mock(name='task',
                         request=mock.Mock(id='bead-feed', retries=2))

    @pytest.fixture
    def wf(self):
        return mock.Mock()

    @pytest.fixture
    def from_dict(self, wf):
        with mock.patch.object(Workflow, 'from_dict', return_value=wf) as mck:
            yield mck

    def test_workflow_processor_public(self, task_obj, from_dict, wf):
        wf.tick.return_value = False
        from_dict.return_value.workflow_options = {'extra': 99}  # Different test data for workflow_options
        tasks.workflow_processor(task_obj, {'x': 'y'})
        from_dict.assert_called_with({'x': 'y', 'id': task_obj.request.id})
        wf.tick.assert_called_with()
        task_obj.retry.assert_not_called()

        wf.tick.return_value = True

        # task run will decrease retries with different dict data and attributes
        tasks.workflow_processor(task_obj, {'x': 'y'})
        task_obj.retry.assert_called_with(
            kwargs=dict(workflow_dict=wf.to_dict()),
            countdown=wf.get_retry_countdown(),
        )
        # retries start at 2, should decrease to 1
        assert task_obj.request.retries == 1