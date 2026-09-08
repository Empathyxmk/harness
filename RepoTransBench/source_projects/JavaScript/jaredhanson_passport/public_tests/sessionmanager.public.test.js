// Public tests for lib/sessionmanager.js using different test data than the originals

const SessionManager = require('../lib/sessionmanager');
const assert = require('assert');

describe('SessionManager (public)', function () {
  it('should initialize SessionManager with an alternate string', function () {
    const sm = new SessionManager({ key: 'passport-alt' });
    assert.strictEqual(sm._key, 'passport-alt');
  });

  it('should serialize and deserialize a user object with unique values', function (done) {
    const sm = new SessionManager({ key: 'unique-session' });
    const user = { id: 42, name: 'Zephyr' };

    sm.serializeUser(function(u, cb) { cb(null, u.id); });

    sm.deserializeUser(function(id, cb) {
      if (id === 42) return cb(null, user);
      cb(null, false);
    });

    sm.serializeUserFunction(user, function(err, id) {
      assert.ifError(err);
      assert.strictEqual(id, 42);

      sm.deserializeUserFunction(id, function(err, result) {
        assert.ifError(err);
        assert.deepStrictEqual(result, user);
        done();
      });
    });
  });
});