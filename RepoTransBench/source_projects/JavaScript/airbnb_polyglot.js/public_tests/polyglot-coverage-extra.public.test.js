// Public test cases for additional coverage for Polyglot.js index.js (edge and branch cases)
// Using different input/output data from the original private tests

const { expect } = require('chai');
const Polyglot = require('../index');

describe('Polyglot extra branch & edge coverage (public)', function () {
  it('handles missing phrases and disables warning with allowMissing (different key)', function () {
    const polyglot = new Polyglot({ allowMissing: true });
    expect(polyglot.t('anothermissing')).to.equal('anothermissing');
  });

  it('handles nested keys with dot notation (different depth)', function () {
    const polyglot = new Polyglot({
      phrases: {
        x: { y: { z: 'z value' } }
      }
    });
    expect(polyglot.t('x.y.z')).to.equal('z value');
  });

  it('can replace phrases and extend (different phrases)', function () {
    const polyglot = new Polyglot({ phrases: { greet: 'hello' } });
    expect(polyglot.t('greet')).to.equal('hello');
    polyglot.replace({ farewell: 'bye' });
    expect(polyglot.t('greet')).to.equal('greet'); // replaced, so missing now
    expect(polyglot.t('farewell')).to.equal('bye');
    polyglot.extend({ welcome: 'howdy' });
    expect(polyglot.t('welcome')).to.equal('howdy');
  });

  it('returns default value if provided and missing (different phrase/default)', function () {
    const polyglot = new Polyglot();
    expect(polyglot.t('absent_key', { _: 'use this default' })).to.equal('use this default');
  });

  it('plurals: correctly picks pluralization forms with different key', function () {
    const polyglot = new Polyglot({
      phrases: {
        cat_count: '%{smart_count} cat |||| %{smart_count} cats'
      }
    });
    expect(polyglot.t('cat_count', { smart_count: 1 })).to.include('1 cat');
    expect(polyglot.t('cat_count', { smart_count: 3 })).to.include('3 cats');
  });

  it('locale: can change locale, affects pluralization (different values)', function () {
    const polyglot = new Polyglot();
    polyglot.locale('es');
    expect(polyglot.locale()).to.equal('es');
    polyglot.locale('de');
    expect(polyglot.locale()).to.equal('de');
  });
});