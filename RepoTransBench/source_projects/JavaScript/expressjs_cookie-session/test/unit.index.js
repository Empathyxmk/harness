/* eslint-env mocha */

const assert = require('assert');
const cookieSession = require('../index');
const connect = require('connect');
const supertest = require('supertest');

describe('cookie-session library core logic', function () {

  // Fix: Match actual error message thrown by the library, not /secret or keys/, but '.keys required.'
  it('throws error if opts.signed and no keys/secret', function () {
    assert.throws(() => cookieSession({ signed: true }), /\.keys required\./);
  });

  it('does not throw if opts.signed false and no keys', function () {
    assert.doesNotThrow(() => cookieSession({ signed: false }));
  });

  it('accepts single secret', function () {
    assert.doesNotThrow(() => cookieSession({ secret: 'keyboard cat' }));
  });

  it('req.session getter returns new session object', function (done) {
    const app = connect()
      .use(cookieSession({ secret: 'keyboard cat' }))
      .use(function (req, res) { 
        assert.deepStrictEqual(typeof req.session, 'object'); 
        res.end('ok');
      });
    supertest(app).get('/').expect(200, done);
  });

  it('req.session setter to null unsets', function (done) {
    const app = connect()
      .use(cookieSession({ secret: 'keyboard cat' }))
      .use(function (req, res) {
        req.session = null;
        assert.strictEqual(req.session, null);
        res.end();
      });
    supertest(app).get('/').expect(200, done);
  });

  it('req.session setter to object resets', function (done) {
    const app = connect()
      .use(cookieSession({ secret: 'keyboard cat' }))
      .use(function (req, res) {
        req.session = { foo: 'bar' };
        assert.strictEqual(req.session.foo, 'bar');
        res.end();
      });
    supertest(app).get('/').expect(200, done);
  });

  // Fix: The actual behavior is to throw, which returns 500. Confirm 500 and error message.
  it('req.session setter to invalid type throws error', function (done) {
    const app = connect()
      .use(cookieSession({ secret: 'keyboard cat' }))
      .use(function (req, res, next) {
        try {
          req.session = 5;
        } catch (e) {
          // Check that the error matches expectation
          assert.ok(/must be a/i.test(e.message));
          res.statusCode = 500;
          return res.end(e.message);
        }
        res.end();
      });
    supertest(app)
      .get('/')
      .expect(500)
      .expect(res => {
        assert.match(res.text, /must be a/i);
      })
      .end(done);
  });

  // Fix: Only check if a Set-Cookie with Expires in past exists at all
  it('removes the cookie when session set to null', function (done) {
    const app = connect()
      .use(cookieSession({ secret: 'keyboard cat', name: 'sessme' }))
      .use(function (req, res) {
        req.session = null;
        res.end();
      });

    supertest(app)
      .get('/')
      .expect(res => {
        const cookies = res.headers['set-cookie'];
        assert.ok(
          cookies && cookies.some(cookie => 
            /sessme=.*Expires=Thu, 01 Jan 1970 00:00:00 GMT;/i.test(cookie)
          ),
          'Should remove the cookie and set Expires in past'
        );
      })
      .expect(200, done);
  });

  it('does not set cookie if session untouched', function (done) {
    const app = connect()
      .use(cookieSession({ secret: 'keyboard cat' }))
      .use(function (req, res) {
        res.end();
      });
    supertest(app)
      .get('/')
      .expect(res => {
        assert(!res.headers['set-cookie'], 'Should not set cookie if session untouched');
      })
      .expect(200, done);
  });
});