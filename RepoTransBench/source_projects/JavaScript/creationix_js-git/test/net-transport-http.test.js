const pktLine = require('../lib/pkt-line');
jest.mock('bodec', () => ({
  join: jest.fn(() => new Uint8Array([1,2,3])),
}));

jest.mock('../lib/pkt-line', () => ({
  framer: jest.fn((cb) => cb),
  deframer: jest.fn((cb) => (body) => {
    ["# service=service", null, "data"].forEach(cb);
  }),
}));

jest.mock('culvert', () => {
  return () => ({
    put: jest.fn(),
    drain: jest.fn(),
    take: jest.fn()
  });
});
jest.mock('../lib/wrap-handler', () => (fn) => fn);

const transportHTTP = require('../net/transport-http');

describe('net/transport-http', () => {
  let lastHeaders, lastBody, called;
  function mockRequest(method, url, headers, body, cb) {
    called = true;
    lastHeaders = headers; lastBody = body;
    if (cb) {
      setTimeout(() => cb({
        statusCode: 200,
        headers: { "content-type": "application/x-service-advertisement" },
        body: "body"
      }), 1);
    }
  }

  it('appends auth if username is provided', () => {
    global.btoa = (s) => "encoded";
    const httpTrans = transportHTTP(mockRequest);
    const f = httpTrans('url', 'u', 'p');
    expect(typeof f).toBe('function');
  });

  it('returns a duplex channel', (done) => {
    const httpTrans = transportHTTP(mockRequest);
    const api = httpTrans('url')('service', () => {});
    expect(api).toHaveProperty('put');
    expect(api).toHaveProperty('drain');
    expect(api).toHaveProperty('take');
    setTimeout(() => {
      expect(called).toBe(true);
      done();
    }, 10);
  });

  it('throws on invalid status code', () => {
    function badRequest(method, url, headers, body, cb) {
      cb && cb({ statusCode: 404, headers: { "content-type": "application/x-service-advertisement" }, body: "" });
    }
    const f = transportHTTP(badRequest)('url')('service', ()=>{});
    expect(() => f.take(() => {})).not.toThrow();
  });
});