const test = require('tape');
const assert = require('../assert.js');

test('assert.js: simple assertion', function (t) {
    t.plan(1);
    try {
        assert(true, 'Should not throw');
        t.pass('Does not throw on true');
    } catch (e) {
        t.fail('Throw on true');
    }
});

test('assert.js: assertion throws on false', function (t) {
    t.plan(2);
    try {
        assert(false, 'Should throw');
        t.fail('Did not throw');
    } catch (e) {
        t.pass('Throws on false');
        t.equal(e.message, 'Should throw');
    }
});