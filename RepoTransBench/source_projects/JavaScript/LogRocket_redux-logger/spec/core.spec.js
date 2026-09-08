// NOTE: Testing the logging logic by using spies for logger
const printBuffer = require('../src/core').default;
const { formatTime } = require('../src/helpers');

describe('core/printBuffer', () => {
  const buildLogger = () => ({
    log: jest.fn(),
    group: jest.fn(),
    groupCollapsed: jest.fn(),
    groupEnd: jest.fn(),
    trace: jest.fn()
  });

  const defaultColors = {
    title: () => 'red',
    prevState: () => 'blue',
    action: () => 'green',
    error: () => 'black',
    nextState: () => 'yellow'
  };

  function getDefaultOptions(overrides = {}) {
    return {
      logger: buildLogger(),
      actionTransformer: a => a,
      titleFormatter: undefined,
      collapsed: false,
      colors: defaultColors,
      level: 'log',
      diff: false,
      timestamp: true,
      duration: true,
      ...overrides
    };
  }
  function buildBuffer(error = false) {
    return [
      {
        started: 0,
        startedTime: new Date(2020, 1, 1, 6, 6, 6, 123),
        action: { type: 'FOO' },
        prevState: { a: 1 },
        error: error ? "SOME_ERR" : undefined,
        took: 3.15,
        nextState: { a: 2 }
      }
    ];
  }

  test('printBuffer logs groupCollapsed if collapsed', () => {
    const opts = getDefaultOptions({ collapsed: true });
    printBuffer(buildBuffer(), opts);
    expect(opts.logger.groupCollapsed).toHaveBeenCalled();
  });

  test('printBuffer logs group if not collapsed', () => {
    const opts = getDefaultOptions({ collapsed: false });
    printBuffer(buildBuffer(), opts);
    expect(opts.logger.group).toHaveBeenCalled();
  });

  test('printBuffer uses groupCollapsed when error is thrown', () => {
    const errorLogger = buildLogger();
    errorLogger.groupCollapsed = () => { throw new Error('failed'); };
    errorLogger.log = jest.fn();
    const opts = getDefaultOptions({ collapsed: true, logger: errorLogger });
    printBuffer(buildBuffer(), opts);
    expect(errorLogger.log).toHaveBeenCalled();
  });

  test('printBuffer formats title including timestamp and duration', () => {
    const opts = getDefaultOptions({
      titleFormatter: (action, time, took) => `MYTITLE ${action.type} ${time} ${took}`
    });
    printBuffer(buildBuffer(), opts);
    expect(opts.logger.group).toHaveBeenCalledWith('MYTITLE FOO 06:06:06.123 3.15');
  });

  test('printBuffer logs prevState, action, error, nextState with correct styles', () => {
    const opts = getDefaultOptions();
    printBuffer(buildBuffer(true), opts);
    expect(opts.logger.log).toHaveBeenCalled();
  });

  test('printBuffer logs trace if logger.withTrace', () => {
    const logger = buildLogger();
    logger.withTrace = true;
    const opts = getDefaultOptions({ logger });
    printBuffer(buildBuffer(), opts);
    expect(logger.trace).toHaveBeenCalled();
    expect(logger.groupCollapsed).toHaveBeenCalledWith('TRACE');
    expect(logger.groupEnd).toHaveBeenCalled();
  });

  test('printBuffer calls groupEnd, handles groupEnd error', () => {
    const logger = buildLogger();
    logger.groupEnd = () => { throw new Error('fail end'); };
    logger.log = jest.fn();
    const opts = getDefaultOptions({ logger });
    printBuffer(buildBuffer(), opts);
    expect(logger.log).toHaveBeenCalled();
  });
});