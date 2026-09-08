const expect = require('chai').expect;
const jwtAuthz = require('../lib');

describe('jwtAuthz functional behavior', () => {
  it('calls next immediately if expectedScopes is empty', done => {
    const req = { user: { scope: 'read:user' } };
    jwtAuthz([])(req, {}, done);
  });

  it('allows when some expectedScopes are in user.scope (as string)', done => {
    const req = { user: { scope: 'read:user write:user' } };
    jwtAuthz(['write:user'])(req, {}, done);
  });

  it('allows when some expectedScopes are in user.scope (as array)', done => {
    const req = { user: { scope: ['read:user', 'write:user'] } };
    jwtAuthz(['write:user'])(req, {}, done);
  });

  it('allows when all expectedScopes are present with checkAllScopes', done => {
    const req = { user: { scope: 'read write' } };
    jwtAuthz(['read', 'write'], { checkAllScopes: true })(req, {}, done);
  });

  it('denies when not all expectedScopes present and checkAllScopes is true', () => {
    const req = { user: { scope: 'read' } };
    const res = {
      status(code) {
        expect(code).to.equal(403);
        return {
          send(msg) { expect(msg).to.equal('Insufficient scope'); }
        };
      },
      append(key, value) {
        expect(key).to.equal('WWW-Authenticate');
        expect(value).to.match(/scope="read write"/);
      }
    };
    jwtAuthz(['read', 'write'], { checkAllScopes: true })(req, res);
  });

  it('supports customScopeKey with string', done => {
    const req = { user: { permissions: 'admin' } };
    jwtAuthz(['admin'], { customScopeKey: 'permissions' })(req, {}, done);
  });

  it('supports customScopeKey with array', done => {
    const req = { user: { roles: ['admin', 'manager'] } };
    jwtAuthz(['manager'], { customScopeKey: 'roles' })(req, {}, done);
  });

  it('supports customUserKey', done => {
    const req = { account: { scope: 'foo' } };
    jwtAuthz(['foo'], { customUserKey: 'account' })(req, {}, done);
  });

  it('error if customUserKey not object', () => {
    const req = { notUser: 42 };
    const res = {
      status(code) {
        expect(code).to.equal(403);
        return {
          send(msg) { expect(msg).to.equal('Insufficient scope'); }
        };
      },
      append(key, value) {
        expect(key).to.equal('WWW-Authenticate');
        expect(value).to.match(/scope="foo"/);
      }
    };
    jwtAuthz(['foo'], { customUserKey: 'notUser' })(req, res);
  });

  it('next() called on allowed even if failWithError true', done => {
    const req = { user: { scope: 'foo' } };
    jwtAuthz(['foo'], { failWithError: true })(req, {}, done);
  });

  it('multiple scopes, checkAllScopes false, at least one matches', done => {
    const req = { user: { scope: 'admin operator' } };
    jwtAuthz(['admin', 'user'])(req, {}, done);
  });
});