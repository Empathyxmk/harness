const SessionManager = require('../lib/sessionmanager');
const assert = require('assert');

describe('SessionManager', function() {
  describe('constructor', function() {
    it('should set key and serializeUser', function() {
      function ser() {}
      const sm = new SessionManager({ key: 'foo' }, ser);
      assert.strictEqual(sm._key, 'foo');
      assert.strictEqual(sm._serializeUser, ser);
    });
    it('should work if first arg is a function', function() {
      function ser() {}
      const sm = new SessionManager(ser);
      assert.strictEqual(sm._key, 'passport');
      assert.strictEqual(sm._serializeUser, ser);
    });
    it('should default options to {}', function() {
      function ser() {}
      const sm = new SessionManager(undefined, ser);
      assert.strictEqual(sm._key, 'passport');
    });
  });

  describe('logIn', function() {
    it('should error if no session', function(done) {
      const sm = new SessionManager(() => {});
      const req = {};
      sm.logIn(req, {id:1}, {}, function(err) {
        assert.ok(err);
        assert.strictEqual(err.message.match(/session support/i) !== null, true);
        done();
      });
    });

    it('should proceed if regenerate and save succeed', function(done) {
      let serializedCalled = false;
      function ser(user, req, cb) {
        serializedCalled = true;
        cb(null, {id: user.id});
      }
      const sm = new SessionManager(ser);

      let saved = false;
      const req = {
        session: {
          data: "test",
          regenerate(cb) { req.session = this; cb(); },
          save(cb) { saved = true; cb(); }
        }
      };
      sm.logIn(req, {id: 42}, function(err) {
        assert.ifError(err);
        assert.ok(serializedCalled);
        assert.ok(saved);
        assert.deepStrictEqual(req.session['passport'].user, {id: 42});
        done();
      });
    });

    it('should pass error if regenerate fails', function(done) {
      const sm = new SessionManager(() => {});
      const req = {
        session: {
          regenerate(cb) { cb(new Error('regenfail')); }
        }
      };
      sm.logIn(req, {id: 55}, function(err) {
        assert.ok(err);
        assert.strictEqual(err.message, 'regenfail');
        done();
      });
    });

    it('should pass error if serializeUser fails', function(done) {
      function ser(user, req, cb) { cb(new Error('serialfail')); }
      const sm = new SessionManager(ser);
      const req = {
        session: {
          regenerate(cb) { cb(); }
        }
      };
      sm.logIn(req, {}, function(err) {
        assert.ok(err);
        assert.strictEqual(err.message, 'serialfail');
        done();
      });
    });

    it('should keep session info if keepSessionInfo is true', function(done) {
      function ser(user, req, cb) { cb(null, 123); }
      const sm = new SessionManager(ser);
      let req = {
        session: {
          foo: 1,
          regenerate(cb) { req.session = this; cb(); },
          save(cb) { cb(); }
        }
      };
      req.session.__proto__.regenerate = function(cb) { req.session = this; cb(); }; // safeguard

      sm.logIn(req, {}, { keepSessionInfo: true }, function(err) {
        assert.ifError(err);
        assert.strictEqual(req.session.foo, 1);
        assert.strictEqual(req.session['passport'].user, 123);
        done();
      });
    });

    it('should error if session.save fails', function(done) {
      function ser(user, req, cb) { cb(null, 1); }
      const sm = new SessionManager(ser);
      const req = {
        session: {
          regenerate(cb) { cb(); },
          save(cb) { cb(new Error('savefail')); }
        }
      };
      sm.logIn(req, {}, function(err) {
        assert.ok(err);
        assert.strictEqual(err.message, 'savefail');
        done();
      });
    });
  });

  describe('logOut', function() {
    it('should error if no session', function(done) {
      const sm = new SessionManager(() => {});
      const req = {};
      sm.logOut(req, {}, function(err) {
        assert.ok(err);
        done();
      });
    });

    it('should clear user and call save and regenerate', function(done) {
      const sm = new SessionManager(() => {});
      let sessionObj = {
        passport: { user: 'foo' },
        save(cb) { this.saved = true; cb(); },
        regenerate(cb) { this.regenerated = true; cb(); }
      };
      const req = { session: sessionObj };
      sm.logOut(req, function(err) {
        assert.ifError(err);
        assert.strictEqual(sessionObj.passport.user, undefined);
        assert.ok(sessionObj.saved);
        assert.ok(sessionObj.regenerated);
        done();
      });
    });

    it('should merge session info if keepSessionInfo is true', function(done) {
      const sm = new SessionManager(() => {});
      let sessionObj = {
        a: 123,
        passport: { user: 'foo' },
        save(cb) { this.saved = true; cb(); },
        regenerate(cb) { this.regenerated = true; cb(); }
      };
      const req = { session: sessionObj };
      sm.logOut(req, { keepSessionInfo: true }, function(err) {
        assert.ifError(err);
        assert.strictEqual(req.session.a, 123);
        done();
      });
    });

    it('should pass error if save fails', function(done) {
      const sm = new SessionManager(() => {});
      let sessionObj = {
        passport: { user: 'foo' },
        save(cb) { cb(new Error('savefail')); },
        regenerate(cb) {}
      };
      const req = { session: sessionObj };
      sm.logOut(req, {}, function(err) {
        assert.ok(err);
        assert.strictEqual(err.message, 'savefail');
        done();
      });
    });

    it('should pass error if regenerate fails', function(done) {
      const sm = new SessionManager(() => {});
      let sessionObj = {
        passport: { user: 'foo' },
        save(cb) { cb(); },
        regenerate(cb) { cb(new Error('regenfail')); }
      };
      const req = { session: sessionObj };
      sm.logOut(req, {}, function(err) {
        assert.ok(err);
        assert.strictEqual(err.message, 'regenfail');
        done();
      });
    });
  });
});