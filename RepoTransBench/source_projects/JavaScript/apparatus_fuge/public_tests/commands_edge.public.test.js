const commands = require('../commands');
const assert = require('assert');

describe('commands.js edge/error (public)', () => {
  it('should handle truly null runner arguments gracefully', () => {
    const cmds = commands(null, null);
    assert(typeof cmds === 'object');
    assert(typeof cmds.init === 'function');
    assert(typeof cmds.shell === 'function');
  });

  it('should exercise branch in isGroup for group not in groups', function () {
    const cmds = commands({}, {});
    if (typeof cmds.isGroup === 'function') {
      const sys = { groups: { prod: ['svcZ'] } };
      assert.strictEqual(cmds.isGroup('qa', sys), undefined);
    }
  });

  it('should handle showInfo with null as arguments', function (done) {
    const cmds = commands({}, {
      preview: function (group, full, cb) {
        cb(null, { out: 'z' });
      }
    });
    if (typeof cmds.showInfo === 'function') {
      cmds.showInfo(null, {}, function(err, result) {
        assert(result);
        done();
      });
    } else {
      done();
    }
  });
});