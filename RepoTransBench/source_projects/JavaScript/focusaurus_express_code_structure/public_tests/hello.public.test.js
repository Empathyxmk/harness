const test = require('tape');

test('Dummy public test: addition works with new data', t => {
    t.equal(7 + 13, 20, 'Sum of 7 and 13 should be 20');
    t.equal(21 + 33, 54, 'Sum of 21 and 33 should be 54');
    t.end();
});