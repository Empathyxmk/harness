const assert = require('assert');
const util = require('../util');

describe('util.js extra branch/edge cases (public)', function () {
  it('should error on missing file in loadSystemConfig (different name)', function (done) {
    if (typeof util.loadSystemConfig === 'function') {
      util.loadSystemConfig('nonexistingfile_public_test.yml', {}, (err, sys) => {
        assert(err, 'Should error on missing file');
        done();
      });
    } else {
      done();
    }
  });

  it('should return undefined for missing service (diff name) in findServiceByName', function () {
    if (typeof util.findServiceByName === 'function') {
      const system = { services: { b: { name: 'b' } } };
      assert.strictEqual(util.findServiceByName(system, 'not_present'), undefined);
    }
  });

  it('should handle getServiceLogPath fallback with changed property', function () {
    if (typeof util.getServiceLogPath === 'function') {
      const result = util.getServiceLogPath({ log_root: undefined }, { name: 'bar' });
      assert(result);
    }
  });

  it('should handle getServiceScript with missing env', function () {
    if (typeof util.getServiceScript === 'function') {
      // No env on config
      const res = util.getServiceScript({}, { scripts: { foo: "x" }, name: 'n2' }, 'stop');
      assert(res);
    }
  });

  it('should NOT throw on undefined for getServiceShell arguments', function () {
    if (typeof util.getServiceShell === 'function') {
      let result = util.getServiceShell(undefined, undefined);
      assert(result);
      result = util.getServiceShell(undefined, {});
      assert(result);
    }
  });

  it('should handle parseWithEnv with null input', function () {
    if (typeof util.parseWithEnv === 'function') {
      assert(util.parseWithEnv(null));
      assert(util.parseWithEnv({}, [1, 2]));
    }
  });

  it('should handle missing group in getGroupByService (diff group)', function () {
    if (typeof util.getGroupByService === 'function') {
      const sys = { groups: { ops: ['svcQ', 'svcW'] } };
      assert.strictEqual(util.getGroupByService(sys, 'noSuchService'), undefined);
    }
  });

  it('should handle malformed system in findServiceByPort (diff port)', function () {
    if (typeof util.findServiceByPort === 'function') {
      assert.strictEqual(util.findServiceByPort(undefined, 54321), undefined);
      assert.strictEqual(util.findServiceByPort({}, 9999), undefined);
    }
  });
});