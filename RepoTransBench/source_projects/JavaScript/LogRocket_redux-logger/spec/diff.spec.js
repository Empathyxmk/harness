const diff = require('../src/diff');

describe('diff', () => {
  test('style returns correct string', () => {
    expect(diff.style('E')).toMatch(/color/);
    expect(diff.style('N')).toMatch(/color/);
    expect(diff.style('D')).toMatch(/color/);
    expect(diff.style('A')).toMatch(/color/);
  });

  test('render returns correct output for E', () => {
    expect(diff.render({ kind: 'E', path: ['foo'], lhs: 1, rhs: 2 })).toEqual(['foo', 1, '→', 2]);
  });
  test('render returns correct output for N', () => {
    expect(diff.render({ kind: 'N', path: ['foo'], rhs: 2 })).toEqual(['foo', 2]);
  });
  test('render returns correct output for D', () => {
    expect(diff.render({ kind: 'D', path: ['bar'] })).toEqual(['bar']);
  });
  test('render returns correct output for A', () => {
    expect(diff.render({ kind: 'A', path: ['arr'], index: 1, item: 'baz' })).toEqual(['arr[1]', 'baz']);
  });
  test('render returns empty for unknown', () => {
    expect(diff.render({ kind: 'X' })).toEqual([]);
  });

  test('diffLogger logs groupCollapsed when isCollapsed', () => {
    const logger = {
      groupCollapsed: jest.fn(),
      group: jest.fn(),
      log: jest.fn(),
      groupEnd: jest.fn()
    };
    // Mock deep-diff to return one 'E'
    jest.mock('deep-diff', () => () => [
      { kind: 'E', path: ['foo'], lhs: 1, rhs: 2 }
    ], { virtual: true });

    const prevState = {foo: 1};
    const newState = {foo: 2};
    require('../src/diff').default(prevState, newState, logger, true);
    expect(logger.groupCollapsed).toHaveBeenCalledWith('diff');
    expect(logger.log).toHaveBeenCalled();
    expect(logger.groupEnd).toHaveBeenCalled();
    jest.resetModules(); // undo virtual mock
  });

  test('diffLogger logs group when !isCollapsed', () => {
    const logger = {
      groupCollapsed: jest.fn(),
      group: jest.fn(),
      log: jest.fn(),
      groupEnd: jest.fn()
    };
    jest.mock('deep-diff', () => () => [{ kind: 'N', path: ['foo'], rhs: 2 }], { virtual: true });
    const prevState = {};
    const newState = {foo: 2};
    require('../src/diff').default(prevState, newState, logger, false);
    expect(logger.group).toHaveBeenCalledWith('diff');
    expect(logger.log).toHaveBeenCalled();
    expect(logger.groupEnd).toHaveBeenCalled();
    jest.resetModules();
  });

  test('diffLogger handles no-diff', () => {
    const logger = {
      groupCollapsed: jest.fn(),
      group: jest.fn(),
      log: jest.fn(),
      groupEnd: jest.fn()
    };
    jest.mock('deep-diff', () => () => undefined, { virtual: true });
    require('../src/diff').default({}, {}, logger, false);
    expect(logger.log).toHaveBeenCalledWith('—— no diff ——');
    jest.resetModules();
  });
});