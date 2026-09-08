const googl = require('../lib/googl.js');
const assert = require('assert');
const sinon = require('sinon');

describe('shorten', function() {
  afterEach(() => {
    if (googl.requestStub) {
      googl.request = googl.requestStubOriginal;
      delete googl.requestStub;
      delete googl.requestStubOriginal;
    }
  });

  it('should successfully shorten a url', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 200}, '{"id":"http://goo.gl/xyz"}');
    });
    googl.request = googl.requestStub;

    googl.shorten('http://longurl.com').then(res => {
      assert.strictEqual(res.id, 'http://goo.gl/xyz');
      done();
    });
  });

  it('should handle API error', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 400}, '{"error":"Error"}');
    });
    googl.request = googl.requestStub;
    googl.shorten('http://longurl.com').catch(e => {
      assert(/Error/.test(e.message));
      done();
    });
  });
});