const expressJwtAuthz = require('../lib/index');
const assert = require('assert');

describe('express-jwt-authz PUBLIC - different scopes/data', () => {
  let req, res, next;

  beforeEach(() => {
    req = {};
    res = {
      statusCode: null,
      headers: {},
      body: null,
      status(code) {
        this.statusCode = code;
        return this;
      },
      send(val) {
        this.body = val;
        return this;
      },
      append(header, value) {
        this.headers[header] = value;
      },
    };
    next = function (err) {
      next.called = true;
      next.error = err;
    };
    next.called = false;
    next.error = null;
  });

  it('should call next if user has one of the expected scopes (with different scope)', () => {
    req.user = { scope: 'read:books download:magazines modify:articles' };
    const mw = expressJwtAuthz(['download:magazines', 'delete:books']);
    mw(req, res, next);
    assert(next.called, 'should call next');
    assert.strictEqual(next.error, null);
  });

  it('should return error if user does not have any of the required scopes (diff)', () => {
    req.user = { scope: 'list:authors read:docs' };
    const mw = expressJwtAuthz(['download:books']);
    mw(req, res, next);
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(res.body, 'Insufficient scope');
    assert.ok(res.headers['WWW-Authenticate']);
  });

  it('should accept array-based user scopes and checkAllScopes (diff)', () => {
    req.user = { scope: ['publish:news', 'edit:news', 'share:news'] };
    const mw = expressJwtAuthz(['publish:news', 'edit:news'], { checkAllScopes: true });
    mw(req, res, next);
    assert(next.called, 'should call next');
    assert.strictEqual(next.error, null);
  });

  it('should not allow access if not all scopes are present with checkAllScopes (diff)', () => {
    req.user = { scope: ['manage:users', 'edit:accounts'] };
    const mw = expressJwtAuthz(['manage:users', 'admin:users'], { checkAllScopes: true });
    mw(req, res, next);
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(res.body, 'Insufficient scope');
  });

  it('should use custom user key (diff)', () => {
    req.customUser = { scope: 'contribute:photos' };
    const mw = expressJwtAuthz(['contribute:photos'], { customUserKey: 'customUser' });
    mw(req, res, next);
    assert(next.called, 'should call next');
    assert.strictEqual(next.error, null);
  });

  it('should use custom scope key (diff)', () => {
    req.user = { customScope: 'admin:settings' };
    const mw = expressJwtAuthz(['admin:settings'], { customScopeKey: 'customScope' });
    mw(req, res, next);
    assert(next.called, 'should call next');
    assert.strictEqual(next.error, null);
  });

  it('should fail with error if no user on req (diff)', () => {
    const mw = expressJwtAuthz(['edit:profile'], { failWithError: true });
    mw(req, res, next);
    assert(next.called);
    assert(next.error);
    assert.strictEqual(next.error.statusCode, 403);
    assert.strictEqual(next.error.message, 'Insufficient scope');
  });

  it('should succeed if expectedScopes is an empty array (diff)', () => {
    req.user = { scope: 'some:random:scope' };
    const mw = expressJwtAuthz([]);
    mw(req, res, next);
    assert(next.called);
    assert.strictEqual(next.error, null);
  });

  it('should throw if expectedScopes is not an array (diff)', () => {
    assert.throws(() => expressJwtAuthz('notArray'), /expectedScopes must be an array/);
  });

  it('should return error if user scope is not a string or array (diff)', () => {
    req.user = { scope: 42 };
    const mw = expressJwtAuthz(['write:something']);
    mw(req, res, next);
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(res.body, 'Insufficient scope');
  });
});