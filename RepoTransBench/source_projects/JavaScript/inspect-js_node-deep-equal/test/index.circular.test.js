const test = require('tape');
const deepEqual = require('../index.js');

test('circular references equal', function (t) {
    const obj1 = {};
    obj1.self = obj1;
    const obj2 = {};
    obj2.self = obj2;
    t.ok(deepEqual(obj1, obj2), 'self-referential objects are equal');
    t.end();
});

test('circular references not equal', function (t) {
    const obj1 = {};
    obj1.self = obj1;
    const obj2 = {};
    t.notOk(deepEqual(obj1, obj2), 'one circular, one not');
    t.end();
});