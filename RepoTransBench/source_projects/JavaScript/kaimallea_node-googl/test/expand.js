const googl = require('../lib/googl.js');
const assert = require('assert');
const sinon = require('sinon');

describe('expand', function() {
  afterEach(() => {
    if (googl.requestStub) {
      googl.request = googl.requestStubOriginal;
      delete googl.requestStub;
      delete googl.requestStubOriginal;
    }
  });

  it('should reject if not a goo.gl url', function(done) {
    googl.expand('http://example.com').catch(e => {
      assert(/Invalid URL/i.test(e.message));
      done();
    });
  });

  it('should expand a valid goo.gl url', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 200}, '{"longUrl":"http://expanded.com"}');
    });
    googl.request = googl.requestStub;
    googl.expand('http://goo.gl/abc').then(res => {
      assert.strictEqual(res.longUrl, 'http://expanded.com');
      done();
    });
  });
});