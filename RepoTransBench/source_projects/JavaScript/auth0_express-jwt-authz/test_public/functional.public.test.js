const expressJwtAuthz = require('../lib/index');
const assert = require('assert');

describe('express-jwt-authz functional PUBLIC - alternate user/scope scenarios', () => {
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

  it('should allow with multiple user scopes string if one matches (different)', () => {
    req.user = { scope: 'export:pdf generate:csv list:files' };
    const mw = expressJwtAuthz(['generate:csv']);
    mw(req, res, next);
    assert(next.called);
    assert.strictEqual(next.error, null);
  });

  it('should reject when no scope matches expected (different)', () => {
    req.user = { scope: 'preview:doc upload:img' };
    const mw = expressJwtAuthz(['deploy:service']);
    mw(req, res, next);
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(res.body, 'Insufficient scope');
  });

  it('should handle array-in-scope user with checkAllScopes true (different)', () => {
    req.user = { scope: ['edit:blog', 'update:blog'] };
    const mw = expressJwtAuthz(['edit:blog', 'update:blog'], { checkAllScopes: true });
    mw(req, res, next);
    assert(next.called);
  });

  it('should fail with error and failWithError when scopes missing (different)', () => {
    req.user = { scope: ['access:repo', 'pull:repo'] };
    const mw = expressJwtAuthz(['release:repo'], { failWithError: true });
    mw(req, res, next);
    assert(next.called);
    assert(next.error);
    assert.strictEqual(next.error.statusCode, 403);
    assert.strictEqual(next.error.message, 'Insufficient scope');
  });

  it('should respect customScopeKey in user object (different)', () => {
    req.user = { myScopes: 'accept:invite remove:invite' };
    const mw = expressJwtAuthz(['accept:invite'], { customScopeKey: 'myScopes' });
    mw(req, res, next);
    assert(next.called);
    assert.strictEqual(next.error, null);
  });

  it('should respect customUserKey in user (different)', () => {
    req.account = { scope: 'claim:rewards' };
    const mw = expressJwtAuthz(['claim:rewards'], { customUserKey: 'account' });
    mw(req, res, next);
    assert(next.called);
  });

  it('should call next if expectedScopes is empty and no user (different)', () => {
    const mw = expressJwtAuthz([]);
    mw(req, res, next);
    assert(next.called);
    assert.strictEqual(next.error, null);
  });

  it('should error if user scope is null/invalid type (different)', () => {
    req.user = { scope: { admin: true } };
    const mw = expressJwtAuthz(['admin:all']);
    mw(req, res, next);
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(res.body, 'Insufficient scope');
  });

  it('should throw error if expectedScopes is not array (different)', () => {
    assert.throws(() => expressJwtAuthz('foo:bar'), /expectedScopes must be an array/);
  });

  it('should return error if user key missing (different)', () => {
    const mw = expressJwtAuthz(['share:photos']);
    mw(req, res, next);
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(res.body, 'Insufficient scope');
  });
});