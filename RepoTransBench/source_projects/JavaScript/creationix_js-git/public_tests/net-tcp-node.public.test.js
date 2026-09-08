const makeChannel = () => {
  // Minimal fake implementation for channels
  const queue = [];
  return {
    put: jest.fn((val) => { queue.push(val); }),
    drain: jest.fn((cb) => setTimeout(cb, 2)),
    take: jest.fn((cb) => setTimeout(() => cb("public"), 2))
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
      setTimeout(cb, 2);
      return c;
    })
  };
});

describe('net/tcp-node public', () => {
  let connect;
  beforeAll(() => {
    connect = require('../net/tcp-node');
  });

  it('throws on missing host/port (public)', () => {
    expect(() => connect(undefined, undefined, () => {})).toThrow(/host and port/);
    expect(() => connect("", 0, () => {})).toThrow(/host and port/);
  });

  it('connects and triggers handlers (public)', (done) => {
    const mockErr = jest.fn();
    const api = connect('127.0.0.1', 9001, mockErr); // different data
    expect(api).toHaveProperty('put');
    expect(api).toHaveProperty('drain');
    expect(api).toHaveProperty('take');
    expect(typeof api.put).toBe('function');
    expect(typeof api.take).toBe('function');
    setTimeout(done, 15);
  });

  it('triggers error handler on error (public)', (done) => {
    const net = require('net');
    const mockErr = jest.fn();
    const origConnect = net.connect;
    net.connect = jest.fn((opts, cb) => {
      const c = origConnect(opts, cb);
      setTimeout(() => {
        try {
          c.emit('error', new Error('public simulated'));
        } catch (e) { /* prevents crash */ }
      }, 3);
      return c;
    });
    connect('127.0.0.1', 9555, mockErr); // different data
    setTimeout(() => {
      expect(mockErr).toHaveBeenCalled();
      net.connect = origConnect;
      done();
    }, 30);
  });
});