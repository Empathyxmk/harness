var chai = require('chai')
  , TwitterStrategy = require('../lib/strategy');

describe('Strategy (public)', function() {
  describe('constructed (public)', function() {
    var strategy = new TwitterStrategy({
        consumerKey: 'XYZ789',
        consumerSecret: 'newsecret'
      }, function(){});
    
    it('should be named twitter', function() {
      expect(strategy.name).to.equal('twitter');
    });
  });

  describe('constructed with undefined options (public)', function() {
    it('should throw', function() {
      expect(function() {
        var strategy = new TwitterStrategy(undefined, function(){});
      }).to.throw(Error);
    });
  });

  describe('authorization request (public)', function() {
    var strategy = new TwitterStrategy({
        consumerKey: 'XYZ789',
        consumerSecret: 'newsecret'
      }, function(){});

    strategy._oauth.getOAuthRequestToken = function(extraParams, callback) {
      callback(null, 'tokennew123', 'secretnew123', {});
    };

    var url;

    before(function(done) {
      chai.passport.use(strategy)
        .redirect(function(u) {
          url = u;
          done();
        })
        .req(function(req) {
          req.session = {};
        })
        .authenticate();
    });

    it('should be redirected with different public token', function() {
      expect(url).to.equal('https://api.twitter.com/oauth/authenticate?oauth_token=tokennew123');
    });
  });

  describe('authorization request with parameters (public)', function() {
    var strategy = new TwitterStrategy({
        consumerKey: 'XYZ789',
        consumerSecret: 'newsecret'
      }, function(){});

    strategy._oauth.getOAuthRequestToken = function(extraParams, callback) {
      callback(null, 'tokenxyz321', 'secretxyz321', {});
    };

    var url;

    before(function(done) {
      chai.passport.use(strategy)
        .redirect(function(u) {
          url = u;
          done();
        })
        .req(function(req) {
          req.session = {};
        })
        .authenticate({ screenName: 'alice', forceLogin: false });
    });

    it('should be redirected with different parameters (public)', function() {
      expect(url).to.equal('https://api.twitter.com/oauth/authenticate?oauth_token=tokenxyz321&force_login=false&screen_name=alice');
    });
  });

  describe('failure caused by user denying request (public)', function() {
    var strategy = new TwitterStrategy({
        consumerKey: 'XYZ789',
        consumerSecret: 'newsecret'
      }, function(){});

    var info;

    before(function(done) {
      chai.passport.use(strategy)
        .fail(function(i) {
          info = i;
          done();
        })
        .req(function(req) {
          req.query = {};
          req.query.denied = 'Z9W8X7Y6';
        })
        .authenticate();
    });

    it('should fail (public)', function() {
      expect(info).to.be.undefined;
    });
  });

  describe('error caused by invalid consumer secret sent to request token URL (public)', function() {
    var strategy = new TwitterStrategy({
      consumerKey: 'XYZ789',
      consumerSecret: 'invalid-public-secret',
      callbackURL: 'http://localhost/callback2'
    }, function verify(){});

    strategy._oauth.getOAuthRequestToken = function(params, callback) {
      callback({ statusCode: 401, data: '{"errors":[{"code":77,"message":"Authentication failed."}]}' });
    };

    var err;

    before(function(done) {
      chai.passport.use(strategy)
        .error(function(e) {
          err = e;
          done();
        })
        .req(function(req) {
          req.session = {};
        })
        .authenticate();
    });

    it('should error (public)', function() {
      expect(err).to.be.an.instanceOf(Error);
      expect(err.message).to.equal("Authentication failed.");
    });
  });

  describe('error caused by invalid consumer secret sent to request token URL, formatted as unexpected JSON (public)', function() {
    var strategy = new TwitterStrategy({
      consumerKey: 'XYZ789',
      consumerSecret: 'invalid-public-secret',
      callbackURL: 'http://localhost/callback2'
    }, function verify(){});

    strategy._oauth.getOAuthRequestToken = function(params, callback) {
      callback({ statusCode: 401, data: '{"unexpected":"format"}' });
    };

    var err;

    before(function(done) {
      chai.passport.use(strategy)
        .error(function(e) {
          err = e;
          done();
        })
        .req(function(req) {
          req.session = {};
        })
        .authenticate();
    });

    it('should error (public) with fallback message', function() {
      expect(err).to.be.an.instanceOf(Error);
      expect(err.constructor.name).to.equal('InternalOAuthError');
      expect(err.message).to.equal('Failed to obtain request token');
    });
  });

  describe("error caused by invalid callback sent to request token URL (public)", function() {
    var strategy = new TwitterStrategy({
      consumerKey: 'XYZ789',
      consumerSecret: 'newsecret',
      callbackURL: 'http://localhost/invalid-callback2'
    }, function verify(){});

    strategy._oauth.getOAuthRequestToken = function(params, callback) {
      callback({ statusCode: 401, data: '<?xml version="1.0"?><hash><error>The callback url is not allowed</error><request>/oauth/request_token</request></hash>' });
    };

    var err;

    before(function(done) {
      chai.passport.use(strategy)
        .error(function(e) {
          err = e;
          done();
        })
        .req(function(req) {
          req.session = {};
        })
        .authenticate();
    });

    it('should error (public) on callback restriction', function() {
      expect(err).to.be.an.instanceOf(Error);
      expect(err.message).to.equal("The callback url is not allowed");
    });
  });

  describe('error caused by invalid request token sent to access token URL (public)', function() {
    var strategy = new TwitterStrategy({
      consumerKey: 'XYZ789',
      consumerSecret: 'newsecret',
      callbackURL: 'http://localhost/callback2'
    }, function verify(){});

    strategy._oauth.getOAuthAccessToken = function(token, tokenSecret, verifier, callback) {
      callback({ statusCode: 401, data: 'Request token not accepted.' });
    };

    var err;

    before(function(done) {
      chai.passport.use(strategy)
        .error(function(e) {
          err = e;
          done();
        })
        .req(function(req) {
          req.query = {};
          req.query['oauth_token'] = 'y-tokennew123';
          req.query['oauth_verifier'] = 'vxyz321abc';
          req.session = {};
          req.session['oauth:twitter'] = {};
          req.session['oauth:twitter']['oauth_token'] = 'y-tokennew123';
          req.session['oauth:twitter']['oauth_token_secret'] = 'secretnew123';
        })
        .authenticate();
    });

    it('should error (public) on invalid request token', function() {
      expect(err).to.be.an.instanceOf(Error);
      expect(err.message).to.equal("Request token not accepted.");
    });
  });

  describe('error caused by invalid verifier sent to access token URL (public)', function() {
    var strategy = new TwitterStrategy({
      consumerKey: 'XYZ789',
      consumerSecret: 'newsecret',
      callbackURL: 'http://localhost/callback2'
    }, function verify(){});

    strategy._oauth.getOAuthAccessToken = function(token, tokenSecret, verifier, callback) {
      callback({ statusCode: 401, data: 'OAuth error: verifier invalid' });
    };

    var err;

    before(function(done) {
      chai.passport.use(strategy)
        .error(function(e) {
          err = e;
          done();
        })
        .req(function(req) {
          req.query = {};
          req.query['oauth_token'] = 'y-tokennew123';
          req.query['oauth_verifier'] = 'badpublicverifier';
          req.session = {};
          req.session['oauth:twitter'] = {};
          req.session['oauth:twitter']['oauth_token'] = 'y-tokennew123';
          req.session['oauth:twitter']['oauth_token_secret'] = 'secretnew123';
        })
        .authenticate();
    });

    it('should error (public) on invalid verifier', function() {
      expect(err).to.be.an.instanceOf(Error);
      expect(err.message).to.equal("OAuth error: verifier invalid");
    });
  });
});