const { expect } = require('chai');
const local = require('../lib/index');

describe('lib/index', function() {
  it('exports Strategy as module.exports', function() {
    expect(local).to.be.a('function');
    expect(local.name).to.equal('Strategy');
  });

  it('exports .Strategy property', function() {
    expect(local.Strategy).to.be.a('function');
  });

  it('Strategy instanceof Function', function() {
    expect(new local(function test(){})).to.be.an.instanceof(local.Strategy);
  });
});