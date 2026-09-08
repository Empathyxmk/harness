const test = require('tape');
const deepEqual = require('../index.js');

test('primitives (public): booleans', function (t) {
    t.ok(deepEqual(true, true), 'true deepEqual true');
    t.notOk(deepEqual(true, false), 'true not deepEqual false');
    t.notOk(deepEqual(false, 0), 'false not deepEqual 0');
    t.end();
});

test('primitives (public): null and undefined', function (t) {
    t.ok(deepEqual(undefined, undefined), 'undefined deepEqual undefined');
    t.ok(deepEqual(null, null), 'null deepEqual null');
    t.notOk(deepEqual(null, undefined), 'null not deepEqual undefined');
    t.end();
});

test('numbers (public)', function (t) {
    t.ok(deepEqual(123, 123), '123 deepEqual 123');
    t.notOk(deepEqual(123, 321), '123 not deepEqual 321');
    t.notOk(deepEqual(123, "123"), 'number not deepEqual string');
    t.end();
});

test('strings (public)', function (t) {
    t.ok(deepEqual('world', 'world'), '"world" deepEqual "world"');
    t.notOk(deepEqual('world', 'WORLD'), '"world" not deepEqual "WORLD"');
    t.notOk(deepEqual('world', 123), 'string not deepEqual number');
    t.end();
});

test('arrays (public)', function (t) {
    t.ok(deepEqual([4, 5, 6], [4, 5, 6]), '[4,5,6] deepEqual [4,5,6]');
    t.notOk(deepEqual([4, 5, 6], [6, 5, 4]), '[4,5,6] not deepEqual [6,5,4]');
    t.notOk(deepEqual([4, 5], [4, 5, 6]), '[4,5] not deepEqual [4,5,6]');
    t.end();
});

test('objects (public)', function (t) {
    t.ok(deepEqual({ b: 2, a: 1 }, { a: 1, b: 2 }), '{b:2,a:1} deepEqual {a:1,b:2}');
    t.notOk(deepEqual({ a: 1, b: 3 }, { a: 1, b: 2 }), '{a:1,b:3} not deepEqual {a:1,b:2}');
    t.notOk(deepEqual({ a: 1 }, { a: 1, b: 2 }), '{a:1} not deepEqual {a:1,b:2}');
    t.end();
});

test('nested objects and arrays (public)', function (t) {
    const a = { c: [4, { d: 5 }], e: { f: 7 } };
    const b = { c: [4, { d: 5 }], e: { f: 7 } };
    const c = { c: [4, { d: 8 }], e: { f: 7 } };
    t.ok(deepEqual(a, b), 'deep nested objects and arrays are deepEqual');
    t.notOk(deepEqual(a, c), 'different nested values not deepEqual');
    t.end();
});