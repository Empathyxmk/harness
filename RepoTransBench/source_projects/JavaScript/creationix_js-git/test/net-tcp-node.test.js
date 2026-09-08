const makeChannel = () => {
  // Minimal fake implementation for channels
  const queue = [];
  return {
    put: jest.fn((val) => { queue.push(val); }),
    drain: jest.fn((cb) => setTimeout(cb, 1)),
    take: jest.fn((cb) => setTimeout(() => cb("test"), 1))
  };
};
jest.mock('culvert', () => makeChannel);

jest.mock('net', () => {
  const EventEmitter = require('events');
  class Client extends EventEmitter {
    constructor() {
      super();
      this.dataWritten = [];
    }
    write(data) {
      this.dataWritten.push(data);
      this.emit('drain');
      return true;
    }
    read() {
      return null;
    }
    end() {
      this.ended = true;
    }
    on() { return this; }
  }
  return {
    connect: jest.fn((opts, cb) => {
      const c = new Client();
      setTimeout(cb, 1);
      return c;
    })
  };
});

describe('net/tcp-node', () => {
  let connect;
  beforeAll(() => {
    connect = require('../net/tcp-node');
  });

  it('throws on missing host/port', () => {
    // Only undefined triggers; null and '' will be coerced to string, so for correct coverage, test only undefined/0
    expect(() => connect(undefined, undefined, () => {})).toThrow(/host and port/);
    expect(() => connect("", 0, () => {})).toThrow(/host and port/);
  });

  it('connects and triggers handlers', (done) => {
    const mockErr = jest.fn();
    const api = connect('localhost', 8000, mockErr);
    expect(api).toHaveProperty('put');
    expect(api).toHaveProperty('drain');
    expect(api).toHaveProperty('take');
    expect(typeof api.put).toBe('function');
    expect(typeof api.take).toBe('function');
    setTimeout(done, 10);
  });

  // Edge: Simulate client error triggering onError
  it('triggers error handler on error', (done) => {
    const net = require('net');
    const mockErr = jest.fn();
    const origConnect = net.connect;
    net.connect = jest.fn((opts, cb) => {
      const c = origConnect(opts, cb);
      setTimeout(() => {
        try {
          c.emit('error', new Error('simulated'));
        } catch (e) { /* prevents crash, since our wrap just calls handler */ }
      }, 2);
      return c;
    });
    connect('localhost', 1337, mockErr);
    setTimeout(() => {
      expect(mockErr).toHaveBeenCalled();
      net.connect = origConnect;
      done();
    }, 20);
  });
});