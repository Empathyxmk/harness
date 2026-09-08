import pytest

# Simulate Redux-like state and thunk handling
class Store:
    def __init__(self, reducer, middleware=None):
        self.reducer = reducer
        self.state = {}
        self.listeners = []
        self.actions = []
        self.middleware = middleware
        self._dispatch = self._default_dispatch
        if middleware:
            self.dispatch = middleware(self)(self._default_dispatch)
        else:
            self.dispatch = self._default_dispatch

    def _default_dispatch(self, action):
        self.state = self.reducer(self.state, action)
        self.actions.append(action)
        for listener in self.listeners:
            listener()
        return action

    def get_state(self):
        return self.state

    def subscribe(self, listener):
        self.listeners.append(listener)
        return lambda: self.listeners.remove(listener)

def thunk_middleware(store):
    def middleware(dispatch):
        def inner(action):
            if callable(action):
                return action(dispatch)
            return dispatch(action)
        return inner
    return middleware

HTTP_STATUS_OK_BOUNDS = {'min': 200, 'max': 300}

class FakeHTTPResponse:
    def __init__(self, status, text=''):
        self.status = status
        self._text = text

    def text(self):
        return self._text

def fake_fetch(href):
    # Returns a FakeHTTPResponse based on url (simulate success for /foo, /bar, fail otherwise)
    from urllib.parse import urlparse
    path = urlparse(href).path
    if path in ['/foo', '/bar']:
        return FakeHTTPResponse(200, f"echo {path}")
    else:
        return FakeHTTPResponse(404, "Not found")

def test_dispatched_real_world_like_example_using_redux_koa_etal(monkeypatch):
    # Monkeypatch fetch
    monkeypatch.setattr('tests.original.test_dispatched.fake_fetch', fake_fetch)

    FETCH_STARTED = 'FETCH_STARTED'
    FETCH_FAILED = 'FETCH_FAILED'
    FETCH_SUCCEEDED = 'FETCH_SUCCEEDED'

    def rootReducer(state=None, action=None):
        if state is None:
            state = {}
        if action is None:
            return state
        type_ = action.get('type')
        payload = action.copy()
        payload.pop('type', None)
        if type_ == FETCH_STARTED:
            into = payload.get('into')
            state2 = state.copy()
            state2[into] = {'status': FETCH_STARTED}
            return state2
        if type_ == FETCH_FAILED:
            into = payload.get('into')
            state2 = state.copy()
            state2[into] = {
                'status': FETCH_FAILED,
                'statusCode': payload.get('statusCode'),
                'err': payload.get('err'),
            }
            return state2
        if type_ == FETCH_SUCCEEDED:
            into = payload.get('into')
            state2 = state.copy()
            state2[into] = {
                'status': FETCH_SUCCEEDED,
                'value': payload.get('value'),
            }
            return state2
        return state

    store = Store(rootReducer, middleware=thunk_middleware)

    def fetch_into(pathname, into):
        async def thunk(dispatch):
            dispatch({'type': FETCH_STARTED, 'into': into})
            # Compose fake url
            baseUrlObj = {'protocol': 'http:', 'hostname': 'localhost', 'port': 8000}
            from urllib.parse import urlunparse
            url = f"http://localhost:8000{pathname}"
            res = fake_fetch(url)
            if res.status < HTTP_STATUS_OK_BOUNDS['min'] or res.status >= HTTP_STATUS_OK_BOUNDS['max']:
                dispatch({
                    'type': FETCH_FAILED,
                    'into': into,
                    'statusCode': res.status,
                    'err': res.text()
                })
                return
            dispatch({
                'type': FETCH_SUCCEEDED,
                'into': into,
                'value': res.text()
            })
        return thunk

    # Simulated 'connected' components: just functions accessing store state
    def OriginalEchoAlpha(alpha):
        if not isinstance(alpha, dict):
            return "???"
        status = alpha.get('status')
        err = alpha.get('err')
        value = alpha.get('value')
        if status == FETCH_STARTED:
            return "..."
        if status == FETCH_FAILED:
            return f"Error fetching beta (Reason: {err})"
        return value

    def ConnectedEchoAlpha(store):
        def get_alpha():
            return store.get_state().get('alpha', {})
        return lambda: OriginalEchoAlpha(get_alpha())

    def EchoAlpha(store):
        async def runner():
            await fetch_into("/foo", 'alpha')(store.dispatch)
            return ConnectedEchoAlpha(store)()
        return runner

    def OriginalEchoBeta(beta):
        if not isinstance(beta, dict):
            return "???"
        status = beta.get('status')
        err = beta.get('err')
        value = beta.get('value')
        if status == FETCH_STARTED:
            return "..."
        if status == FETCH_FAILED:
            return f"Error fetching beta (Reason: {err})"
        return value

    def ConnectedEchoBeta(store):
        def get_beta():
            return store.get_state().get('beta', {})
        return lambda: OriginalEchoBeta(get_beta())

    def EchoBeta(store):
        async def runner():
            await fetch_into("/bar", 'beta')(store.dispatch)
            return ConnectedEchoBeta(store)()
        return runner

    # "App"
    async def run_app():
        # prepare
        await fetch_into("/foo", 'alpha')(store.dispatch)
        await fetch_into("/bar", 'beta')(store.dispatch)
        # render to static markup
        html = (
            "<ul>"
            f"<li><div>{ConnectedEchoAlpha(store)()}</div></li>"
            f"<li><div>{ConnectedEchoBeta(store)()}</div></li>"
            "</ul>"
        )
        return html

    import asyncio
    html = asyncio.run(run_app())
    assert html == '<ul><li><div>echo /foo</div></li><li><div>echo /bar</div></li></ul>', 'renders correct html'