const { expect } = require('chai');
const path = require('path');

describe('passport-google-oauth (package main) [PUBLIC]', function () {
  const LIB_PATH = path.resolve(__dirname, '../lib/index.js');
  let originalRequire;

  beforeEach(() => {
    originalRequire = module.constructor.prototype.require;
  });

  afterEach(() => {
    module.constructor.prototype.require = originalRequire;
    delete require.cache[require.resolve(LIB_PATH)];
    try { delete require.cache[require.resolve('passport-google-oauth1')]; } catch (e) {}
    try { delete require.cache[require.resolve('passport-google-oauth20')]; } catch (e) {}
  });

  it('allows require and exports different mock strategies when both peer deps are present', function () {
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') return 'public-mock-oauth1-main';
      if (id === 'passport-google-oauth20') return 'public-mock-oauth2-main';
      return originalRequire.call(this, id);
    };
    const entry = require(LIB_PATH);
    expect(entry.Strategy).to.equal('public-mock-oauth1-main');
    expect(entry.OAuthStrategy).to.equal('public-mock-oauth1-main');
    expect(entry.OAuth2Strategy).to.equal('public-mock-oauth2-main');
  });

  it('throws custom error if passport-google-oauth1 is absent [public]', function () {
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') {
        let e = new Error('PUBLIC_MODULE_NOT_FOUND_OAUTH1');
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      }
      if (id === 'passport-google-oauth20') return 'public-mock-oauth2-main';
      return originalRequire.call(this, id);
    };
    expect(() => require(LIB_PATH)).to.throw(/must be installed/i);
  });

  it('throws custom error if passport-google-oauth20 is absent [public]', function () {
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') return 'public-mock-oauth1-main';
      if (id === 'passport-google-oauth20') {
        let e = new Error('PUBLIC_MODULE_NOT_FOUND_OAUTH2');
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      }
      return originalRequire.call(this, id);
    };
    expect(() => require(LIB_PATH)).to.throw(/must be installed/i);
  });
});