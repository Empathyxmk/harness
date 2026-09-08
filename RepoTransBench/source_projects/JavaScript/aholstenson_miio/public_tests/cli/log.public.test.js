const log = require('../../cli/log');

// Mock the console output
beforeEach(() => {
  jest.spyOn(global.console, 'log').mockImplementation(() => {});
});
afterEach(() => {
  global.console.log.mockRestore();
});

describe('cli/log public', () => {
  it('should log info with different words', () => {
    log.info('foo', 'bar', 'baz');
    expect(console.log).toHaveBeenCalled();
  });

  it('should log error with alternate message', () => {
    log.error('unexpected', 'problem');
    expect(console.log).toHaveBeenCalled();
  });

  it('should log warn with alternate text', () => {
    log.warn('alert', 'now');
    expect(console.log).toHaveBeenCalled();
  });

  it('should log plain with alternate values', () => {
    log.plain('simple', 'output');
    expect(console.log).toHaveBeenCalled();
  });

  it('should group and restore indentation (public)', () => {
    const origIndent = log.indent;
    log.group(() => {
      log.warn('inside group');
      expect(log.indent).not.toEqual(origIndent);
    });
    expect(log.indent).toEqual(origIndent);
  });

  it('should print device info, all public branches', () => {
    // With address, with token and autoToken = false
    log.device({
      id: 'miio:654321',
      metadata: { types: new Set(['miio:type2', 'othertype2']), capabilities: new Set(['x', 'y']) },
      management: { model: 'xyz', address: 'otherip', token: 'tok2', autoToken: false }
    });
    // With address, with token and autoToken true, and test true flag
    log.device({
      id: 'miio:888888',
      metadata: { types: new Set(['miio:type99']), capabilities: new Set(['cap']) },
      management: { model: '', address: 'otherip', token: 'tok3', autoToken: true }
    }, true);
    // With no address, but parent
    log.device({
      id: 'miio:222222',
      metadata: { types: new Set(['typeX']), capabilities: new Set(['c1']) },
      management: { address: null, model: 'modelX', parent: {id:'parent1'}, token: null }
    });
    // With no token and no parent
    log.device({
      id: '54321',
      metadata: { types: new Set(['typeX']), capabilities: new Set([]) },
      management: { address: 'otherip', model: null, parent: null, token: null }
    });
    // With parent and no token
    log.device({
      id: 'miio:33333',
      metadata: { types: new Set(['miio:typeQ']), capabilities: new Set(['q1']) },
      management: { address: null, model: 'mm', parent: {id:'pp'}, token: null }
    }, true);
    expect(console.log).toHaveBeenCalled();
  });
});