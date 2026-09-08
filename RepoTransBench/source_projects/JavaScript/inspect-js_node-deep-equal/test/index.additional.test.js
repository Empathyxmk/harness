const test = require('tape');
const deepEqual = require('../index.js');

test('handles NaN comparisons (consistent with implementation)', function (t) {
  // The current implementation of deepEqual does NOT treat NaN as equal to NaN,
  // so we expect this to fail.
  t.notOk(deepEqual(NaN, NaN), 'NaN not deepEqual NaN per implementation');
  t.notOk(deepEqual(NaN, 5), 'NaN not deepEqual non-NaN');
  t.end();
});

test('handles +0 and -0 comparisons', function (t) {
  t.ok(deepEqual(+0, -0), '+0 deepEqual -0');
  t.end();
});

test('handles RegExp equality', function (t) {
  t.ok(deepEqual(/abc/i, /abc/i), 'Equivalent RegExp objects');
  t.notOk(deepEqual(/abc/i, /abc/), 'Different flags on RegExp');
  t.notOk(deepEqual(/abc/i, /def/i), 'Different patterns on RegExp');
  t.end();
});

test('handles Date equality', function (t) {
  t.ok(deepEqual(new Date('2023-01-01'), new Date('2023-01-01')), 'Equivalent dates');
  t.notOk(deepEqual(new Date('2023-01-01'), new Date('2022-01-01')), 'Different dates');
  t.end();
});

test('handles complex nested structures', function (t) {
  const a = { arr: [1, { z: 2 }, [3, 4]], obj: { x: 1, y: [{ q: 8 }] } };
  const b = { arr: [1, { z: 2 }, [3, 4]], obj: { x: 1, y: [{ q: 8 }] } };
  const c = { arr: [1, { z: 3 }, [3, 4]], obj: { x: 1, y: [{ q: 8 }] } };
  t.ok(deepEqual(a, b), 'equivalent complex nested structures');
  t.notOk(deepEqual(a, c), 'different nested values');
  t.end();
});

test('handles arguments objects', function (t) {
  function foo(a, b) { return arguments; }
  const args1 = foo(1, 2);
  const args2 = foo(1, 2);
  const args3 = foo(2, 3);
  t.ok(deepEqual(args1, args2), 'same arguments');
  t.notOk(deepEqual(args1, args3), 'different arguments');
  t.end();
});

test('different constructors with same properties (implementation: treated as equal)', function (t) {
  function Foo() { this.x = 5; }
  function Bar() { this.x = 5; }
  // Based on the implementation, objects with different constructors but same properties are treated as equal.
  // We expect this to return true; so .ok:
  t.ok(deepEqual(new Foo(), new Bar()), 'different constructors are deepEqual per implementation');
  t.end();
});

test('buffers', function (t) {
  const a = Buffer.from([1, 2, 3]);
  const b = Buffer.from([1, 2, 3]);
  const c = Buffer.from([1, 2, 4]);
  t.ok(deepEqual(a, b), 'equal buffers');
  t.notOk(deepEqual(a, c), 'unequal buffers');
  t.end();
});

test('maps and sets', function (t) {
  if (typeof Map !== 'undefined' && typeof Set !== 'undefined') {
    let m1 = new Map([[1, 'a'], [2, 'b']]);
    let m2 = new Map([[1, 'a'], [2, 'b']]);
    let m3 = new Map([[1, 'a'], [2, 'c']]);
    t.ok(deepEqual(m1, m2), 'equal maps');
    t.notOk(deepEqual(m1, m3), 'unequal maps');

    let s1 = new Set([1, 2, 3]);
    let s2 = new Set([1, 2, 3]);
    let s3 = new Set([1, 2, 4]);
    t.ok(deepEqual(s1, s2), 'equal sets');
    t.notOk(deepEqual(s1, s3), 'unequal sets');
  }
  t.end();
});

test('functions are only equal by reference', function (t) {
  function a() { return 1; }
  function b() { return 1; }
  t.ok(deepEqual(a, a), 'function is equal to itself');
  t.notOk(deepEqual(a, b), 'identical function code, different identity');
  t.end();
});