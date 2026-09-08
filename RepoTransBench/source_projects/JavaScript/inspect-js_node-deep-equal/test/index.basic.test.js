const test = require('tape');
const deepEqual = require('../index.js');

test('primitive equal', function (t) {
    t.ok(deepEqual(1, 1), 'numbers equal');
    t.ok(deepEqual('a', 'a'), 'strings equal');
    t.ok(deepEqual(true, true), 'booleans equal');
    t.end();
});

test('primitive not equal', function (t) {
    t.notOk(deepEqual(1, 2), 'numbers not equal');
    t.notOk(deepEqual('a', 'b'), 'strings not equal');
    t.notOk(deepEqual(true, false), 'booleans not equal');
    t.end();
});

test('object equal', function (t) {
    t.ok(deepEqual({a:1}, {a:1}), 'simple objects equal');
    t.end();
});

test('object not equal', function (t) {
    t.notOk(deepEqual({a:1}, {b:1}), 'objects with different keys not equal');
    t.notOk(deepEqual({a:1}, {a:2}), 'objects with different values not equal');
    t.end();
});

test('array equal', function (t) {
    t.ok(deepEqual([1,2,3], [1,2,3]), 'arrays equal');
    t.end();
});

test('array not equal', function (t) {
    t.notOk(deepEqual([1,2,3], [1,2]), 'arrays of different lengths not equal');
    t.notOk(deepEqual([1,2,3], [3,2,1]), 'arrays with different order not equal');
    t.end();
});