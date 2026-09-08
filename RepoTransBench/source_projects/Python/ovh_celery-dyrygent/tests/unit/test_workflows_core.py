import pytest

from celery_dyrygent.workflows import WorkflowException
from celery_dyrygent.workflows.exceptions import WorkflowException as WFExc
from celery_dyrygent.workflows.workflow import CeleryWorkflowMixin, WorkflowSignalMixin

def test_workflow_exception_inheritance():
    assert issubclass(WFExc, Exception)
    with pytest.raises(WFExc, match="error"):
        raise WFExc("error")

class DummyWorkflow(CeleryWorkflowMixin):
    def add_signature(self, signature, dependencies):
        return "signode"

def test_celeryworkflowmixin_add_celery_signature_calls_add_signature(mocker):
    dummy = DummyWorkflow()
    sig = mocker.Mock()
    sig.freeze = mocker.Mock()
    result = dummy.add_celery_signature(sig, dependencies=None)
    sig.freeze.assert_called_once()
    assert result == ["signode"]

def test_celeryworkflowmixin_add_celery_canvas_calls_handlers_real_types(mocker):
    dummy = DummyWorkflow()
    # Import the actual classes
    from celery_dyrygent.workflows import workflow as wf_mod
    # Patch handler methods for call verification
    dummy.add_celery_signature = lambda sig, dep=None: ["one"]
    dummy.add_celery_chord = lambda chord, dep: ["chord"]
    dummy.add_celery_chain = lambda chain, dep=None: ["chain"]
    dummy.add_celery_group = lambda group, dep: ["group"]

    # Correct instantiation for all canvas types!
    assert dummy.add_celery_canvas(wf_mod.entities.Signature(), None) == ["one"]
    # Chord needs both header and body
    header, body = [], None
    assert dummy.add_celery_canvas(wf_mod.entities.Chord(header, body), None) == ["chord"]
    # Chain can be initiated empty or with one
    chain_tasks = []
    assert dummy.add_celery_canvas(wf_mod.entities.Chain(chain_tasks), None) == ["chain"]
    group_tasks = []
    assert dummy.add_celery_canvas(wf_mod.entities.Group(group_tasks), None) == ["group"]
    # Unknown type triggers KeyError, which is expected behaviour per code
    class Unknown: pass
    with pytest.raises(KeyError):
        dummy.add_celery_canvas(Unknown(), None)

def test_signal_connect_and_emit(monkeypatch):
    class T(WorkflowSignalMixin):
        hooks = {'on_state_change': [], 'on_finish': [], 'after_active_tick': []}

    called = []

    @T.connect('on_finish')
    def cb(workflow, payload):
        called.append((workflow, payload))

    t = T()
    t.emit('on_finish', payload=42)
    assert called[-1][1] == 42

    # Unknown hook_name raises WorkflowException
    with pytest.raises(WorkflowException):
        class T2(WorkflowSignalMixin):
            hooks = {'on_finish': []}
        T2.connect('bad_hook')

    # Emits for wrong hook raises AssertionError
    t = T()
    with pytest.raises(AssertionError):
        t.emit('bad_hook', 5)

def test_signal_multiple_hooks_are_independent(monkeypatch):
    class T(WorkflowSignalMixin):
        hooks = {'on_state_change': [], 'on_finish': [], 'after_active_tick': []}

    called = []
    @T.connect('after_active_tick')
    def cb1(wk, pay):
        called.append(('cb1', pay))
    @T.connect('after_active_tick')
    def cb2(wk, pay):
        called.append(('cb2', pay))

    t = T()
    t.emit('after_active_tick', 'xxx')
    assert len([v for v, p in called if v == 'cb1']) == 1
    assert len([v for v, p in called if v == 'cb2']) == 1