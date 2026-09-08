// Public test suite for Polyglot main API -- uses public/different test data

const { expect } = require('chai');
const Polyglot = require('../index');

describe('Polyglot main API (public)', function () {
  it('deals with falsy values as phrase (different keys)', function () {
    const polyglot = new Polyglot({ phrases: { nullValue: null, blank: '' } });
    // Null becomes key string, empty remains empty
    expect(polyglot.t('nullValue')).to.equal('nullValue');
    expect(polyglot.t('blank')).to.equal('');
  });

  it('does not throw for interpolation delimiters with different delimiters', function () {
    const polyglot = new Polyglot();
    expect(() =>
      polyglot.extend({ bye: 'bye %{username}' }, { interpolation: { prefix: '#{', suffix: '}' } }),
    ).to.not.throw();
  });

  // Add an additional check publicly (unique phrase interpolation)
  it('interpolates values with different phrasing', function () {
    const polyglot = new Polyglot({ phrases: { greet: 'Hey, %{person}!' } });
    expect(polyglot.t('greet', { person: 'Sam' })).to.equal('Hey, Sam!');
  });
});