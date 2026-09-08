const test = require('tape');
const deepEqual = require('../index.js');

test('circular references equal (different property name)', function (t) {
    const obj1 = {};
    obj1.loop = obj1;
    const obj2 = {};
    obj2.loop = obj2;
    t.ok(deepEqual(obj1, obj2), 'self-referential objects are equal (with property "loop")');
    t.end();
});

test('circular references not equal (different structure)', function (t) {
    const obj1 = {};
    obj1.foo = obj1;
    const obj2 = {};
    obj2.foo = {};
    t.notOk(deepEqual(obj1, obj2), 'one is circular, one is not');
    t.end();
});