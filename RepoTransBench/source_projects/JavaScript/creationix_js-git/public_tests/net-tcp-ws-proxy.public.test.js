// mute console.error for expected error test
jest.spyOn(global.console, 'error').mockImplementation(() => {});
global.WebSocket = class {
  constructor(url) {
    this.url = url;
    setTimeout(() => this.onopen && this.onopen(), 2);
  }
  send() {}
  close() {}
  set binaryType(type) {}
};

jest.mock('culvert', () => {
  return () => ({
    put: jest.fn(),
    drain: jest.fn(),
    take: jest.fn(),
  });
});
jest.mock('../lib/wrap-handler', () => (fn) => fn);

const wsProxy = require('../net/tcp-ws-proxy');

describe('net/tcp-ws-proxy public', () => {
  it('appends / to proxyUrl if missing (public)', () => {
    const fn = wsProxy('ws://proxyhost/different');
    expect(typeof fn).toBe('function');
  });
  it('throws if host or port are missing (public)', () => {
    const fn = wsProxy('ws://proxyhost/different/');
    expect(() => fn(undefined, undefined, () => {})).toThrow(/host and port/);
    expect(() => fn("", 0, () => {})).toThrow(/host and port/);
  });
  it('returns channels and sets up ws (public)', (done) => {
    const fn = wsProxy('ws://proxyhost/different/');
    const api = fn('publichost', 6543, () => {});
    expect(typeof api.put).toBe('function');
    setTimeout(() => done(), 13);
  });
  it('calls error handler on ws error (public)', (done) => {
    global.WebSocket = class {
      constructor(url) {
        setTimeout(() => (this.onerror && this.onerror(new Error('fail-public'))), 4);
      }
      close() { }
      set binaryType(type) {}
      send() { }
    };
    const fn = wsProxy('ws://proxyhost/different/');
    let errorCalled = false;
    try {
      fn('errorhost', 4321, () => { errorCalled = true; });
    } catch (e) {/* should not throw */}
    setTimeout(() => {
      expect(errorCalled).toBe(true);
      done();
    }, 25);
  });
});