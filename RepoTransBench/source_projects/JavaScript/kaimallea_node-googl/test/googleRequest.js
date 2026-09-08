const googl = require('../lib/googl.js');
const assert = require('assert');
const sinon = require('sinon');

describe('_googleRequest', function() {
  afterEach(() => {
    if (googl.requestStub) {
      googl.request = googl.requestStubOriginal;
      delete googl.requestStub;
      delete googl.requestStubOriginal;
    }
  });

  it('should reject invalid operation', function(done) {
    googl._googleRequest().catch(err => {
      assert(/Invalid URL/i.test(err.message));
      done();
    });
  });

  it('should handle API 400 error', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 400}, '{"error":"Bad"}');
    });
    googl.request = googl.requestStub;
    googl._googleRequest('shorten', 'http://x').catch(e => {
      assert(/Bad/.test(e.message));
      done();
    });
  });

  it('should parse success response', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 200}, '{"id":"s"}');
    });
    googl.request = googl.requestStub;
    googl._googleRequest('shorten', 'http://x').then(res => {
      assert.strictEqual(res.id, 's');
      done();
    });
  });
});