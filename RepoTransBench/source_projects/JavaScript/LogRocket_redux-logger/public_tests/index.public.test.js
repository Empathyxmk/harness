const { createLogger, logger } = require('../src/index');
const printBuffer = require('../src/core').default;

describe('index (public)', () => {
  test('defaultLogger warns if no dispatch/getState (public)', () => {
    global.console.error = jest.fn();
    logger({ foo: 'bar' });
    expect(console.error).toHaveBeenCalled();
  });

  test('defaultLogger with dispatch/getState calls createLogger (public)', () => {
    const dispatch = jest.fn();
    const getState = jest.fn().mockReturnValue({ foo: 'bar' });
    expect(typeof logger({dispatch, getState, bar: 'baz'})).toBe('function');
  });

  test('createLogger returns noop if logger missing (public)', () => {
    const middleware = createLogger({ someField: 42 }); // no logger provided
    const fakeStore = { getState: () => ({ key: 'val' }) };
    const fakeNext = jest.fn();
    const fn = middleware(fakeStore);
    expect(typeof fn(fakeNext)).toBe('function');
    expect(fakeNext).not.toHaveBeenCalled();
  });

  test('createLogger installs as middleware (public)', () => {
    const toLog = [];
    const opts = {
      logger: {
        log: (...a) => toLog.push(['log-public', ...a]),
        group: (...a) => toLog.push(['group-public', ...a]),
        groupEnd: () => toLog.push(['groupEnd-public']),
        groupCollapsed: (...a) => toLog.push(['groupCollapsed-public', ...a])
      },
      stateTransformer: a => a,
      errorTransformer: e => e,
      predicate: null,
      logErrors: false
    };
    const middleware = createLogger(opts);
    const store = { getState: () => ({ bar: 123 }) };
    const dispatched = [];
    const next = action => { dispatched.push(action); return 'publicReturn'; };
    const action = { type: 'DIFFERENT', id: 99 };
    const fn = middleware(store)(next);
    const res = fn(action);
    expect(res).toBe('publicReturn');
    expect(toLog.length).toBeGreaterThan(0);
    expect(dispatched[0]).toBe(action);
  });

  test('createLogger calls predicate, skips logging (public)', () => {
    const predicate = jest.fn(() => false);
    const next = jest.fn(x => 'PUBLIC_VAL');
    const middleware = createLogger({
      logger: {log(){}, group(){}, groupEnd(){}, groupCollapsed(){}},
      stateTransformer: a => a,
      actionTransformer: a => a,
      predicate
    });
    const store = { getState: () => ({ some: 7 }) };
    const fn = middleware(store)(next);
    expect(fn({type: 'Z'})).toBe('PUBLIC_VAL');
    expect(predicate).toHaveBeenCalled();
    expect(next).toHaveBeenCalled();
  });

  test('createLogger logs error when logErrors (public)', () => {
    const errorObject = new Error('PUBLIC error!');
    const opts = {
      logger: {log(){}, group(){}, groupEnd(){}, groupCollapsed(){}},
      stateTransformer: a => a,
      errorTransformer: e => e,
      logErrors: true
    };
    const next = () => { throw errorObject; };
    const middleware = createLogger(opts);
    const store = { getState: () => ({ some: 'val' }) };
    const fn = middleware(store)(next);
    expect(() => fn({type: 'ERR'})).toThrow(errorObject);
  });

  test('createLogger uses diffPredicate (public)', () => {
    let called = false;
    const middleware = createLogger({
      logger: {log(){}, group(){}, groupEnd(){}, groupCollapsed(){}},
      stateTransformer: a => a,
      actionTransformer: a => a,
      diff: true,
      diffPredicate: () => { called = true; return false; }
    });
    const store = { getState: () => ({ foo: 'bar' }) };
    const fn = middleware(store)(a=>a);
    fn({type: 'P'});
    expect(called).toBe(true);
  });
});