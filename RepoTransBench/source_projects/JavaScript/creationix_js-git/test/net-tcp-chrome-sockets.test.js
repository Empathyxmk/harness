global.window = {
  chrome: {
    sockets: {
      tcp: {
        onReceive: { addListener: jest.fn() },
        onReceiveError: { addListener: jest.fn() },
        create: jest.fn((cb) => setTimeout(() => cb({ socketId: 1 }), 1)),
        connect: jest.fn((id, host, port, cb) => setTimeout(() => cb(0), 1)),
        getInfo: jest.fn((socketId, cb) => setTimeout(() => cb({ connected: true }), 1)),
        setPaused: jest.fn(),
        close: jest.fn(),
        send: jest.fn((socketId, buf, cb) => setTimeout(() => cb({ resultCode: 1 }), 1)),
      }
    },
    runtime: { lastError: { message: "err" } }
  }
};

jest.mock('culvert', () => {
  return () => ({
    put: jest.fn(),
    drain: jest.fn(),
    take: jest.fn()
  });
});
jest.mock('../lib/wrap-handler', () => (fn) => fn);

const connect = require('../net/tcp-chrome-sockets');

describe('net/tcp-chrome-sockets', () => {
  it('throws on fully missing host/port (undefined/undefined)', () => {
    expect(() => connect(undefined, undefined, () => {})).toThrow(/host and port/);
  });
  it('returns expected api and starts process', (done) => {
    const api = connect('localhost', 1234, () => {});
    expect(api).toHaveProperty('put');
    expect(api).toHaveProperty('drain');
    expect(api).toHaveProperty('take');
    expect(typeof api.take).toBe('function');
    setTimeout(() => done(), 10);
  });
  it('calls error handler if connect returns <0', (done) => {
    // test error path: simulate chrome.sockets.tcp.connect error (<0 result)
    window.chrome.sockets.tcp.connect = jest.fn((id, host, port, cb) => setTimeout(() => cb(-1), 1));
    let errorCall = false;
    connect('localhost', 4321, () => { errorCall = true; });
    setTimeout(() => {
      expect(errorCall).toBeTruthy();
      done();
    }, 15);
  });
});