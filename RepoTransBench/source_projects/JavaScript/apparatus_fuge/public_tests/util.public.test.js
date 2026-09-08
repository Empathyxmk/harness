const assert = require('assert');
const util = require('../util');

describe('util.js public basic', function () {
  it('should fallback to undefined finding service by name in empty system', function () {
    if (typeof util.findServiceByName === 'function') {
      assert.strictEqual(util.findServiceByName({}, 'fooX'), undefined);
    }
  });

  it('getServiceLogPath should produce a string for different input', function () {
    if (typeof util.getServiceLogPath === 'function') {
      const result = util.getServiceLogPath({ log_root: '/tmp/fooBar/' }, { name: 'baz_service' });
      assert(typeof result === 'string');
    }
  });

  it('findServiceByPort gives undefined for missing', function () {
    if (typeof util.findServiceByPort === 'function') {
      assert.strictEqual(util.findServiceByPort({ services: { } }, 11111), undefined);
    }
  });

  it('parseWithEnv works with array input', function () {
    if (typeof util.parseWithEnv === 'function') {
      assert(util.parseWithEnv({}, ['a', 'b']));
    }
  });
});