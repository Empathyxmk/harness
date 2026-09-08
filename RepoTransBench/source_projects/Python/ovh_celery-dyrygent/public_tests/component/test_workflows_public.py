import pytest

from celery_dyrygent.workflows.workflow import WorkflowSignalMixin

def test_connect_and_emit_public(monkeypatch):
    class MyWF(WorkflowSignalMixin):
        hooks = {'on_custom': []}

    called = []

    @MyWF.connect('on_custom')
    def handler(wf, payload):
        called.append(payload)

    w = MyWF()
    w.emit('on_custom', payload=1001)
    assert called[-1] == 1001

def test_connect_wrong_hook_public():
    from celery_dyrygent.workflows import WorkflowException
    class MyWF2(WorkflowSignalMixin):
        hooks = {}

    with pytest.raises(WorkflowException):
        MyWF2.connect('unknown_hook')

def test_emit_assertion_error_public():
    # 'unregistered_hook' is not present in hooks, so should raise AssertionError
    class MyWF3(WorkflowSignalMixin):
        hooks = {'some_hook': []}
    w = MyWF3()
    import pytest
    with pytest.raises(AssertionError):
        w.emit('unregistered_hook', 'data')