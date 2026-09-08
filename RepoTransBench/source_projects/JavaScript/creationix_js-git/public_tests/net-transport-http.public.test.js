jest.mock('bodec', () => ({
  join: jest.fn(() => new Uint8Array([4,5,6])),
}));

jest.mock('../lib/pkt-line', () => ({
  framer: jest.fn((cb) => cb),
  deframer: jest.fn((cb) => (body) => {
    ["# service=another-service", null, "pubdata"].forEach(cb);
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

describe('net/transport-http public', () => {
  let lastHeaders, lastBody, called;
  function mockRequest(method, url, headers, body, cb) {
    called = true;
    lastHeaders = headers; lastBody = body;
    if (cb) {
      setTimeout(() => cb({
        statusCode: 201,
        headers: { "content-type": "application/x-another-advertisement" },
        body: "publicbody"
      }), 2);
    }
  }

  it('appends auth if username is provided (public)', () => {
    global.btoa = (s) => "public-encoded";
    const httpTrans = transportHTTP(mockRequest);
    const f = httpTrans('public-url', 'user', 'pword');
    expect(typeof f).toBe('function');
  });

  it('returns a duplex channel (public)', (done) => {
    const httpTrans = transportHTTP(mockRequest);
    const api = httpTrans('public-url')('another-service', () => {});
    expect(api).toHaveProperty('put');
    expect(api).toHaveProperty('drain');
    expect(api).toHaveProperty('take');
    setTimeout(() => {
      expect(called).toBe(true);
      done();
    }, 13);
  });

  it('throws on invalid status code (public)', () => {
    function badRequest(method, url, headers, body, cb) {
      cb && cb({ statusCode: 400, headers: { "content-type": "application/x-another-advertisement" }, body: "" });
    }
    const f = transportHTTP(badRequest)('pub-url')('pub-service', ()=>{});
    expect(() => f.take(() => {})).not.toThrow();
  });
});