"use strict";

jest.mock('culvert', () => {
  return () => ({
    put: jest.fn(),
    drain: jest.fn(),
    take: jest.fn(),
  });
});
jest.mock('../lib/wrap-handler', () => (fn) => fn);
global.window = global.window || { chrome: { sockets: { tcp: {} }, runtime: {} } };

// Mocks for window.chrome.sockets.tcp and chrome.runtime
window.chrome.sockets.tcp = {
  onReceive: { addListener: jest.fn() },
  onReceiveError: { addListener: jest.fn() },
  create: jest.fn(),
  connect: jest.fn(),
  getInfo: jest.fn(),
  setPaused: jest.fn(),
  close: jest.fn(),
  send: jest.fn(),
};
window.chrome.runtime = { lastError: { message: "test-error-public" } };

const connect = require('../net/tcp-chrome-sockets');

describe('net/tcp-chrome-sockets public', () => {
  beforeEach(() => {
    // Reset all mock calls
    for (let fn in window.chrome.sockets.tcp) {
      if (window.chrome.sockets.tcp[fn].mockClear) window.chrome.sockets.tcp[fn].mockClear();
    }
  });

  it('throws on missing host/port (public)', () => {
    expect(() => connect(undefined, undefined, () => {})).toThrow(/host and port/);
    expect(() => connect("", 0, () => {})).toThrow(/host and port/);
  });

  it('calls create and listeners (public)', () => {
    // Prepare mocks to call listeners
    let errorCalled = false;
    const onError = jest.fn(() => { errorCalled = true; });
    window.chrome.sockets.tcp.create.mockImplementation((cb) => cb && cb({ socketId: 200 }));
    window.chrome.sockets.tcp.connect.mockImplementation((sid, host, port, cb) => cb && cb(2)); // non-error
    window.chrome.sockets.tcp.getInfo.mockImplementation((sid, cb) => cb && cb({ connected: true }));
    connect("pubhost", 2345, onError);
    expect(window.chrome.sockets.tcp.create).toHaveBeenCalled();
  });
});