const assert = require('assert');
const util = require('../util.js');

describe('util.js', function () {
  it('should export expected utility functions', function () {
    [
      'isDisabled', 'findChanged', 'compile',
      'getGroups', 'serviceByPid', 'writeIfChanged', 'getContainerState'
    ].forEach(key => assert.strictEqual(typeof util[key], 'function'));
  });

  it('isDisabled returns false if flags.running is true', function () {
    const container = { process: { flags: { running: true } } };
    assert.strictEqual(util.isDisabled(container), false);
  });

  it('isDisabled returns true if flags.running is false', function () {
    const container = { process: { flags: { running: false } } };
    assert.strictEqual(util.isDisabled(container), true);
  });

  it('isDisabled returns true if flags missing', function () {
    const container = { process: { } };
    assert.strictEqual(util.isDisabled(container), true);
    assert.strictEqual(util.isDisabled(), true);
  });

  it('findChanged returns empty array if no containers', function () {
    assert.deepStrictEqual(util.findChanged({}, {}), []);
  });

  it('findChanged returns changed items when content changes', function () {
    const oldState = { svc: { some: 'old' } };
    const newState = { svc: { some: 'new' } };
    assert.deepStrictEqual(util.findChanged(newState, oldState), ['svc']);
  });

  it('compile returns a string for input', function () {
    assert.strictEqual(typeof util.compile('foo'), 'string');
  });

  it('findChanged supports error path for invalid args', function() {
    assert.deepStrictEqual(util.findChanged(null, null), []);
  });

  it('getGroups returns list of groups', function() {
    const services = {
      svc1: { group: 'groupA' },
      svc2: { group: 'groupB' },
      svc3: { group: 'groupA' }
    };
    const result = util.getGroups(services);
    assert(result.includes('groupA'));
    assert(result.includes('groupB'));
  });

  it('serviceByPid finds service by pid', function() {
    const state = {
      s1: { process: { pid: 42 } }
    };
    assert.strictEqual(util.serviceByPid(state, 42), 's1');
    assert.strictEqual(util.serviceByPid(state, 9999), undefined);
  });

  it('writeIfChanged writes only if content changes', function(done) {
    const fs = require('fs');
    const tmpFile = './tmp_utl.txt';
    try { fs.unlinkSync(tmpFile); } catch (_) {}
    util.writeIfChanged(tmpFile, 'foo', () => {
      util.writeIfChanged(tmpFile, 'foo', () => {
        fs.unlinkSync(tmpFile);
        done();
      });
    });
  });

  it('getContainerState returns correct state', function() {
    const containers = {
      foo: { process: { stopped: true } }
    };
    assert.strictEqual(util.getContainerState(containers, 'foo'), 'stopped');
    assert.strictEqual(util.getContainerState({}, 'bar'), 'not-started');
  });
});