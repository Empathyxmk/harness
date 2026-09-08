const test = require('tape');
const deepEqual = require('../index.js');

test('handles NaN comparisons (public/consistent with implementation)', function (t) {
  // Implementation: NaN !== NaN.
  t.notOk(deepEqual(Number('foo'), Number('foo')), 'NaN not deepEqual NaN (public test #1)');
  t.notOk(deepEqual(Number('foo'), 42), 'NaN not deepEqual non-NaN (public test #2)');
  t.end();
});

test('handles +0 and -0 comparisons (public test)', function (t) {
  t.ok(deepEqual(-0, +0), '-0 deepEqual +0 (public)');
  t.end();
});

test('handles RegExp equality (different pattern and flags)', function (t) {
  t.ok(deepEqual(/def/g, /def/g), 'Equivalent RegExp "def/g"');
  t.notOk(deepEqual(/def/g, /def/i), 'RegExp different flags');
  t.notOk(deepEqual(/abc/g, /def/g), 'RegExp different pattern');
  t.end();
});

test('handles Date equality (public dates)', function (t) {
  t.ok(deepEqual(new Date('2022-07-15'), new Date('2022-07-15')), 'Equivalent dates (public)');
  t.notOk(deepEqual(new Date('2022-07-15'), new Date('2023-07-15')), 'Different dates (public)');
  t.end();
});

test('handles different complex nested structures', function (t) {
  const x = { arr: [5, { n: 10 }, [7, 8]], obj: { a: 9, b: [{ f: 20 }] } };
  const y = { arr: [5, { n: 10 }, [7, 8]], obj: { a: 9, b: [{ f: 20 }] } };
  const z = { arr: [5, { n: 12 }, [7, 8]], obj: { a: 9, b: [{ f: 20 }] } };
  t.ok(deepEqual(x, y), 'equivalent different complex nested structures');
  t.notOk(deepEqual(x, z), 'different nested values in public test');
  t.end();
});

test('handles arguments objects (public test)', function (t) {
  function bar(x, y, z) { return arguments; }
  const args1 = bar(3, 4, 5);
  const args2 = bar(3, 4, 5);
  const args3 = bar(7, 8, 9);
  t.ok(deepEqual(args1, args2), 'same arguments (public)');
  t.notOk(deepEqual(args1, args3), 'different arguments (public)');
  t.end();
});

test('different constructors with identical properties (public)', function (t) {
  function Apple() { this.kind = 'fruit'; }
  function Orange() { this.kind = 'fruit'; }
  t.ok(deepEqual(new Apple(), new Orange()), 'different constructors are deepEqual (public)');
  t.end();
});

test('buffers (public test)', function (t) {
  const bufA = Buffer.from([10, 20, 30]);
  const bufB = Buffer.from([10, 20, 30]);
  const bufC = Buffer.from([10, 20, 31]);
  t.ok(deepEqual(bufA, bufB), 'equal buffers (public)');
  t.notOk(deepEqual(bufA, bufC), 'unequal buffers (public)');
  t.end();
});

test('maps and sets (different data, public)', function (t) {
  if (typeof Map !== 'undefined' && typeof Set !== 'undefined') {
    let m1 = new Map([[10, 'x'], [20, 'y']]);
    let m2 = new Map([[10, 'x'], [20, 'y']]);
    let m3 = new Map([[10, 'x'], [20, 'z']]);
    t.ok(deepEqual(m1, m2), 'equal maps (public)');
    t.notOk(deepEqual(m1, m3), 'unequal maps (public)');

    let s1 = new Set([9, 8, 7]);
    let s2 = new Set([9, 8, 7]);
    let s3 = new Set([9, 8, 6]);
    t.ok(deepEqual(s1, s2), 'equal sets (public)');
    t.notOk(deepEqual(s1, s3), 'unequal sets (public)');
  }
  t.end();
});

test('functions are only equal by reference (public)', function (t) {
  function foo() { return 2; }
  function bar() { return 2; }
  t.ok(deepEqual(foo, foo), 'function is equal to itself (public)');
  t.notOk(deepEqual(foo, bar), 'different function identity (public)');
  t.end();
});