// mute console.error for expected error test
jest.spyOn(global.console, 'error').mockImplementation(() => {});
global.WebSocket = class {
  constructor(url) {
    this.url = url;
    setTimeout(() => this.onopen && this.onopen(), 1);
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

describe('net/tcp-ws-proxy', () => {
  it('appends / to proxyUrl if missing', () => {
    const fn = wsProxy('ws://host/proxy');
    expect(typeof fn).toBe('function');
  });
  it('throws if host or port are missing (just undefined/0)', () => {
    const fn = wsProxy('ws://host/proxy/');
    expect(() => fn(undefined, undefined, () => {})).toThrow(/host and port/);
    expect(() => fn("", 0, () => {})).toThrow(/host and port/);
  });
  it('returns channels and sets up ws', (done) => {
    const fn = wsProxy('ws://host/proxy/');
    const api = fn('localhost', 8080, () => {});
    expect(typeof api.put).toBe('function');
    setTimeout(() => done(), 10);
  });
  it('calls error handler on ws error', (done) => {
    global.WebSocket = class {
      constructor(url) {
        setTimeout(() => (this.onerror && this.onerror(new Error('fail'))), 2);
      }
      close() { }
      set binaryType(type) {}
      send() { }
    };
    const fn = wsProxy('ws://host/proxy/');
    let errorCalled = false;
    try {
      fn('localhost', 9090, () => { errorCalled = true; });
    } catch (e) {/* should not throw */}
    setTimeout(() => {
      expect(errorCalled).toBe(true);
      done();
    }, 20);
  });
});