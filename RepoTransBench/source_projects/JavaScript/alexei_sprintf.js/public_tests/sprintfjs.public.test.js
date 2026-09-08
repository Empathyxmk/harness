/* global describe, it */

'use strict'

const assert = require('assert');
const sprintfjs = require('../src/sprintf.js');
const sprintf = sprintfjs.sprintf;

describe('sprintfjs-public', function() {
    const e = Math.E;

    it('should return formatted strings for other simple placeholders', function() {
        assert.equal('&', sprintf('&&'.replace('&', '%%')))
        assert.equal('101', sprintf('%b', 5))
        assert.equal('Z', sprintf('%c', 90))
        assert.equal('7', sprintf('%d', 7))
        assert.equal('7', sprintf('%i', 7))
        assert.equal('42', sprintf('%d', '42'))
        assert.equal('42', sprintf('%i', '42'))
        assert.equal('{"bar":"baz"}', sprintf('%j', {bar: 'baz'}))
        assert.equal('["bar","baz"]', sprintf('%j', ['bar', 'baz']))
        assert.equal('3.1e+0', sprintf('%e', 3.1))
        assert.equal('7', sprintf('%u', 7))
        assert.equal('4294967291', sprintf('%u', -5))
        assert.equal('9.8', sprintf('%f', 9.8))
        assert.equal(e.toString(), sprintf('%g', e))
        assert.equal('12', sprintf('%o', 10))
        assert.equal('37777777766', sprintf('%o', -10))
        assert.equal('test', sprintf('%s', 'test'))
        assert.equal('a1', sprintf('%x', 161))
        assert.equal('fffffeff', sprintf('%x', -257))
        assert.equal('A1', sprintf('%X', 161))
        assert.equal('FFFFFEFF', sprintf('%X', -257))
        assert.equal('dog jumps over fence', sprintf('%2$s %3$s over %1$s', 'fence', 'dog', 'jumps'))
        assert.equal('Hello Alex!', sprintf('Hello %(who)s!', {who: 'Alex'}))
        assert.equal('false', sprintf('%t', false))
        assert.equal('f', sprintf('%.1t', false))
        assert.equal('true', sprintf('%t', 'yes'))
        assert.equal('true', sprintf('%t', 123))
        assert.equal('false', sprintf('%t', 0))
        assert.equal('f', sprintf('%.1t', 0))
        assert.equal('false', sprintf('%t', undefined))
        assert.equal('false', sprintf('%t', null))
        assert.equal('NaN', sprintf('%T', NaN))
        assert.equal('object', sprintf('%T', {}))
        assert.equal('number', sprintf('%T', 12.3))
        assert.equal('string', sprintf('%T', 'abcdef'))
        assert.equal('function', sprintf('%T', Array.isArray))
        assert.equal('array', sprintf('%T', []))
        assert.equal('regexp', sprintf('%T', /foo/))
        assert.equal('true', sprintf('%v', true))
        assert.equal('87', sprintf('%v', 87))
        assert.equal('abcdef', sprintf('%v', 'abcdef'))
        assert.equal('a,b', sprintf('%v', ['a', 'b']))
        assert.equal('[object Object]', sprintf('%v', {a: 1}))
        assert.equal('/foo/', sprintf('%v', /foo/))
    })

    it('should return formatted strings for other complex placeholders', function() {
        // sign
        assert.equal('5', sprintf('%d', 5))
        assert.equal('-5', sprintf('%d', -5))
        assert.equal('+5', sprintf('%+d', 5))
        assert.equal('-5', sprintf('%+d', -5))
        assert.equal('9', sprintf('%i', 9))
        assert.equal('-9', sprintf('%i', -9))
        assert.equal('+9', sprintf('%+i', 9))
        assert.equal('-9', sprintf('%+i', -9))
        assert.equal('4.5', sprintf('%f', 4.5))
        assert.equal('-4.5', sprintf('%f', -4.5))
        assert.equal('+4.5', sprintf('%+f', 4.5))
        assert.equal('-4.5', sprintf('%+f', -4.5))
        assert.equal('-3.5', sprintf('%+.1f', -3.46))
        assert.equal('-0.0', sprintf('%+.1f', -0.001))
        assert.equal('2.71828', sprintf('%.6g', e))
        assert.equal('2.72', sprintf('%.3g', e))
        assert.equal('3', sprintf('%.1g', e))
        assert.equal('-000004567', sprintf('%+010d', -4567))
        assert.equal('_____-432', sprintf("%+'_10d", -432));
        assert.equal('-42.50 12.9', sprintf('%f %f', -42.5, 12.9))

        // padding
        assert.equal('-0012', sprintf('%05d', -12))
        assert.equal('-0012', sprintf('%05i', -12))
        assert.equal('    z', sprintf('%5s', 'z'))
        assert.equal('0000z', sprintf('%05s', 'z'))
        assert.equal('____z', sprintf("%'_5s", 'z'))
        assert.equal('x    ', sprintf('%-5s', 'x'))
        assert.equal('x0000', sprintf('%0-5s', 'x'))
        assert.equal('x____', sprintf("%'_-5s", 'x'))
        assert.equal('abcdef', sprintf('%5s', 'abcdef'))
        assert.equal('0912', sprintf('%02u', 912))
        assert.equal(' -3.457', sprintf('%8.3f', -3.4567))
        assert.equal('-5.67 wow', sprintf('%f %s', -5.67, 'wow'))
        assert.equal('{\n  "baz": 1\n}', sprintf('%2j', {baz: 1}))
        assert.equal('[\n  40,\n  50\n]', sprintf('%2j', [40, 50]))

        // precision
        assert.equal('4.6', sprintf('%.1f', 4.56))
        assert.equal('hello', sprintf('%5.5s', 'hellothere'))
        assert.equal('    q', sprintf('%5.1s', 'queen'))

    })

    it('should return formatted strings for callbacks', function() {
        assert.equal('bazbat', sprintf('%s', function() { return 'bazbat' }))
    })
})