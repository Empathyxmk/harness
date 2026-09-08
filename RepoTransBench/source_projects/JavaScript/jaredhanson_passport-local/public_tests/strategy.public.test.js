/* global describe, it, expect */

var Strategy = require('../lib/strategy');

describe('Strategy - Public Cases', function() {
    
  var strategy = new Strategy(function(){});
    
  it('should be named local', function() {
    expect(strategy.name).to.equal('local');
  });

  it('should throw if constructed without a verify callback (public test)', function() {
    expect(function() {
      var s = new Strategy();
    }).to.throw(TypeError, 'LocalStrategy requires a verify callback');
  });
});