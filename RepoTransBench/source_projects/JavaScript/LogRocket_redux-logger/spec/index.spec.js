const { createLogger, logger } = require('../src/index');
const printBuffer = require('../src/core').default;

describe('index', () => {
  test('defaultLogger warns if no dispatch/getState', () => {
    global.console.error = jest.fn();
    logger();
    expect(console.error).toHaveBeenCalled();
  });

  test('defaultLogger with dispatch/getState calls createLogger', () => {
    const dispatch = jest.fn();
    const getState = jest.fn().mockReturnValue({});
    expect(typeof logger({dispatch, getState})).toBe('function');
  });

  test('createLogger returns noop if logger missing', () => {
    const middleware = createLogger({}); // no logger provided
    const fakeStore = { getState: () => ({}) };
    const fakeNext = jest.fn();
    const fn = middleware(fakeStore);
    expect(typeof fn(fakeNext)).toBe('function');
    expect(fakeNext).not.toHaveBeenCalled();
  });

  test('createLogger installs as middleware', () => {
    const toLog = [];
    const opts = {
      logger: {
        log: (...a) => toLog.push(['log', ...a]),
        group: (...a) => toLog.push(['group', ...a]),
        groupEnd: () => toLog.push(['groupEnd']),
        groupCollapsed: (...a) => toLog.push(['groupCollapsed', ...a])
      },
      stateTransformer: a => a,
      errorTransformer: e => e,
      predicate: null,
      logErrors: false
    };
    const middleware = createLogger(opts);
    const store = { getState: () => ({ some: "state" }) };
    const dispatched = [];
    const next = action => { dispatched.push(action); return 'returnValue'; };
    const action = { type: 'TEST', val: 1 };
    const fn = middleware(store)(next);
    const res = fn(action);
    expect(res).toBe('returnValue');
    expect(toLog.length).toBeGreaterThan(0);
    expect(dispatched[0]).toBe(action);
  });

  test('createLogger calls predicate, skips logging', () => {
    const predicate = jest.fn(() => false);
    const next = jest.fn(x => 'VAL');
    const middleware = createLogger({
      logger: {log(){}, group(){}, groupEnd(){}, groupCollapsed(){}},
      stateTransformer: a => a,
      actionTransformer: a => a,
      predicate
    });
    const store = { getState: () => ({}) };
    const fn = middleware(store)(next);
    expect(fn({type: 'T'})).toBe('VAL');
    expect(predicate).toHaveBeenCalled();
    expect(next).toHaveBeenCalled();
  });

  test('createLogger logs error when logErrors', () => {
    const errored = new Error('problem!');
    const opts = {
      logger: {log(){}, group(){}, groupEnd(){}, groupCollapsed(){}},
      stateTransformer: a => a,
      errorTransformer: e => e,
      logErrors: true
    };
    const next = () => { throw errored; };
    const middleware = createLogger(opts);
    const store = { getState: () => ({}) };
    const fn = middleware(store)(next);
    expect(() => fn({type: 'T'})).toThrow(errored);
  });

  test('createLogger uses diffPredicate', () => {
    let used = false;
    const middleware = createLogger({
      logger: {log(){}, group(){}, groupEnd(){}, groupCollapsed(){}},
      stateTransformer: a => a,
      actionTransformer: a => a,
      diff: true,
      diffPredicate: () => { used = true; return false; }
    });
    const store = { getState: () => ({}) };
    const fn = middleware(store)(a=>a);
    fn({type: 'T'});
    expect(used).toBe(true);
  });
});