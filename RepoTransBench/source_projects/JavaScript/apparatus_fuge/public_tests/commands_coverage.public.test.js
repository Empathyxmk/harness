const assert = require('assert');
const commands = require('../commands');

describe('commands.js coverage (public)', function () {
  it('should properly call showInfo with 1 argument (string)', function (done) {
    let called = false;
    const cmds = commands({}, {
      preview: function(group, full, cb) {
        called = true;
        cb(null, { ok: 1 });
      }
    });
    if (typeof cmds.showInfo === 'function') {
      cmds.showInfo(['testgroup'], {}, function(err, result) {
        assert(called);
        assert(result);
        done();
      });
    } else {
      done();
    }
  });

  it('should call preview with group and false', function (done) {
    let params = {};
    const cmds = commands({}, {
      preview: function(group, full, cb) {
        params = { group, full };
        cb(null, { out: 42 });
      }
    });
    if (typeof cmds.showInfo === 'function') {
      cmds.showInfo(['g'], {}, function(err, result) {
        assert(params.full === false);
        assert(result);
        done();
      });
    } else {
      done();
    }
  });
});