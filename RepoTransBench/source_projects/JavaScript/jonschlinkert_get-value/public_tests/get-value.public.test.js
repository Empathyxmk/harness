const { expect } = require('chai');
const getValue = require('../index.js').default || require('../index.js');

/* 
Public test suite for get-value.
Covers various usages using different input/output data than any likely internal tests.
*/

// 1. Basic property access, different keys and values
describe('get-value public: basic property access', () => {
  it('should get property from top-level object', () => {
    expect(getValue({engine: 'v8'}, 'engine')).to.equal('v8');
  });

  it('should return undefined for non-existent property', () => {
    expect(getValue({foo: 123}, 'bar')).to.equal(undefined);
  });
});

// 2. Nested property access with string path, new structure
describe('get-value public: deep property via string path', () => {
  it('should get deeply nested property', () => {
    const obj = {a: {b: {c: 'deepValue'}}};
    expect(getValue(obj, 'a.b.c')).to.equal('deepValue');
  });

  it('should return default value if property does not exist', () => {
    const obj = {x: {y: {z: 0}}};
    expect(getValue(obj, 'x.y.w', {default: 'notfound'})).to.equal('notfound');
  });
});

// 3. Nested property access with array path, different nesting
describe('get-value public: deep property via array path', () => {
  it('should get nested property via array path', () => {
    const obj = {john: {profile: {age: 42}}};
    expect(getValue(obj, ['john', 'profile', 'age'])).to.equal(42);
  });

  it('should return default for wrong path with array', () => {
    const obj = {one: {two: 2}};
    expect(getValue(obj, ['one', 'three'], {default: 99})).to.equal(99);
  });
});

// 4. Numeric paths (array index) and number coercion, with different data
describe('get-value public: array index', () => {
  it('should access array index property', () => {
    const arr = ['zero', 'uno', 'dos'];
    expect(getValue(arr, 2)).to.equal('dos');
  });

  it('should return default for missing array index', () => {
    const arr = [5,4,3];
    expect(getValue(arr, 10, {default: 'empty'})).to.equal('empty');
  });
});

// 5. Option: custom separator and joinChar
describe('get-value public: custom separators', () => {
  it('should use custom separator', () => {
    const obj = {'foo/bar': {baz: 'zzz'}};
    expect(getValue(obj, 'foo/bar.baz', {separator: '.'})).to.equal('zzz');
  });

  it('should use custom separator (other char)', () => {
    const obj = {'p|q': {'r': 12}};
    expect(getValue(obj, 'p|q|r', {separator: '|'})).to.equal(12);
  });
});

// 6. Escaped separator property name (with \)
describe('get-value public: escaped dots', () => {
  it('should get property with literal dot in name', () => {
    const obj = {'main.sub': {'x': 'val'}};
    expect(getValue(obj, 'main\\.sub.x')).to.equal('val');
  });

  it('should get property with double backslash escape', () => {
    const obj = {'level1\\level2': {leaf: 'leafy'}};
    expect(getValue(obj, 'level1\\\\level2.leaf', {separator: '.'})).to.equal('leafy');
  });
});

// 7. isValid and split/join function options (custom scenario)
describe('get-value public: custom validation and split/join', () => {
  it('should use custom isValid to deny property', () => {
    const obj = {block: {safe: 'yes'}};
    const options = {isValid: (key, target) => key !== 'block'};
    expect(getValue(obj, 'block.safe', options)).to.equal(undefined);
  });

  it('should use custom split and join functions for paths', () => {
    const obj = {'a___b': {'c': 101}};
    const options = {
      split: p => p.split('***'),
      join: segs => segs.join('___')
    };
    expect(getValue(obj, 'a***b.c', options)).to.equal(101);
  });
});

// 8. Non-object targets and default value behavior
describe('get-value public: non-object target', () => {
  it('should return default for null input', () => {
    expect(getValue(null, 'abc', {default: 'fallback'})).to.equal('fallback');
  });
  it('should return primitive target if no valid object', () => {
    expect(getValue('primitive', 'anything')).to.equal('primitive');
  });
});

// 9. Function as object target (should behave as object)
describe('get-value public: function as target', () => {
  it('should get property of a function target', () => {
    function foo() {}
    foo.bar = 'bazfunc';
    expect(getValue(foo, 'bar')).to.equal('bazfunc');
  });
});

// 10. Path is array, property name as number key string
describe('get-value public: number key as string', () => {
  it('should return value for number key as string', () => {
    const obj = {'12': 'dozen'};
    expect(getValue(obj, ['12'])).to.equal('dozen');
  });
});