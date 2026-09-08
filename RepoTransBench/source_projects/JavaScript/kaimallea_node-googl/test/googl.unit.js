const googl = require('../lib/googl.js');
const assert = require('assert');
const sinon = require('sinon');
const Q = require('q');

describe('unit: googl.js implementation', function() {

  afterEach(() => {
    if (googl.requestStub) {
      googl.request = googl.requestStubOriginal;
      delete googl.requestStub;
      delete googl.requestStubOriginal;
    }
  });

  it('should get and set key correctly', function() {
    const testKey = '1234KEY';
    assert.strictEqual(googl.setKey(testKey), testKey);
    assert.strictEqual(googl.getKey(), testKey);
    assert.strictEqual(googl.setKey(''), '');
    assert.strictEqual(googl.getKey(), '');
  });

  it('_googleRequest rejects when called with no operation', function(done) {
    googl._googleRequest().catch((err) => {
      assert(/Invalid URL/i.test(err.message));
      done();
    });
  });

  it('should reject expand when input is not a goo.gl URL', function(done) {
    googl.expand('http://not-googl.com/abc')
      .catch(err => {
        assert(/Invalid URL/i.test(err.message));
        done();
      });
  });

  it('should handle shorten API error', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 400}, '{"error":"API Broken"}');
    });
    googl.request = googl.requestStub;

    googl.shorten('http://valid.com').catch(err => {
      assert(/API Broken/.test(err.message) || err);
      done();
    });
  });

  it('should handle expand API error', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 400}, '{"error":"API Broken"}');
    });
    googl.request = googl.requestStub;

    googl.expand('http://goo.gl/foo').catch(err => {
      assert(/API Broken/.test(err.message) || err);
      done();
    });
  });

  it('should resolve for a successful shorten', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 200}, '{"id":"http://goo.gl/bar"}');
    });
    googl.request = googl.requestStub;

    googl.shorten('http://valid.com').then((res) => {
      assert.strictEqual(res.id, 'http://goo.gl/bar');
      done();
    });
  });

  it('should resolve for a successful expand', function(done) {
    googl.requestStubOriginal = googl.request;
    googl.requestStub = sinon.stub().callsFake((opts, cb) => {
      cb(null, {statusCode: 200}, '{"longUrl":"http://long.com/foo"}');
    });
    googl.request = googl.requestStub;

    googl.expand('http://goo.gl/bar').then((res) => {
      assert.strictEqual(res.longUrl, 'http://long.com/foo');
      done();
    });
  });
});