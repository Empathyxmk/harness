/* global describe, it */

'use strict'

const assert = require('assert');
const sprintfjs = require('../src/sprintf.js');
const sprintf = sprintfjs.sprintf;
const vsprintf = sprintfjs.vsprintf;

function should_throw(format, args, err) {
    assert.throws(function() { vsprintf(format, args) }, err);
}

function should_not_throw(format, args) {
    assert.doesNotThrow(function() { vsprintf(format, args) });
}

describe('sprintfjs-public cache', function() {
    it('should not throw Error (public cache consistency)', function() {
        // Use some different strings to stimulate cache changes
        sprintf('toString')
        sprintf('valueOf')
        should_not_throw('%s', ['testing cache...'])
        should_not_throw('%s', ['does this break?'])
    })
})

describe('sprintfjs-public', function() {
    it('should throw SyntaxError for some new placeholders', function() {
        should_throw('%z', [], SyntaxError)
        should_throw('%Y', [], SyntaxError)
        should_throw('%s%%%', [], SyntaxError)
        should_throw('%(foo', [], SyntaxError)
        should_throw('%)foo', [], SyntaxError)
        should_throw('%@s', [], SyntaxError)
        should_throw('%()foo', [], SyntaxError)
        should_throw('%(7)s', [], SyntaxError)
    })

    const numeric = 'bcdiefguxX'.split('');
    numeric.forEach(function(specifier) {
        const fmt = sprintf('%%%s', specifier)
        it(fmt + ' should throw TypeError for missing numbers', function() {
            should_throw(fmt, [], TypeError)
        })
    });

    it('%s should throw TypeError for null/undefined', function() {
        should_throw('%s', [undefined], TypeError)
        should_throw('%s', [null], TypeError)
    })

    it('%d should throw TypeError for strings/objects', function() {
        should_throw('%d', ['foo'], TypeError)
        should_throw('%d', [{}], TypeError)
    })

    it('should not throw for valid specifier values', function() {
        should_not_throw('%d', [7])
        should_not_throw('%s', ['bar'])
    })
})