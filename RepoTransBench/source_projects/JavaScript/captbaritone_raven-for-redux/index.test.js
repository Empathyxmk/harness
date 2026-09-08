const createRavenMiddleware = require('./index');

// Mock Raven API
function createMockRaven() {
  return {
    setDataCallback: jest.fn(),
    captureBreadcrumb: jest.fn()
  };
}

function createMockStore(getStateResp = { foo: 'bar' }) {
  return {
    getState: jest.fn(() => getStateResp)
  };
}

describe('createRavenMiddleware', () => {
  it('should be a function', () => {
    expect(typeof createRavenMiddleware).toBe('function');
  });

  it('returns a middleware function', () => {
    const Raven = createMockRaven();
    const mw = createRavenMiddleware(Raven);
    expect(typeof mw).toBe('function');
  });

  it('calls setDataCallback with a callback', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    createRavenMiddleware(Raven)(store);

    expect(Raven.setDataCallback).toHaveBeenCalled();
    expect(typeof Raven.setDataCallback.mock.calls[0][0]).toBe('function');
  });

  it('setDataCallback callback extends data.extra and invokes original, getUserContext, and getTags', () => {
    const original = jest.fn(d => ({ ...d, extraDummy: 42 }));
    const getUserContext = jest.fn(() => ({ id: 1 }));
    const getTags = jest.fn(() => ({ tag: 'yes' }));
    const Raven = createMockRaven();
    const state = { val: 'x' };
    const store = createMockStore(state);

    createRavenMiddleware(Raven, {
      actionTransformer: a => ({ x: 'y', ...a }),
      stateTransformer: s => ({ stateX: s.val }),
      getUserContext,
      getTags
    })(store);

    // find the callback passed to setDataCallback
    const callback = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: { old: 'a' } };
    callback(data, original);

    expect(original).toHaveBeenCalled();
    expect(getUserContext).toHaveBeenCalledWith(state);
    expect(getTags).toHaveBeenCalledWith(state);
    // lastAction is undefined at first, so lastAction should be the transformer applied to undefined
    const passedData = original.mock.calls[0][0];
    expect(passedData.extra).toHaveProperty('lastAction');
    expect(passedData.extra).toHaveProperty('state');
    expect(passedData.user).toEqual({ id: 1 });
    expect(passedData.tags).toEqual({ tag: 'yes' });
    expect(passedData.extra.old).toBe('a');
    expect(passedData.extra.state).toEqual({ stateX: 'x' });
  });

  it('setDataCallback callback returns data if original is falsy', () => {
    const Raven = createMockRaven();
    const store = createMockStore({ foo: 'bar' });

    createRavenMiddleware(Raven)(store);

    const cb = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: { a: 1 } };
    const r = cb(data, null);

    // Should return exactly the data passed (in this case, "data")
    expect(r).toBe(data);
  });

  it('middleware passes action to next and updates lastAction', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn(a => a);
    const action = { type: 'PING' };

    const mw = createRavenMiddleware(Raven)(store)(next);
    const ret = mw(action);

    expect(ret).toBe(action);
    // lastAction will be updated, but not directly testable; indirect checks via callback
    // But we can check captureBreadcrumb was called.
    expect(Raven.captureBreadcrumb).toHaveBeenCalled();
  });

  it('breadcrumbMessageFromAction, breadcrumbDataFromAction, breadcrumbCategory, filterBreadcrumbActions can be customized', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const customOptions = {
      breadcrumbMessageFromAction: a => "MSG_" + a.type,
      breadcrumbDataFromAction: a => ({ foo: a.payload }),
      breadcrumbCategory: "my-category",
      filterBreadcrumbActions: a => a.type !== "IGNORE"
    };

    const mw = createRavenMiddleware(Raven, customOptions)(store)(next);

    // Should call captureBreadcrumb with custom fields
    const action = { type: "TESTING", payload: 123 };
    mw(action);

    expect(Raven.captureBreadcrumb).toHaveBeenCalledWith({
      category: "my-category",
      message: "MSG_TESTING",
      data: { foo: 123 }
    });

    // Should not call for filtered-out action
    Raven.captureBreadcrumb.mockClear();
    mw({ type: "IGNORE", payload: 456 });
    expect(Raven.captureBreadcrumb).not.toHaveBeenCalled();
  });

  it('default filterBreadcrumbActions allows all', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const mw = createRavenMiddleware(Raven)(store)(next);
    mw({ type: "ANY_ACTION" });
    expect(Raven.captureBreadcrumb).toHaveBeenCalled();
  });

  it('breadcrumbDataFromAction default returns undefined', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const mw = createRavenMiddleware(Raven)(store)(next);

    mw({ type: "TEST_DATA_UNDEF" });
    expect(
      Raven.captureBreadcrumb.mock.calls[0][0].data
    ).toBeUndefined();
  });

  it('stateTransformer and actionTransformer defaults are identity', () => {
    const Raven = createMockRaven();
    const store = createMockStore({ foo: 'BAR' });

    createRavenMiddleware(Raven)(store);

    const cb = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: {} };
    cb(data);

    expect(data.extra.state).toEqual({ foo: 'BAR' });
  });

  it('receive an action with no type still sets breadcrumb message to undefined', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const mw = createRavenMiddleware(Raven)(store)(next);
    mw({ notype: 42 });
    expect(Raven.captureBreadcrumb.mock.calls[0][0].message).toBe(undefined);
  });

  it('edge: multiple calls, updates lastAction each time and context is updated', () => {
    const Raven = createMockRaven();
    const store = createMockStore({ foo: 10 });
    const next = jest.fn(a => a);

    const mwOuter = createRavenMiddleware(Raven)(store);
    const mw = mwOuter(next);

    const action1 = { type: "HELLO", payload: 123 };
    mw(action1);
    const action2 = { type: "WORLD", payload: 456 };
    mw(action2);

    // simulate error to test context callback
    const cb = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: {} };
    cb(data);

    expect(Raven.captureBreadcrumb).toHaveBeenCalledTimes(2);
    expect(data.extra.lastAction).toEqual({ type: "WORLD", payload: 456 });
  });
});