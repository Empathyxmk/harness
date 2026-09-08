import pytest
from unittest.mock import Mock
from src.raven_for_redux.middleware import create_raven_middleware

def create_mock_raven():
    Raven = Mock()
    Raven.setDataCallback = Mock()
    Raven.captureBreadcrumb = Mock()
    return Raven

def create_mock_store(get_state_resp=None):
    if get_state_resp is None:
        get_state_resp = {"baz": "qux"}
    store = Mock()
    store.getState = Mock(return_value=get_state_resp)
    return store

def test_should_export_a_function():
    assert callable(create_raven_middleware)

def test_returns_middleware_function_when_invoked():
    Raven = create_mock_raven()
    mw = create_raven_middleware(Raven)
    assert callable(mw)

def test_invokes_setDataCallback_with_function_argument():
    Raven = create_mock_raven()
    store = create_mock_store()
    create_raven_middleware(Raven)(store)
    assert Raven.setDataCallback.called
    cb = Raven.setDataCallback.call_args[0][0]
    assert callable(cb)

def test_setDataCallback_callback_augments_data_extra_and_invokes_original_user_tags():
    original = Mock(side_effect=lambda d: {**d, "zzz": 101})
    getUserContext = Mock(return_value={"uid": 77})
    getTags = Mock(return_value={"status": "active"})
    Raven = create_mock_raven()
    state = {"check": "vvv"}
    store = create_mock_store(state)

    create_raven_middleware(Raven, {
        "actionTransformer": lambda a: {"newAct": True, **(a or {})} if a is not None else {"newAct": True},
        "stateTransformer": lambda s: {"customState": s["check"]},
        "getUserContext": getUserContext,
        "getTags": getTags
    })(store)

    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {"exist": "qq"}}
    cb(data, original)
    assert original.called
    getUserContext.assert_called_with(state)
    getTags.assert_called_with(state)
    called_data = original.call_args[0][0]
    assert "lastAction" in called_data["extra"]
    assert "state" in called_data["extra"]
    assert called_data["user"] == {"uid": 77}
    assert called_data["tags"] == {"status": "active"}
    assert called_data["extra"]["exist"] == "qq"
    assert called_data["extra"]["state"] == {"customState": "vvv"}

def test_setDataCallback_callback_returns_data_if_original_is_undefined():
    Raven = create_mock_raven()
    store = create_mock_store({"lorem": "ipsum"})
    create_raven_middleware(Raven)(store)
    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {"x": 9}}
    r = cb(data, None)
    assert r is data

def test_middleware_passes_action_to_next_and_updates_lastAction():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock(side_effect=lambda a: {**a, "testadd": True})
    action = {"type": "ECHO"}
    mw = create_raven_middleware(Raven)(store)(next_)
    ret = mw(action)
    assert ret == {**action, "testadd": True}
    assert Raven.captureBreadcrumb.called

def test_custom_breadcrumb_functions_and_filtering():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    custom_options = {
        "breadcrumbMessageFromAction": lambda a: "EVENT_" + (a.get("kind", a.get("type"))) if isinstance(a, dict) else None,
        "breadcrumbDataFromAction": lambda a: {"value": a["info"]} if "info" in a else None,
        "breadcrumbCategory": "custom-category",
        "filterBreadcrumbActions": lambda a: a.get("type") != "NOLOG" if isinstance(a, dict) and "type" in a else True
    }
    mw = create_raven_middleware(Raven, custom_options)(store)(next_)
    action = {"type": "ANOTHER", "info": 222}
    mw(action)
    Raven.captureBreadcrumb.assert_called_with({
        "category": "custom-category",
        "message": "EVENT_ANOTHER",
        "data": {"value": 222}
    })
    Raven.captureBreadcrumb.reset_mock()
    mw({"type": "NOLOG", "info": 333})
    Raven.captureBreadcrumb.assert_not_called()

def test_default_filterBreadcrumbActions_allows_all_with_alternate():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    mw = create_raven_middleware(Raven)(store)(next_)
    mw({"type": "SOME_ACTION"})
    assert Raven.captureBreadcrumb.called

def test_breadcrumbDataFromAction_default_returns_None_with_other_action():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    mw = create_raven_middleware(Raven)(store)(next_)
    mw({"type": "OTHER_DATA_UNDEF"})
    call_args = Raven.captureBreadcrumb.call_args[0][0]
    assert call_args["data"] is None

def test_stateTransformer_actionTransformer_defaults_are_identity_different_state():
    Raven = create_mock_raven()
    store = create_mock_store({"bar": "BAZ"})
    create_raven_middleware(Raven)(store)
    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {}}
    cb(data)
    assert data["extra"]["state"] == {"bar": "BAZ"}

def test_action_object_no_type_sets_breadcrumb_message_to_none():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    mw = create_raven_middleware(Raven)(store)(next_)
    mw({"idonly": 999})
    call_args = Raven.captureBreadcrumb.call_args[0][0]
    assert call_args["message"] is None

def test_edge_multiple_calls_update_lastAction_and_context():
    Raven = create_mock_raven()
    store = create_mock_store({"bar": 202})
    next_ = Mock(side_effect=lambda a: a)
    mw_outer = create_raven_middleware(Raven)(store)
    mw = mw_outer(next_)
    action1 = {"type": "FIRST", "payload": 1001}
    mw(action1)
    action2 = {"type": "SECOND", "payload": 2002}
    mw(action2)
    cb = Raven.setDataCallback.call_args[0][0]
    d = {"extra": {}}
    cb(d)
    assert d["extra"]["lastAction"] == action2
    assert d["extra"]["state"] == {"bar": 202}