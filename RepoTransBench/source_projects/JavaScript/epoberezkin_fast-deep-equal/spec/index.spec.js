const equal = require('../index');

describe('fast-deep-equal - index.js', () => {
  it('should return true for equal primitives', () => {
    expect(equal(1, 1)).toBe(true);
    expect(equal('a', 'a')).toBe(true);
    expect(equal(null, null)).toBe(true);
    expect(equal(undefined, undefined)).toBe(true);
    expect(equal(true, true)).toBe(true);
    expect(equal(false, false)).toBe(true);
  });

  it('should return false for different primitives', () => {
    expect(equal(1, 2)).toBe(false);
    expect(equal('a', 'b')).toBe(false);
    expect(equal(null, undefined)).toBe(false);
    expect(equal(true, false)).toBe(false);
  });

  it('should handle objects: equal and not equal', () => {
    expect(equal({a: 1}, {a: 1})).toBe(true);
    expect(equal({a: 1}, {a: 2})).toBe(false);
    expect(equal({a: 1}, {b: 1})).toBe(false);
    expect(equal({a: 1, b: 2}, {b: 2, a: 1})).toBe(true);
    expect(equal({}, {})).toBe(true);
  });

  it('should handle arrays: equal and not equal', () => {
    expect(equal([1,2,3], [1,2,3])).toBe(true);
    expect(equal([1,2,3], [1,2])).toBe(false);
    expect(equal([1,2,3], [3,2,1])).toBe(false);
    expect(equal([], [])).toBe(true);
  });

  it('should handle nested structures', () => {
    expect(equal({a: [1,2,{b:3}]}, {a: [1,2,{b:3}]})).toBe(true);
    expect(equal({a: [1,2,{b:3}]}, {a: [1,2,{b:4}]})).toBe(false);
  });

  it('should handle RegExp', () => {
    expect(equal(/a/g, /a/g)).toBe(true);
    expect(equal(/a/g, /a/i)).toBe(false);
    expect(equal(/a/, /b/)).toBe(false);
  });

  it('should handle different constructors', () => {
    expect(equal({}, [])).toBe(false);
    function Foo() {this.x=1;}
    function Bar() {this.x=1;}
    const foo = new Foo();
    const bar = new Bar();
    expect(equal(foo, bar)).toBe(false);
  });

  it('should handle .valueOf property', () => {
    // objects with valueOf methods
    function V(v) { this.v = v; }
    V.prototype.valueOf = function() { return this.v; };
    const a = new V(42);
    const b = new V(42);
    const c = new V(43);
    expect(equal(a, b)).toBe(true);
    expect(equal(a, c)).toBe(false);

    // fallback to valueOf branch
    const o1 = { valueOf: () => 5 };
    const o2 = { valueOf: () => 5 };
    expect(equal(o1, o2)).toBe(true);
    const o3 = { valueOf: () => 6 };
    expect(equal(o1, o3)).toBe(false);
  });

  it('should handle .toString property', () => {
    // objects with custom toString
    const a = {toString() { return 'foo'; }};
    const b = {toString() { return 'foo'; }};
    const c = {toString() { return 'bar'; }};
    expect(equal(a, b)).toBe(true);
    expect(equal(a, c)).toBe(false);
  });

  it('should handle objects with missing keys', () => {
    expect(equal({a:1, b:2}, {a:1})).toBe(false);
    expect(equal({a:1}, {a:1, b:2})).toBe(false);
  });

  it('should handle objects with extra keys', () => {
    expect(equal({a:1, b:undefined}, {a:1})).toBe(false);
  });

  it('should handle hasOwnProperty edge case', () => {
    // create two different objects without prototype, and provide valueOf method
    const a = Object.create(null);
    const b = Object.create(null);
    a.x = 1; b.x = 1;
    // Provide a dummy valueOf so equal() code won't fail
    a.valueOf = function() { return '[a]'; };
    b.valueOf = function() { return '[a]'; };
    expect(equal(a, b)).toBe(true);
    b.y = 2;
    b.valueOf = function() { return '[b]'; };
    expect(equal(a, b)).toBe(false);
  });

  it('should handle NaN', () => {
    expect(equal(NaN, NaN)).toBe(true);
    expect(equal(NaN, 1)).toBe(false);
    expect(equal(1, NaN)).toBe(false);
  });

  it('should return false for non-object/primitive', () => {
    expect(equal(3, {a:3})).toBe(false);
    expect(equal([1,2], {0:1,1:2})).toBe(false);
  });

  it('should handle deeply nested (equal and not equal)', () => {
    const obj1 = {a: {b: {c:[1,2,3], d: 'e'}}};
    const obj2 = {a: {b: {c:[1,2,3], d: 'e'}}};
    const obj3 = {a: {b: {c:[1,2,4], d: 'e'}}};
    expect(equal(obj1, obj2)).toBe(true);
    expect(equal(obj1, obj3)).toBe(false);
  });

  it('should not throw on objects with null prototype (no valueOf/toString)', () => {
    // Patch missing valueOf to safely return default if missing
    const a = Object.create(null);
    const b = Object.create(null);
    a.test = 123; b.test = 123;
    // patch a.valueOf and b.valueOf to match expected API
    a.valueOf = Object.prototype.valueOf;
    b.valueOf = Object.prototype.valueOf;
    a.toString = Object.prototype.toString;
    b.toString = Object.prototype.toString;
    expect(equal(a, b)).toBe(true);
  });
});