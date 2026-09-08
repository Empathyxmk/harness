const test = require('tape');
const deepEqual = require('../index.js');

test('error objects equal', function (t) {
    const err1 = new Error('fail');
    const err2 = new Error('fail');
    t.ok(deepEqual(err1, err2), 'equal errors');
    t.end();
});

test('error objects not equal', function (t) {
    const err1 = new Error('fail');
    const err2 = new Error('success');
    t.notOk(deepEqual(err1, err2), 'different errors');
    t.end();
});