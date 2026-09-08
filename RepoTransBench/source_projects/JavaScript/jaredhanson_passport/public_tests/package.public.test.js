/* global describe, it, expect */

var passport = require('..');

describe('passport (public)', function() {
  
  it('should expose singleton authenticator with different checks', function() {
    expect(passport).to.be.an('object');
    // Confirm it's not null and not undefined for variety
    expect(passport).to.not.equal(null);
    expect(passport).to.not.equal(undefined);
    expect(passport).to.be.an.instanceOf(passport.Authenticator);
  });
  
  it('should export constructors (public logic)', function() {
    // Test .Passport separately too
    expect(passport.Authenticator).to.be.a('function');
    expect(passport.Strategy).to.be.a('function');
    expect(passport.Passport).to.be.a('function');
  });
  
  it('should export strategies (public variation)', function() {
    expect(passport.strategies).to.be.an('object');
    expect(passport.strategies.SessionStrategy).to.be.a('function');
  });
  
});