const printBuffer = require('../src/core').default;
const { formatTime } = require('../src/helpers');

describe('core/printBuffer (public)', () => {
  const buildLogger = () => ({
    log: jest.fn(),
    group: jest.fn(),
    groupCollapsed: jest.fn(),
    groupEnd: jest.fn(),
    trace: jest.fn()
  });

  const defaultColors = {
    title: () => 'magenta',
    prevState: () => 'cyan',
    action: () => 'orange',
    error: () => 'pink',
    nextState: () => 'lime'
  };

  function getDefaultOptions(overrides = {}) {
    return {
      logger: buildLogger(),
      actionTransformer: a => ({ ...a, added: 'yes' }),
      titleFormatter: undefined,
      collapsed: true,
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
        started: 100,
        startedTime: new Date(2021, 2, 2, 10, 22, 55, 57),
        action: { type: 'BAR', custom: 5 },
        prevState: { b: 3 },
        error: error ? "DIFFERENT_ERR" : undefined,
        took: 8.45,
        nextState: { b: 4 }
      }
    ];
  }

  test('printBuffer logs groupCollapsed if collapsed (public)', () => {
    const opts = getDefaultOptions({ collapsed: true });
    printBuffer(buildBuffer(), opts);
    expect(opts.logger.groupCollapsed).toHaveBeenCalled();
  });

  test('printBuffer logs group if not collapsed (public)', () => {
    const opts = getDefaultOptions({ collapsed: false });
    printBuffer(buildBuffer(), opts);
    expect(opts.logger.group).toHaveBeenCalled();
  });

  test('printBuffer uses groupCollapsed when error is thrown (public)', () => {
    const errorLogger = buildLogger();
    errorLogger.groupCollapsed = () => { throw new Error('another-failed'); };
    errorLogger.log = jest.fn();
    const opts = getDefaultOptions({ collapsed: true, logger: errorLogger });
    printBuffer(buildBuffer(), opts);
    expect(errorLogger.log).toHaveBeenCalled();
  });

  test('printBuffer formats title including timestamp and duration (public)', () => {
    const opts = getDefaultOptions({
      titleFormatter: (action, time, took) => `PUBTITLE ${action.type} ${time} ${took}`
    });
    printBuffer(buildBuffer(), opts);
    expect(opts.logger.groupCollapsed).toHaveBeenCalledWith('PUBTITLE BAR 10:22:55.057 8.45');
  });

  test('printBuffer logs prevState, action, error, nextState with correct styles (public)', () => {
    const opts = getDefaultOptions();
    printBuffer(buildBuffer(true), opts);
    expect(opts.logger.log).toHaveBeenCalled();
  });

  test('printBuffer logs trace if logger.withTrace (public)', () => {
    const logger = buildLogger();
    logger.withTrace = true;
    const opts = getDefaultOptions({ logger });
    printBuffer(buildBuffer(), opts);
    expect(logger.trace).toHaveBeenCalled();
    expect(logger.groupCollapsed).toHaveBeenCalledWith('TRACE');
    expect(logger.groupEnd).toHaveBeenCalled();
  });

  test('printBuffer calls groupEnd, handles groupEnd error (public)', () => {
    const logger = buildLogger();
    logger.groupEnd = () => { throw new Error('fail-end-public'); };
    logger.log = jest.fn();
    const opts = getDefaultOptions({ logger });
    printBuffer(buildBuffer(), opts);
    expect(logger.log).toHaveBeenCalled();
  });
});