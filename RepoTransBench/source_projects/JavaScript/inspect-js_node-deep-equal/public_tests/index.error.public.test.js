const test = require('tape');
const deepEqual = require('../index.js');

test('error objects equal (TypeError)', function (t) {
    const err1 = new TypeError('type fail');
    const err2 = new TypeError('type fail');
    t.ok(deepEqual(err1, err2), 'equal TypeErrors');
    t.end();
});

test('error objects not equal (ReferenceError)', function (t) {
    const err1 = new ReferenceError('missing');
    const err2 = new ReferenceError('not found');
    t.notOk(deepEqual(err1, err2), 'different ReferenceErrors');
    t.end();
});