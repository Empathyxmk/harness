import pytest
from unittest.mock import Mock, call
from src.raven_for_redux.middleware import create_raven_middleware

def create_mock_raven():
    Raven = Mock()
    Raven.setDataCallback = Mock()
    Raven.captureBreadcrumb = Mock()
    return Raven

def create_mock_store(get_state_resp=None):
    if get_state_resp is None:
        get_state_resp = {"foo": "bar"}
    store = Mock()
    store.getState = Mock(return_value=get_state_resp)
    return store

def test_createRavenMiddleware_is_function():
    assert callable(create_raven_middleware)

def test_returns_middleware_function():
    Raven = create_mock_raven()
    mw = create_raven_middleware(Raven)
    assert callable(mw)

def test_calls_setDataCallback_with_callback():
    Raven = create_mock_raven()
    store = create_mock_store()
    create_raven_middleware(Raven)(store)
    assert Raven.setDataCallback.called
    cb = Raven.setDataCallback.call_args[0][0]
    assert callable(cb)

def test_setDataCallback_callback_extends_data_and_invokes_original_getUserContext_getTags():
    original = Mock(side_effect=lambda d: {**d, "extraDummy": 42})
    getUserContext = Mock(return_value={"id": 1})
    getTags = Mock(return_value={"tag": "yes"})
    Raven = create_mock_raven()
    state = {"val": "x"}
    store = create_mock_store(state)

    create_raven_middleware(Raven, {
        "actionTransformer": lambda a: {"x": "y", **(a or {})} if a is not None else {"x": "y"},
        "stateTransformer": lambda s: {"stateX": s["val"]},
        "getUserContext": getUserContext,
        "getTags": getTags
    })(store)

    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {"old": "a"}}
    cb(data, original)
    assert original.called
    getUserContext.assert_called_with(state)
    getTags.assert_called_with(state)
    called_data = original.call_args[0][0]
    assert "lastAction" in called_data["extra"]
    assert "state" in called_data["extra"]
    assert called_data["user"] == {"id": 1}
    assert called_data["tags"] == {"tag": "yes"}
    assert called_data["extra"]["old"] == "a"
    assert called_data["extra"]["state"] == {"stateX": "x"}

def test_setDataCallback_callback_returns_data_if_original_falsy():
    Raven = create_mock_raven()
    store = create_mock_store({"foo": "bar"})
    create_raven_middleware(Raven)(store)
    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {"a": 1}}
    r = cb(data, None)
    assert r is data

def test_middleware_passes_action_to_next_and_updates_lastAction():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock(side_effect=lambda a: a)
    action = {"type": "PING"}
    mw = create_raven_middleware(Raven)(store)(next_)
    ret = mw(action)
    assert ret == action
    assert Raven.captureBreadcrumb.called

def test_custom_breadcrumbMessage_breadcrumbData_breadcrumbCategory_filterBreadcrumbActions():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    custom_options = {
        "breadcrumbMessageFromAction": lambda a: "MSG_" + a["type"],
        "breadcrumbDataFromAction": lambda a: {"foo": a["payload"]},
        "breadcrumbCategory": "my-category",
        "filterBreadcrumbActions": lambda a: a["type"] != "IGNORE"
    }
    mw = create_raven_middleware(Raven, custom_options)(store)(next_)
    action = {"type": "TESTING", "payload": 123}
    mw(action)
    Raven.captureBreadcrumb.assert_called_with({
        "category": "my-category",
        "message": "MSG_TESTING",
        "data": {"foo": 123}
    })
    Raven.captureBreadcrumb.reset_mock()
    mw({"type": "IGNORE", "payload": 456})
    Raven.captureBreadcrumb.assert_not_called()

def test_default_filterBreadcrumbActions_allows_all():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    mw = create_raven_middleware(Raven)(store)(next_)
    mw({"type": "ANY_ACTION"})
    assert Raven.captureBreadcrumb.called

def test_breadcrumbDataFromAction_default_returns_None():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    mw = create_raven_middleware(Raven)(store)(next_)
    mw({"type": "TEST_DATA_UNDEF"})
    call_args = Raven.captureBreadcrumb.call_args[0][0]
    assert call_args["data"] is None

def test_stateTransformer_actionTransformer_defaults_are_identity():
    Raven = create_mock_raven()
    store = create_mock_store({"foo": "BAR"})
    create_raven_middleware(Raven)(store)
    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {}}
    cb(data)
    assert data["extra"]["state"] == {"foo": "BAR"}

def test_action_with_no_type_sets_breadcrumb_message_to_none():
    Raven = create_mock_raven()
    store = create_mock_store()
    next_ = Mock()
    mw = create_raven_middleware(Raven)(store)(next_)
    mw({"notype": 42})
    call_args = Raven.captureBreadcrumb.call_args[0][0]
    assert call_args["message"] is None

def test_edge_multiple_calls_updates_lastAction_each_time_and_context_is_updated():
    Raven = create_mock_raven()
    store = create_mock_store({"foo": 10})
    next_ = Mock(side_effect=lambda a: a)
    mw_outer = create_raven_middleware(Raven)(store)
    mw = mw_outer(next_)
    action1 = {"type": "HELLO", "payload": 123}
    mw(action1)
    action2 = {"type": "WORLD", "payload": 456}
    mw(action2)
    cb = Raven.setDataCallback.call_args[0][0]
    data = {"extra": {}}
    cb(data)
    assert Raven.captureBreadcrumb.call_count == 2
    assert data["extra"]["lastAction"] == action2