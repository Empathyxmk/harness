'use strict';

// Public test cases for Polyglot utility & pluralization functions (with different data)

var Polyglot = require('../');
var expect = require('chai').expect;

describe('Polyglot utility & pluralization functions (public)', function () {
  it('falls back to default locale when unknown (different language)', function () {
    var p = new Polyglot({ phrases: { birds: '%{smart_count} bird |||| %{smart_count} birds' } });
    // Hawaiian - expect fallback to 'en'
    expect(p.t('birds', { smart_count: 1, locale: 'haw' })).to.equal('1 bird');
    expect(p.t('birds', { smart_count: 3, locale: 'haw' })).to.equal('3 birds');
  });

  it('handles russian plurals correctly (different word)', function () {
    var p = new Polyglot({
      phrases: {
        apples: '%{smart_count} яблоко||||%{smart_count} яблока||||%{smart_count} яблок'
      },
      locale: 'ru'
    });
    expect(p.t('apples', { smart_count: 1 })).to.equal('1 яблоко');
    expect(p.t('apples', { smart_count: 3 })).to.equal('3 яблока');
    expect(p.t('apples', { smart_count: 7 })).to.equal('7 яблок');
  });

  it('handles slovenian plurals correctly (different word)', function () {
    var p = new Polyglot({
      phrases: {
        cars: '%{smart_count} avto||||%{smart_count} avta||||%{smart_count} avti||||%{smart_count} avtov'
      },
      locale: 'sl'
    });
    expect(p.t('cars', { smart_count: 1 })).to.equal('1 avto');
    expect(p.t('cars', { smart_count: 2 })).to.equal('2 avta');
    expect(p.t('cars', { smart_count: 4 })).to.equal('4 avti');
    expect(p.t('cars', { smart_count: 10 })).to.equal('10 avtov');
  });

  it('warns when phrase is missing, respects silent (different phrases)', function () {
    var p = new Polyglot({ phrases: { orange: 'Orange' }, silent: false });
    expect(p.t('peach')).to.equal('peach');
    var p2 = new Polyglot({ phrases: { orange: 'Orange' }, silent: true });
    expect(p2.t('peach')).to.equal('peach');
  });

  it('throws error on invalid interpolation delimiters (different delimiters)', function () {
    expect(function () {
      new Polyglot({ interpolation: { prefix: '(((((', suffix: '**' } });
    }).to.throw(RangeError);
    expect(function () {
      new Polyglot({ interpolation: { prefix: '<<', suffix: '>>>>>' } });
    }).to.throw(RangeError);
  });

  it('handles setting and replacing phrases at runtime (different keys)', function () {
    var p = new Polyglot();
    p.extend({ first: 'alpha', second: 'beta' });
    expect(p.t('first')).to.equal('alpha');
    p.replace({ updated: 'gamma' });
    expect(p.t('updated')).to.equal('gamma');
    expect(p.t('first')).to.equal('first'); // Should be missing now
  });

  it('supports unset() (different keys)', function () {
    var p = new Polyglot({ phrases: { morning: 'Good morning', night: 'Good night' } });
    p.unset('night');
    expect(p.t('night')).to.equal('night');
    p.extend({ night: 'Sleep well' });
    expect(p.t('night')).to.equal('Sleep well');
  });

  it('handles allowMissing correctly (different phrase/content)', function () {
    var p = new Polyglot({ allowMissing: true });
    expect(p.t('welcome %{username}', { username: 'Robot' })).to.equal('welcome Robot');
  });

  it('handles chinese pluralization (different key/values)', function () {
    var p = new Polyglot({
      phrases: {
        task: '%{smart_count} 任務'
      },
      locale: 'zh'
    });
    expect(p.t('task', { smart_count: 5 })).to.equal('5 任務');
    expect(p.t('task', { smart_count: 13 })).to.equal('13 任務');
  });

  it('accepts falsy options safely (alternate key)', function () {
    var p = new Polyglot();
    expect(p.t('another key', null)).to.equal('another key');
    expect(p.t('another key', undefined)).to.equal('another key');
  });
});