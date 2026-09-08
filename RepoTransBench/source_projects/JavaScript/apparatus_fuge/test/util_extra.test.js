const assert = require('assert');
const util = require('../util');

describe('util.js extra branch/edge cases', function () {
  it('should handle missing and malformed system input in loadSystemConfig', function (done) {
    if (typeof util.loadSystemConfig === 'function') {
      // Test with bad file path
      util.loadSystemConfig('notarealfile.yml', {}, (err, sys) => {
        assert(err, 'Should error on missing file');
        done();
      });
    } else {
      done();
    }
  });

  it('should return undefined or similar for missing service in findServiceByName', function () {
    if (typeof util.findServiceByName === 'function') {
      const system = { services: { a: { name: 'a' } } };
      assert.strictEqual(util.findServiceByName(system, 'missing'), undefined);
    }
  });

  it('should handle getServiceLogPath fallback', function () {
    if (typeof util.getServiceLogPath === 'function') {
      const result = util.getServiceLogPath({ log_root: null }, { name: 'foo' });
      assert(result); // Just test fallback path - result exists
    }
  });

  it('should handle getServiceScript with unusual config', function () {
    if (typeof util.getServiceScript === 'function') {
      // No scripts on service
      const res = util.getServiceScript({ env: {} }, { scripts: {}, name: 'n' }, 'start');
      assert(res);
    }
  });

  it('should NOT throw on malformed values for getServiceShell', function () {
    if (typeof util.getServiceShell === 'function') {
      // No service object or no shell, expect fallback
      let result = util.getServiceShell({}, null);
      assert(result);
      result = util.getServiceShell(null, {});
      assert(result);
    }
  });

  it('should handle parseWithEnv on malformed input', function () {
    if (typeof util.parseWithEnv === 'function') {
      assert(util.parseWithEnv());
      assert(util.parseWithEnv({}, []));
    }
  });

  it('should handle missing name in getGroupByService', function () {
    if (typeof util.getGroupByService === 'function') {
      const sys = { groups: { dev: ['svc1', 'svc2'] } };
      assert.strictEqual(util.getGroupByService(sys, 'svcX'), undefined);
    }
  });

  it('should handle bad system in findServiceByPort', function () {
    if (typeof util.findServiceByPort === 'function') {
      assert.strictEqual(util.findServiceByPort(null, 1234), undefined);
      assert.strictEqual(util.findServiceByPort({}, 1234), undefined);
    }
  });
});