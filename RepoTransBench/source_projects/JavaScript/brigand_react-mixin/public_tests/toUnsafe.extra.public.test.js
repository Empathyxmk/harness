const toUnsafe = require('../toUnsafe');

describe('toUnsafe (public)', () => {
  it('should copy mixin with only componentWillMount (different return data)', () => {
    const mixin = {
      componentWillMount: function() { return 99; }
    };
    const result = toUnsafe(mixin);
    expect(result.componentWillMount).toBeUndefined();
    expect(typeof result.UNSAFE_componentWillMount).toBe('function');
    expect(result.UNSAFE_componentWillMount()).toBe(99);
  });

  it('should copy mixin with only componentWillReceiveProps (different fn)', () => {
    const fn = jest.fn().mockReturnValue('public_test');
    const mixin = {
      componentWillReceiveProps: fn
    };
    const result = toUnsafe(mixin);
    expect(result.componentWillReceiveProps).toBeUndefined();
    expect(result.UNSAFE_componentWillReceiveProps).toBe(fn);
    expect(result.UNSAFE_componentWillReceiveProps()).toBe('public_test');
  });

  it('should copy mixin with only componentWillUpdate (different fn)', () => {
    const fn = jest.fn().mockReturnValue(789);
    const mixin = {
      componentWillUpdate: fn
    };
    const result = toUnsafe(mixin);
    expect(result.componentWillUpdate).toBeUndefined();
    expect(result.UNSAFE_componentWillUpdate).toBe(fn);
    expect(result.UNSAFE_componentWillUpdate()).toBe(789);
  });

  it('should not set unsafe keys if original keys missing (different keys)', () => {
    const mixin = { foo: 3, bar: 4 };
    const result = toUnsafe(mixin);
    expect(result.UNSAFE_componentWillMount).toBeUndefined();
    expect(result.UNSAFE_componentWillReceiveProps).toBeUndefined();
    expect(result.UNSAFE_componentWillUpdate).toBeUndefined();
  });

  it('should retain all other properties (different other prop value)', () => {
    const mixin = {
      componentWillMount: () => 5,
      anotherThing: 101
    };
    const result = toUnsafe(mixin);
    expect(result.anotherThing).toBe(101);
  });
});