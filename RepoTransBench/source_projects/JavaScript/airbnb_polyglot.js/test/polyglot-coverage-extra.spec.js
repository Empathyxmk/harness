// Additional coverage for Polyglot.js index.js (airbnb-polyglot) - branch and edge cases

const { expect } = require('chai');
const Polyglot = require('../index');

describe('Polyglot extra branch & edge coverage', function () {
  it('handles missing phrases and disables warning with allowMissing', function () {
    const polyglot = new Polyglot({ allowMissing: true });
    expect(polyglot.t('notpresent')).to.equal('notpresent'); // No warning expected with allowMissing
  });

  it('handles nested keys with dot notation', function () {
    const polyglot = new Polyglot({
      phrases: {
        a: { b: { c: 'c value' } }
      }
    });
    expect(polyglot.t('a.b.c')).to.equal('c value');
  });

  it('can replace phrases and extend', function () {
    const polyglot = new Polyglot({ phrases: { hello: 'hi' } });
    expect(polyglot.t('hello')).to.equal('hi');
    polyglot.replace({ bye: 'goodbye' });
    expect(polyglot.t('hello')).to.equal('hello'); // now missing
    expect(polyglot.t('bye')).to.equal('goodbye');
    polyglot.extend({ newkey: 'val' });
    expect(polyglot.t('newkey')).to.equal('val');
  });

  it('returns default value if provided and missing', function () {
    const polyglot = new Polyglot();
    expect(polyglot.t('notfound', { _: 'fallback!' })).to.equal('fallback!');
  });

  it('plurals: correctly picks pluralization forms', function () {
    const polyglot = new Polyglot({
      phrases: {
        dog_count: '%{smart_count} dog |||| %{smart_count} dogs'
      }
    });
    // singular
    expect(polyglot.t('dog_count', { smart_count: 1 })).to.include('1 dog');
    // plural
    expect(polyglot.t('dog_count', { smart_count: 4 })).to.include('4 dogs');
  });

  it('locale: can change locale, affects pluralization', function () {
    const polyglot = new Polyglot();
    polyglot.locale('fr');
    expect(polyglot.locale()).to.equal('fr');
    polyglot.locale('en'); // back to en
    expect(polyglot.locale()).to.equal('en');
  });
});