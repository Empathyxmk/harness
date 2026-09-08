/* global describe, it, expect, before */
/* jshint expr: true */

var chai = require('chai')
  , Authenticator = require('../lib/authenticator');


describe('Authenticator (public)', function() {
  
  describe('#initialize', function() {
    
    it('should have correct arity (public)', function() {
      var passport = new Authenticator();
      expect(passport.initialize).to.have.length(1);
    });
    
    describe('handling a request with a different custom user property', function() {
      var passport = new Authenticator();
      var request, error;

      before(function(done) {
        chai.connect.use(passport.initialize({ userProperty: 'loggedInUser' }))
          .req(function(req) {
            request = req;
            req.session = {};
          })
          .next(function(err) {
            error = err;
            done();
          })
          .dispatch();
      });
    
      it('should not error (public)', function() {
        expect(error).to.be.undefined;
      });
      
      it('should set user property on request (public)', function() {
        expect(request._userProperty).to.equal('loggedInUser');
      });
    
      it('should not initialize namespace within session (public)', function() {
        expect(request.session.passport).to.be.undefined;
      });
      
      it('should expose authenticator on internal request property (public)', function() {
        expect(request._passport).to.be.an('object');
        expect(request._passport.instance).to.be.an.instanceOf(Authenticator);
        expect(request._passport.instance).to.equal(passport);
        expect(request._passport.instance._sm).to.be.an('object');
        expect(request._passport.instance._userProperty).to.equal('loggedInUser');
      });
    });
  });
  
  
  describe('#authenticate', function() {
    it('should have correct arity (public)', function() {
      var passport = new Authenticator();
      expect(passport.authenticate).to.have.length(3);
    });

    describe('handling a request (public, with different user data)', function() {
      function Strategy() {}
      Strategy.prototype.authenticate = function(req) {
        var user = { id: '42', username: 'differentuser' };
        this.success(user);
      };

      var passport = new Authenticator();
      passport.use('success', new Strategy());

      var request, error;

      before(function(done) {
        chai.connect.use(passport.authenticate('success'))
          .req(function(req) {
            request = req;
            req.logIn = function(user, options, done) {
              this.user = user;
              done();
            };
          })
          .next(function(err) {
            error = err;
            done();
          })
          .dispatch();
      });

      it('should not error (public)', function() {
        expect(error).to.be.undefined;
      });

      it('should set user (public)', function() {
        expect(request.user).to.be.an('object');
        expect(request.user.id).to.equal('42');
        expect(request.user.username).to.equal('differentuser');
      });

      it('should set authInfo (public)', function() {
        expect(request.authInfo).to.be.an('object');
        expect(Object.keys(request.authInfo)).to.have.length(0);
      });
    });

    describe('handling a request with instantiated strategy (public, variant)', function() {
      function Strategy() {}
      Strategy.prototype.authenticate = function(req) {
        var user = { id: '99', username: 'publictestuser' };
        this.success(user);
      };

      var passport = new Authenticator();

      var request, error;

      before(function(done) {
        chai.connect.use(passport.authenticate(new Strategy()))
          .req(function(req) {
            request = req;
            req.logIn = function(user, options, done) {
              this.user = user;
              done();
            };
          })
          .next(function(err) {
            error = err;
            done();
          })
          .dispatch();
      });

      it('should not error (public)', function() {
        expect(error).to.be.undefined;
      });

      it('should set user (public)', function() {
        expect(request.user).to.be.an('object');
        expect(request.user.id).to.equal('99');
        expect(request.user.username).to.equal('publictestuser');
      });

      it('should set authInfo (public)', function() {
        expect(request.authInfo).to.be.an('object');
        expect(Object.keys(request.authInfo)).to.have.length(0);
      });
    });
  });

  describe('#authorize', function() {
    it('should have correct arity (public)', function() {
      var passport = new Authenticator();
      expect(passport.authorize).to.have.length(3);
    });

    describe('handling a request (public)', function() {
      function Strategy() {}
      Strategy.prototype.authenticate = function(req) {
        var user = { id: '55', username: 'authorizeUser' };
        this.success(user);
      };

      var passport = new Authenticator();
      passport.use('success', new Strategy());

      var request, error;

      before(function(done) {
        chai.connect.use(passport.authorize('success'))
          .req(function(req) {
            request = req;
            req.logIn = function(user, options, done) {
              this.user = user;
              done();
            };
          })
          .next(function(err) {
            error = err;
            done();
          })
          .dispatch();
      });

      it('should not error (public)', function() {
        expect(error).to.be.undefined;
      });

      it('should not set user (public)', function() {
        expect(request.user).to.be.undefined;
      });

      it('should set account (public)', function() {
        expect(request.account).to.be.an('object');
        expect(request.account.id).to.equal('55');
        expect(request.account.username).to.equal('authorizeUser');
      });

      it('should set authInfo to empty object (public)', function() {
        expect(request.authInfo).to.deep.equal({});
      });
    });
  });
});