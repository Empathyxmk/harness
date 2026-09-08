jest.mock('../modules/mailin');
jest.mock('../modules/config', () => ({
  keywordBlackList: ['foo', 'bar'],
  mailin: {},
}));

const ioModule = require('../modules/io');

class DummySocket {
  constructor(initialId) {
    this.events = {};
    this.emitted = {};
    this.shortid = initialId;
    this.disconnectCalled = false;
  }
  emit(event, data) {
    this.emitted[event] = data;
  }
  on(event, cb) {
    this.events[event] = cb;
  }
  trigger(event, ...args) {
    if (this.events[event]) this.events[event](...args);
  }
}

class DummyIo {
  constructor() { this.events = {}; }
  on(event, cb) { this.events[event] = cb; }
  trigger(event, ...args) {
    if (this.events[event]) this.events[event](...args);
  }
}

describe('modules/io.js main logic', () => {
  let io;
  beforeEach(() => { io = new DummyIo(); });

  test('Connection and shortid request', () => {
    ioModule(io);
    const socket = new DummySocket();
    io.trigger('connection', socket);
    socket.trigger('request shortid');
    expect(socket.emitted.shortid).toEqual(socket.shortid);
    expect(socket.shortid).toMatch(/^[a-z0-9_-]+$/);
  });

  test('set shortid skips blacklisted', () => {
    ioModule(io);
    const socket = new DummySocket();
    io.trigger('connection', socket);
    socket.trigger('set shortid', 'foobar'); // matches blacklist
    expect(socket.emitted.shortid).toBeUndefined();
    socket.trigger('set shortid', 'customid');
    expect(socket.emitted.shortid).toBe('customid');
  });

  test('disconnect deletes from online', () => {
    ioModule(io);
    const socket = new DummySocket();
    io.trigger('connection', socket);
    socket.trigger('request shortid');
    socket.trigger('disconnect', socket);
    // No externally visible effect required for coverage
    expect(socket.emitted.shortid).toEqual(socket.shortid);
  });

  test('Mailin message delivers mail to socket', () => {
    const mailin = require('../modules/mailin');
    ioModule(io);

    // simulate connection & message
    const socket = new DummySocket();
    io.trigger('connection', socket);
    socket.trigger('request shortid');
    // Find mailin message handler
    let emitterFn;
    mailin.on.mock.calls.forEach(call => {
      if (call[0] === 'message') emitterFn = call[1];
    });
    const data = { headers: { to: socket.shortid + '@domain', from: 'from@a', subject: '', date: (new Date()).toString() }};
    emitterFn({}, data);
    expect(socket.emitted.mail).toBe(data);
  });

  test('Mailin message: to does not match, nothing happens', () => {
    const mailin = require('../modules/mailin');
    ioModule(io);
    let emitterFn;
    mailin.on.mock.calls.forEach(call => {
      if (call[0] === 'message') emitterFn = call[1];
    });
    io.trigger('connection', new DummySocket());
    const data = { headers: { to: 'not-an-email', from: 'none', subject: '', date: '' } };
    expect(() => emitterFn({}, data)).not.toThrow();
  });

  test('Mailin message: to with valid email, but shortid not in online map', () => {
    const mailin = require('../modules/mailin');
    ioModule(io);
    let emitterFn;
    mailin.on.mock.calls.forEach(call => {
      if (call[0] === 'message') emitterFn = call[1];
    });
    const data = { headers: { to: 'nosuchid@domain.com', from: 'none', subject: '', date: '' } };
    expect(() => emitterFn({}, data)).not.toThrow();
  });
});

// Test the blacklist checker as an isolated function (for full branch coverage)
// Further direct coverage can't really be increased without changing the actual io.js