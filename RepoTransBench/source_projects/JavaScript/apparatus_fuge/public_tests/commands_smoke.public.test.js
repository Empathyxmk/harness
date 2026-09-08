const assert = require('assert');
const commands = require('../commands');

describe('commands.js smoke public', function () {
  it('should create commands instance with non-empty object', function () {
    const cmds = commands({ a: 1 }, { b: 2 });
    assert(typeof cmds === 'object');
    assert('init' in cmds && typeof cmds.init === 'function');
    assert('shell' in cmds && typeof cmds.shell === 'function');
  });

  it('should return usage=true for showInfo with >2 arguments', function (done) {
    const cmds = commands({}, {
      preview: function(group, full, cb) {
        cb(null, { out: 'y' });
      }
    });
    if (typeof cmds.showInfo === 'function') {
      cmds.showInfo([1, 2, 3], {}, function(err, result) {
        assert(result && result.usage === true);
        done();
      });
    } else {
      done();
    }
  });

  it('should call preview for showInfo with full as argument', function (done) {
    let called = false;
    const cmds = commands({}, {
      preview: function(group, full, cb) {
        called = true;
        assert(full === true);
        cb(null, { ok: 'yes' });
      }
    });
    if (typeof cmds.showInfo === 'function') {
      cmds.showInfo(['groupA', 'full'], {}, function(err, result) {
        assert(called);
        assert(result);
        done();
      });
    } else {
      done();
    }
  });
});