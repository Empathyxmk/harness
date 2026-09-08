const createRavenMiddleware = require('../index');

// Mock Raven API for public tests
function createMockRaven() {
  return {
    setDataCallback: jest.fn(),
    captureBreadcrumb: jest.fn()
  };
}

function createMockStore(getStateResp = { baz: 'qux' }) {
  return {
    getState: jest.fn(() => getStateResp)
  };
}

describe('createRavenMiddleware [PUBLIC TESTS]', () => {
  it('should export a function', () => {
    expect(typeof createRavenMiddleware).toBe('function');
  });

  it('returns a middleware function when invoked', () => {
    const Raven = createMockRaven();
    const mw = createRavenMiddleware(Raven);
    expect(typeof mw).toBe('function');
  });

  it('invokes setDataCallback with a function as argument', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    createRavenMiddleware(Raven)(store);

    expect(Raven.setDataCallback).toHaveBeenCalled();
    expect(typeof Raven.setDataCallback.mock.calls[0][0]).toBe('function');
  });

  it('setDataCallback callback augments data.extra, invokes original, getUserContext, and getTags (with different data)', () => {
    const original = jest.fn(d => ({ ...d, zzz: 101 }));
    const getUserContext = jest.fn(() => ({ uid: 77 }));
    const getTags = jest.fn(() => ({ status: 'active' }));
    const Raven = createMockRaven();
    const state = { check: 'vvv' };
    const store = createMockStore(state);

    createRavenMiddleware(Raven, {
      actionTransformer: a => ({ newAct: true, ...a }),
      stateTransformer: s => ({ customState: s.check }),
      getUserContext,
      getTags
    })(store);

    // find the callback passed to setDataCallback
    const callback = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: { exist: 'qq' } };
    callback(data, original);

    expect(original).toHaveBeenCalled();
    expect(getUserContext).toHaveBeenCalledWith(state);
    expect(getTags).toHaveBeenCalledWith(state);

    const passedData = original.mock.calls[0][0];
    expect(passedData.extra).toHaveProperty('lastAction');
    expect(passedData.extra).toHaveProperty('state');
    expect(passedData.user).toEqual({ uid: 77 });
    expect(passedData.tags).toEqual({ status: 'active' });
    expect(passedData.extra.exist).toBe('qq');
    expect(passedData.extra.state).toEqual({ customState: 'vvv' });
  });

  it('setDataCallback callback returns data if original is undefined', () => {
    const Raven = createMockRaven();
    const store = createMockStore({ lorem: 'ipsum' });

    createRavenMiddleware(Raven)(store);

    const cb = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: { x: 9 } };
    const r = cb(data, undefined);

    // Should return exactly the data passed ("data")
    expect(r).toBe(data);
  });

  it('middleware passes action to next middleware and updates lastAction', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn(a => ({ ...a, testadd: true }));
    const action = { type: 'ECHO' };

    const mw = createRavenMiddleware(Raven)(store)(next);
    const ret = mw(action);

    expect(ret).toEqual({ ...action, testadd: true });
    expect(Raven.captureBreadcrumb).toHaveBeenCalled();
  });

  it('custom breadcrumbMessageFromAction, breadcrumbDataFromAction, breadcrumbCategory, filterBreadcrumbActions work (different data)', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const customOptions = {
      breadcrumbMessageFromAction: a => "EVENT_" + (a.kind || a.type),
      breadcrumbDataFromAction: a => ({ value: a.info }),
      breadcrumbCategory: "custom-category",
      filterBreadcrumbActions: a => a.type !== "NOLOG"
    };

    const mw = createRavenMiddleware(Raven, customOptions)(store)(next);

    // Should call captureBreadcrumb with custom fields
    const action = { type: "ANOTHER", info: 222 };
    mw(action);

    expect(Raven.captureBreadcrumb).toHaveBeenCalledWith({
      category: "custom-category",
      message: "EVENT_ANOTHER",
      data: { value: 222 }
    });

    // Should not call for filtered-out action
    Raven.captureBreadcrumb.mockClear();
    mw({ type: "NOLOG", info: 333 });
    expect(Raven.captureBreadcrumb).not.toHaveBeenCalled();
  });

  it('default filterBreadcrumbActions allows all (with alternate action)', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const mw = createRavenMiddleware(Raven)(store)(next);
    mw({ type: "SOME_ACTION" });
    expect(Raven.captureBreadcrumb).toHaveBeenCalled();
  });

  it('breadcrumbDataFromAction default returns undefined (with another action type)', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const mw = createRavenMiddleware(Raven)(store)(next);

    mw({ type: "OTHER_DATA_UNDEF" });
    expect(
      Raven.captureBreadcrumb.mock.calls[0][0].data
    ).toBeUndefined();
  });

  it('stateTransformer and actionTransformer defaults are identity (different state)', () => {
    const Raven = createMockRaven();
    const store = createMockStore({ bar: 'BAZ' });

    createRavenMiddleware(Raven)(store);

    const cb = Raven.setDataCallback.mock.calls[0][0];
    const data = { extra: {} };
    cb(data);

    expect(data.extra.state).toEqual({ bar: 'BAZ' });
  });

  it('an action object with no type sets breadcrumb message to undefined (different property)', () => {
    const Raven = createMockRaven();
    const store = createMockStore();
    const next = jest.fn();
    const mw = createRavenMiddleware(Raven)(store)(next);
    mw({ idonly: 999 });
    expect(Raven.captureBreadcrumb.mock.calls[0][0].message).toBe(undefined);
  });

  it('edge: multiple calls update lastAction and context is updated [changed action/state]', () => {
    const Raven = createMockRaven();
    const store = createMockStore({ bar: 202 });
    const next = jest.fn(a => a);

    const mwOuter = createRavenMiddleware(Raven)(store);
    const mw = mwOuter(next);

    const action1 = { type: "FIRST", payload: 1001 };
    mw(action1);
    const action2 = { type: "SECOND", payload: 2002 };
    mw(action2);

    // simulate error to test context callback
    const cb = Raven.setDataCallback.mock.calls[0][0];

    let d = { extra: {} };
    cb(d);

    expect(d.extra.lastAction).toEqual(action2);
    expect(d.extra.state).toEqual({ bar: 202 });
  });
});