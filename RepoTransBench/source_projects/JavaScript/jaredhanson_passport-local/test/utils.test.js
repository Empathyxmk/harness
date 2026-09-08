const { expect } = require('chai');
const { lookup } = require('../lib/utils');

describe('utils.lookup', function() {
  it('returns found field at root', function() {
    expect(lookup({foo: 'bar'}, 'foo')).to.equal('bar');
  });

  it('returns found nested field with brackets', function() {
    expect(lookup({foo: { bar: 'baz' }}, 'foo[bar]')).to.equal('baz');
  });

  it('returns null if not found', function() {
    expect(lookup({foo: { }}, 'foo[bar]')).to.equal(null);
    expect(lookup({foo: 'bar'}, 'doesnotexist')).to.equal(null);
    expect(lookup(null, 'foo')).to.equal(null);
  });

  it('returns non-object field in deep nesting', function() {
    expect(lookup({foo: { bar: { baz: 7 }}}, 'foo[bar][baz]')).to.equal(7);
  });

  it('returns null for undefined along the chain', function() {
    expect(lookup({foo: undefined}, 'foo[bar]')).to.equal(null);
  });

  it('returns null for empty string field on chain', function() {
    expect(lookup({foo: {"": 1}}, 'foo[]')).to.equal(1);
  });
});