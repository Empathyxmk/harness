import assert from 'assert';
import getValue from '../index';

describe('get-value', () => {
  it('should get a direct property', () => {
    const obj = { a: 1 };
    assert.strictEqual(getValue(obj, 'a'), 1);
  });

  it('should return default value if property does not exist', () => {
    const obj = {};
    assert.strictEqual(getValue(obj, 'foo', { default: 'bar' }), 'bar');
  });

  it('should handle nested properties with dot notation', () => {
    const obj = { foo: { bar: { baz: 'qux' } } };
    assert.strictEqual(getValue(obj, 'foo.bar.baz'), 'qux');
  });

  it('should handle array path', () => {
    const obj = { foo: { bar: 'baz' } };
    assert.strictEqual(getValue(obj, ['foo', 'bar']), 'baz');
  });

  it('should handle numeric path', () => {
    const obj = { '1': 'one' };
    assert.strictEqual(getValue(obj, 1), 'one');
  });

  it('should return default when accessing property on non-object', () => {
    assert.strictEqual(getValue(null, 'foo', { default: 123 }), 123);
    assert.strictEqual(getValue(undefined, 'foo', { default: 123 }), 123);
  });

  it('should return original value if path is not string/array', () => {
    const obj = { foo: 'bar' };
    assert.strictEqual(getValue(obj, {} as any), obj);
  });

  it('should use a custom split function', () => {
    const obj = { foo: { bar: 'baz' } };
    const options = {
      split: (path: string) => path.split('#')
    };
    assert.strictEqual(getValue(obj, 'foo#bar', options), 'baz');
  });

  it('should use a custom join function', () => {
    const obj = { 'foo#bar': 'baz' };
    const options = {
      join: (segs: string[]) => segs.join('#'),
      separator: '#'
    };
    assert.strictEqual(getValue(obj, 'foo#bar', options), 'baz');
  });

  it('should use custom isValid to filter properties', () => {
    const obj = { foo: 'bar', bar: 'baz' };
    const options = {
      isValid: (key: string) => key === 'foo'
    };
    assert.strictEqual(getValue(obj, 'foo', options), 'bar');
    assert.strictEqual(getValue(obj, 'bar', options), undefined);
  });

  it('should support path segments with escaped separator (\\)', () => {
    const obj = { 'foo.bar': { baz: 'buzz' } };
    assert.deepStrictEqual(getValue(obj, 'foo\\.bar.baz'), 'buzz');
  });


  it('should properly handle multi-segment join with joinChar', () => {
    const obj = { 'foo|bar|baz': 'abc' };
    const options = {
      separator: '|',
      joinChar: '|'
    };
    assert.strictEqual(getValue(obj, 'foo|bar|baz', options), 'abc');
  });

  it('should properly handle property that is a function', () => {
    const obj = { foo: () => 42 };
    assert.strictEqual(typeof getValue(obj, 'foo'), 'function');
    assert.strictEqual(getValue(obj, 'foo')(), 42);
  });

  it('should support options being a primitive and treat as default', () => {
    const obj = {};
    assert.strictEqual(getValue(obj, 'foo', 'DEFAULT'), 'DEFAULT');
  });

  it('should handle empty path string', () => {
    const obj = { '': 42 };
    assert.strictEqual(getValue(obj, '', {}), 42);
  });

  it('should return default when target is not an object or function', () => {
    assert.strictEqual(getValue(123 as any, 'a', { default: 'D' }), 'D');
    assert.strictEqual(getValue(null, 'a'), null);
  });
});