const { expect } = require('chai');
const path = require('path');

/**
 * Helper to clear the require cache for a given module
 */
function clearModule(modulePath) {
  delete require.cache[require.resolve(modulePath)];
}

describe('lib/index.js', function () {
  let LIB_PATH = path.resolve(__dirname, '../../lib/index.js');
  let originalRequire;

  beforeEach(() => {
    // Backup original require
    originalRequire = module.constructor.prototype.require;
  });

  afterEach(() => {
    // Clean up require hooks, if any
    module.constructor.prototype.require = originalRequire;
    clearModule(LIB_PATH);
    try { clearModule('passport-google-oauth1'); } catch (e) {}
    try { clearModule('passport-google-oauth20'); } catch (e) {}
  });

  it('should export Strategy, OAuthStrategy, and OAuth2Strategy when both peer deps are present', function () {
    // Mock both modules
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') return 'mock-oauth1';
      if (id === 'passport-google-oauth20') return 'mock-oauth2';
      return originalRequire.call(this, id);
    };
    const entry = require(LIB_PATH);
    expect(entry.Strategy).to.equal('mock-oauth1');
    expect(entry.OAuthStrategy).to.equal('mock-oauth1');
    expect(entry.OAuth2Strategy).to.equal('mock-oauth2');
  });

  it('should throw if passport-google-oauth1 is missing', function () {
    // Mock only the 20 module
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth20') return 'mock-oauth2';
      if (id === 'passport-google-oauth1') {
        let e = new Error('Cannot find module "passport-google-oauth1"');
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      }
      return originalRequire.call(this, id);
    };
    expect(() => require(LIB_PATH)).to.throw(/passport-google-oauth1/);
  });

  it('should throw if passport-google-oauth20 is missing', function () {
    // Mock only the 1 module
    module.constructor.prototype.require = function (id) {
      if (id === 'passport-google-oauth1') return 'mock-oauth1';
      if (id === 'passport-google-oauth20') {
        let e = new Error('Cannot find module "passport-google-oauth20"');
        e.code = 'MODULE_NOT_FOUND';
        throw e;
      }
      return originalRequire.call(this, id);
    };
    expect(() => require(LIB_PATH)).to.throw(/passport-google-oauth20/);
  });
});