const test = require('tape');
const assert = require('../assert.js');

test('assert.ok (public)', function (t) {
    t.doesNotThrow(function () { assert.ok(456); }, 'ok does not throw on 456');
    t.throws(function () { assert.ok(false); }, 'ok throws on false');
    t.end();
});

test('assert.equal (public)', function (t) {
    t.doesNotThrow(function () { assert.equal('abc', 'abc'); }, 'equal "abc" == "abc"');
    t.throws(function () { assert.equal('abc', 'def'); }, 'equal "abc" != "def"');
    t.end();
});

test('assert.deepEqual (public)', function (t) {
    t.doesNotThrow(function () { assert.deepEqual([9], [9]); }, 'deepEqual [9] == [9]');
    t.throws(function () { assert.deepEqual([9], [10]); }, 'deepEqual [9] != [10]');
    t.end();
});

test('assert.notDeepEqual (public)', function (t) {
    t.doesNotThrow(function () { assert.notDeepEqual([1, 2], [2, 1]); }, 'notDeepEqual [1,2] != [2,1]');
    t.throws(function () { assert.notDeepEqual([3], [3]); }, 'notDeepEqual [3] == [3]');
    t.end();
});