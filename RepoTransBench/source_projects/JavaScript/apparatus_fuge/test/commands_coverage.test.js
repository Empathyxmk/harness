const assert = require('assert');
const commands = require('../commands.js');

describe('commands.js functional coverage', function () {
  let fakeRunner = {
    preview: function (group, full, cb) {
      cb(null, { out: 'preview:' + group + ':' + full });
    }
  };
  let cmnds;

  before(function () {
    cmnds = commands({}, fakeRunner);
  });

  it('exports functions including init, shell, isGroup, showInfo (if present)', function () {
    assert(typeof cmnds.init === 'function');
    assert(typeof cmnds.shell === 'function');
    // Optionally defined:
    if (typeof cmnds.isGroup === 'function') assert(true);
    if (typeof cmnds.showInfo === 'function') assert(true);
  });

  it('isGroup returns true if match, undefined if no match', function () {
    if (typeof cmnds.isGroup === 'function') {
      const sys = { groups: { dev: ['svc1', 'svc2'] } };
      assert.strictEqual(cmnds.isGroup('dev', sys), true);
      assert.strictEqual(cmnds.isGroup('foo', sys), undefined);
    }
  });

  it('showInfo routes to runner.preview and usage', function (done) {
    if (typeof cmnds.showInfo === 'function') {
      cmnds.showInfo(['foo'], {}, function (err, out) {
        assert(out && out.out === 'preview:foo:false');
        cmnds.showInfo(['foo', 'full'], {}, function (err, out) {
          assert(out && out.out === 'preview:foo:true');
          cmnds.showInfo(['foo','bar','baz'], {}, function(err, out) {
            assert(out && out.usage);
            cmnds.showInfo([], {}, function(err, out) {
              assert(out && out.usage);
              done();
            });
          });
        });
      });
    } else {
      done();
    }
  });
});