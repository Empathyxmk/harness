const log = require('./log');

// Mock the console output
beforeEach(() => {
  jest.spyOn(global.console, 'log').mockImplementation(() => {});
});
afterEach(() => {
  global.console.log.mockRestore();
});

describe('cli/log', () => {
  it('should log info', () => {
    log.info('hello', 'world');
    expect(console.log).toHaveBeenCalled();
  });

  it('should log error', () => {
    log.error('bad', 'thing');
    expect(console.log).toHaveBeenCalled();
  });

  it('should log warn', () => {
    log.warn('careful', 'here');
    expect(console.log).toHaveBeenCalled();
  });

  it('should log plain', () => {
    log.plain('go', 'ahead');
    expect(console.log).toHaveBeenCalled();
  });

  it('should group and restore indentation', () => {
    const origIndent = log.indent;
    log.group(() => {
      log.info('nested');
      expect(log.indent).not.toEqual(origIndent);
    });
    expect(log.indent).toEqual(origIndent);
  });

  it('should print device info, all branches', () => {
    // With address, with token and autoToken
    log.device({
      id: 'miio:123456',
      metadata: { types: new Set(['miio:type1', 'othertype']), capabilities: new Set(['a', 'b']) },
      management: { model: 'abc', address: 'ip', token: 'tok', autoToken: true }
    });
    // With address, with token and no autoToken
    log.device({
      id: 'miio:78910',
      metadata: { types: new Set(['miio:type1']), capabilities: new Set([]) },
      management: { model: null, address: 'ip', token: 'tok', autoToken: false }
    }, true);
    // With no address, but parent
    log.device({
      id: 'miio:78910',
      metadata: { types: new Set(['type1']), capabilities: new Set([]) },
      management: { address: null, model: 'model1', parent: {id:'par'}, token: null }
    });
    // With no token and no parent
    log.device({
      id: '12345',
      metadata: { types: new Set(['type1']), capabilities: new Set([]) },
      management: { address: 'ip', model: null, parent: null, token: null }
    });
    // With parent and no token
    log.device({
      id: 'miio:23456',
      metadata: { types: new Set(['miio:type1']), capabilities: new Set([]) },
      management: { address: null, model: 'm', parent: {id:'p'}, token: null }
    }, true);

    expect(console.log).toHaveBeenCalled();
  });
});