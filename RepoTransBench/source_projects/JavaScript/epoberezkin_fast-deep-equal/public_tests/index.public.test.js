const equal = require('../index');

describe('fast-deep-equal - index.js (public)', () => {
  it('should return true for equal primitives (public)', () => {
    expect(equal(42, 42)).toBe(true);
    expect(equal('public', 'public')).toBe(true);
    expect(equal(null, null)).toBe(true);
    expect(equal(undefined, undefined)).toBe(true);
    expect(equal(false, false)).toBe(true);
    expect(equal(true, true)).toBe(true);
  });

  it('should return false for different primitives (public)', () => {
    expect(equal(99, 100)).toBe(false);
    expect(equal('alpha', 'beta')).toBe(false);
    expect(equal(undefined, false)).toBe(false);
    expect(equal(false, true)).toBe(false);
  });

  it('should handle objects: equal and not equal (public)', () => {
    expect(equal({x: 9}, {x: 9})).toBe(true);
    expect(equal({x: 9}, {x: 10})).toBe(false);
    expect(equal({a: 2}, {b: 2})).toBe(false);
    expect(equal({first: 1, second: 2}, {second: 2, first: 1})).toBe(true);
    expect(equal({tag: 'open'}, {tag: 'open'})).toBe(true);
    expect(equal({}, {})).toBe(true);
  });

  it('should handle arrays: equal and not equal (public)', () => {
    expect(equal([10,20,30], [10,20,30])).toBe(true);
    expect(equal([10,20,30], [10,20])).toBe(false);
    expect(equal([5,6,7], [7,6,5])).toBe(false);
    expect(equal([], [])).toBe(true);
  });

  it('should handle nested structures (public)', () => {
    expect(equal({x: [5,6,{y:7}]}, {x: [5,6,{y:7}]})).toBe(true);
    expect(equal({x: [5,6,{y:7}]}, {x: [5,6,{y:8}]})).toBe(false);
  });

  it('should handle RegExp (public)', () => {
    expect(equal(/b/i, /b/i)).toBe(true);
    expect(equal(/b/i, /b/g)).toBe(false);
    expect(equal(/b/, /c/)).toBe(false);
  });

  it('should handle different constructors (public)', () => {
    expect(equal({}, new Date())).toBe(false);
    function FooBar() {this.y=5;}
    function Baz() {this.y=5;}
    const fooBar = new FooBar();
    const baz = new Baz();
    expect(equal(fooBar, baz)).toBe(false);
  });

  it('should handle .valueOf property (public)', () => {
    function Val(u) { this.u = u; }
    Val.prototype.valueOf = function() { return this.u; };
    const d = new Val(99);
    const e = new Val(99);
    const f = new Val(100);
    expect(equal(d, e)).toBe(true);
    expect(equal(d, f)).toBe(false);

    const o1 = { valueOf: () => 10 };
    const o2 = { valueOf: () => 10 };
    expect(equal(o1, o2)).toBe(true);
    const o3 = { valueOf: () => 11 };
    expect(equal(o1, o3)).toBe(false);
  });

  it('should handle .toString property (public)', () => {
    const a = {toString() { return 'baz'; }};
    const b = {toString() { return 'baz'; }};
    const c = {toString() { return 'qux'; }};
    expect(equal(a, b)).toBe(true);
    expect(equal(a, c)).toBe(false);
  });

  it('should handle objects with missing keys (public)', () => {
    expect(equal({x:5, y:8}, {x:5})).toBe(false);
    expect(equal({x:5}, {x:5, y:8})).toBe(false);
  });

  it('should handle objects with extra keys (public)', () => {
    expect(equal({x:7, y:undefined}, {x:7})).toBe(false);
  });

  it('should handle hasOwnProperty edge case (public)', () => {
    const a = Object.create(null);
    const b = Object.create(null);
    a.k = 14; b.k = 14;
    a.valueOf = function() { return '[x]'; };
    b.valueOf = function() { return '[x]'; };
    expect(equal(a, b)).toBe(true);
    b.z = 9;
    b.valueOf = function() { return '[y]'; };
    expect(equal(a, b)).toBe(false);
  });

  it('should handle NaN (public)', () => {
    expect(equal(NaN, NaN)).toBe(true);
    expect(equal(NaN, 99)).toBe(false);
    expect(equal(99, NaN)).toBe(false);
  });

  it('should return false for non-object/primitive (public)', () => {
    expect(equal(100, {value:100})).toBe(false);
    expect(equal([3,4], {0:3,1:4})).toBe(false);
  });

  it('should handle deeply nested (equal and not equal, public)', () => {
    const obj1 = {p: {q: {r:[8,9,'x'], s: 't'}}};
    const obj2 = {p: {q: {r:[8,9,'x'], s: 't'}}};
    const obj3 = {p: {q: {r:[8,9,'y'], s: 't'}}};
    expect(equal(obj1, obj2)).toBe(true);
    expect(equal(obj1, obj3)).toBe(false);
  });

  it('should not throw on objects with null prototype (no valueOf/toString, public)', () => {
    const a = Object.create(null);
    const b = Object.create(null);
    a.alpha = 456; b.alpha = 456;
    a.valueOf = Object.prototype.valueOf;
    b.valueOf = Object.prototype.valueOf;
    a.toString = Object.prototype.toString;
    b.toString = Object.prototype.toString;
    expect(equal(a, b)).toBe(true);
  });
});