const { expect } = require('chai');
const path = require('path');

function clearModule(modulePath) {
  delete require.cache[require.resolve(modulePath)];
}

describe('lib/index.js [PUBLIC]', function () {
  let LIB_PATH = path.resolve(__dirname, '../../lib/index.js');
  let originalRequire;

  beforeEach(() => {
    originalRequire = module.constructor.prototype.require;
  });

  afterEach(() => {
    module.constructor.prototype.require = originalRequire;
    clearModule(LIB_PATH);
    try { clearModule('passport-google-oauth1'); } catch (e) {}
    try { clearModule('passport-google-oauth20'); } catch (e) {}
  });

  it('exports public Strategy, OAuthStrategy, and OAuth2Strategy when both peer deps are present', function () {
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') return 'public-mock-oauth1';
      if (id === 'passport-google-oauth20') return 'public-mock-oauth2';
      return originalRequire.call(this, id);
    };
    const entry = require(LIB_PATH);
    expect(entry.Strategy).to.equal('public-mock-oauth1');
    expect(entry.OAuthStrategy).to.equal('public-mock-oauth1');
    expect(entry.OAuth2Strategy).to.equal('public-mock-oauth2');
  });

  it('throws if passport-google-oauth1 is missing (public test)', function () {
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth20') return 'public-mock-oauth2';
      if (id === 'passport-google-oauth1') {
        let e = new Error('Cannot find PUBLIC_OAUTH1');
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      }
      return originalRequire.call(this, id);
    };
    expect(() => require(LIB_PATH)).to.throw(/passport-google-oauth1/);
  });

  it('throws if passport-google-oauth20 is missing (public test)', function () {
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') return 'public-mock-oauth1';
      if (id === 'passport-google-oauth20') {
        let e = new Error('Cannot find PUBLIC_OAUTH20');
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      }
      return originalRequire.call(this, id);
    };
    expect(() => require(LIB_PATH)).to.throw(/passport-google-oauth20/);
  });
});