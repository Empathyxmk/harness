'use strict';

var Polyglot = require('../');
var expect = require('chai').expect;

describe('Polyglot utility & pluralization functions', function () {
  it('falls back to default locale when unknown', function () {
    var p = new Polyglot({ phrases: { dogs: '%{smart_count} dog |||| %{smart_count} dogs' } });
    // Igbo - should fallback to default 'en' pluralization
    expect(p.t('dogs', { smart_count: 1, locale: 'ig' })).to.equal('1 dog');
    expect(p.t('dogs', { smart_count: 2, locale: 'ig' })).to.equal('2 dogs');
  });

  it('handles russian plurals correctly', function () {
    var p = new Polyglot({
      phrases: {
        cats: '%{smart_count} кот||||%{smart_count} кота||||%{smart_count} котов'
      },
      locale: 'ru'
    });
    expect(p.t('cats', { smart_count: 1 })).to.equal('1 кот');
    expect(p.t('cats', { smart_count: 2 })).to.equal('2 кота');
    expect(p.t('cats', { smart_count: 5 })).to.equal('5 котов');
  });

  it('handles slovenian plurals correctly', function () {
    var p = new Polyglot({
      phrases: {
        items: '%{smart_count} stvar||||%{smart_count} stvari||||%{smart_count} stvari||||%{smart_count} stvari'
      },
      locale: 'sl'
    });
    expect(p.t('items', { smart_count: 1 })).to.equal('1 stvar');
    expect(p.t('items', { smart_count: 2 })).to.equal('2 stvari');
    expect(p.t('items', { smart_count: 3 })).to.equal('3 stvari');
    expect(p.t('items', { smart_count: 5 })).to.equal('5 stvari');
  });

  it('warns when phrase is missing, respects silent', function () {
    // This is a shallow test assuming that warn function does not throw, just logs
    var p = new Polyglot({ phrases: { apple: 'Apple' }, silent: false });
    expect(p.t('banana')).to.equal('banana');
    var p2 = new Polyglot({ phrases: { apple: 'Apple' }, silent: true });
    expect(p2.t('banana')).to.equal('banana');
  });

  it('throws error on invalid interpolation delimiters', function () {
    expect(function () {
      new Polyglot({ interpolation: { prefix: '||||', suffix: 'xx' } });
    }).to.throw(RangeError);
    expect(function () {
      new Polyglot({ interpolation: { prefix: '{{', suffix: '||||' } });
    }).to.throw(RangeError);
  });

  it('handles setting and replacing phrases at runtime', function () {
    var p = new Polyglot();
    p.extend({ key1: 'foo', key2: 'bar' });
    expect(p.t('key1')).to.equal('foo');
    p.replace({ newkey: 'baz' });
    expect(p.t('newkey')).to.equal('baz');
    expect(p.t('key1')).to.equal('key1'); // Replaced, not extended
  });

  it('supports unset()', function () {
    var p = new Polyglot({ phrases: { hi: 'Hello', bye: 'Goodbye' } });
    p.unset('hi');
    expect(p.t('hi')).to.equal('hi');
    p.extend({ hi: 'Hello again' });
    expect(p.t('hi')).to.equal('Hello again');
  });

  it('handles allowMissing correctly', function () {
    var p = new Polyglot({ allowMissing: true });
    expect(p.t('greeting %{name}', { name: 'Test' })).to.equal('greeting Test');
  });

  it('handles chinese pluralization', function () {
    var p = new Polyglot({
      phrases: {
        item: '%{smart_count} 项'
      },
      locale: 'zh'
    });
    expect(p.t('item', { smart_count: 1 })).to.equal('1 项');
    expect(p.t('item', { smart_count: 99 })).to.equal('99 项');
  });

  it('accepts empty options safely', function () {
    var p = new Polyglot();
    expect(p.t('some key', null)).to.equal('some key');
    expect(p.t('some key', undefined)).to.equal('some key');
  });
});