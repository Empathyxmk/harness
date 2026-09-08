import pytest

from celery_dyrygent.workflows import WorkflowException
from celery_dyrygent.workflows.exceptions import WorkflowException as WFExc
from celery_dyrygent.workflows.workflow import CeleryWorkflowMixin, WorkflowSignalMixin

def test_workflow_exception_inheritance_public():
    assert issubclass(WFExc, BaseException)
    with pytest.raises(WFExc, match="another error"):
        raise WFExc("another error")

class DummyWorkflowPub(CeleryWorkflowMixin):
    def add_signature(self, signature, dependencies):
        return "nodex"

def test_celeryworkflowmixin_add_celery_signature_calls_add_signature_public(mocker):
    dummy = DummyWorkflowPub()
    sig = mocker.Mock()
    sig.freeze = mocker.Mock()
    result = dummy.add_celery_signature(sig, dependencies="something")
    sig.freeze.assert_called_once()
    assert result == ["nodex"]

def test_celeryworkflowmixin_add_celery_canvas_calls_handlers_real_types_public(mocker):
    dummy = DummyWorkflowPub()
    from celery_dyrygent.workflows import workflow as wf_mod
    dummy.add_celery_signature = lambda sig, dep=None: ["alpha"]
    dummy.add_celery_chord = lambda chord, dep: ["beta"]
    dummy.add_celery_chain = lambda chain, dep=None: ["gamma"]
    dummy.add_celery_group = lambda group, dep: ["delta"]

    # Use alternate objects with other test data for coverage
    assert dummy.add_celery_canvas(wf_mod.entities.Signature(), dependencies={"foo": 1}) == ["alpha"]
    # Chord with non-empty header
    header, body = [1], "b"
    assert dummy.add_celery_canvas(wf_mod.entities.Chord(header, body), None) == ["beta"]
    # Chain with a fake task for diversity
    chain_tasks = [object()]
    assert dummy.add_celery_canvas(wf_mod.entities.Chain(chain_tasks), None) == ["gamma"]
    group_tasks = [2]
    assert dummy.add_celery_canvas(wf_mod.entities.Group(group_tasks), None) == ["delta"]
    # Unknown type triggers KeyError
    class X: pass
    with pytest.raises(KeyError):
        dummy.add_celery_canvas(X(), None)

def test_signal_connect_and_emit_public(monkeypatch):
    class T(WorkflowSignalMixin):
        hooks = {'on_update': [], 'on_custom_finish': [], 'after_special_tick': []}

    called = []

    @T.connect('on_custom_finish')
    def cb(workflow, payload):
        called.append((workflow, payload))

    t = T()
    t.emit('on_custom_finish', payload=24)
    assert called[-1][1] == 24

    # Unknown hook_name raises WorkflowException
    with pytest.raises(WorkflowException):
        class T2(WorkflowSignalMixin):
            hooks = {'on_empty': []}
        T2.connect('nonexistent_hook')

    # Emits for wrong hook raises AssertionError
    t = T()
    with pytest.raises(AssertionError):
        t.emit('nonexistent_hook', 15)

def test_signal_multiple_hooks_are_independent_public(monkeypatch):
    class T(WorkflowSignalMixin):
        hooks = {'on_update': [], 'on_custom_finish': [], 'after_special_tick': []}

    called = []
    @T.connect('after_special_tick')
    def cb1(wk, pay):
        called.append(('cb1', pay))
    @T.connect('after_special_tick')
    def cb2(wk, pay):
        called.append(('cb2', pay))

    t = T()
    t.emit('after_special_tick', 'yyy')
    assert len([v for v, p in called if v == 'cb1']) == 1
    assert len([v for v, p in called if v == 'cb2']) == 1