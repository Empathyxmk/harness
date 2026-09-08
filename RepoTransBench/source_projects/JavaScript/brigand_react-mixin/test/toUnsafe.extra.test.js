const toUnsafe = require('../toUnsafe');

describe('toUnsafe', () => {
  it('should copy mixin with only componentWillMount', () => {
    const mixin = {
      componentWillMount: function() { return 42; }
    };
    const result = toUnsafe(mixin);
    expect(result.componentWillMount).toBeUndefined();
    expect(typeof result.UNSAFE_componentWillMount).toBe('function');
    expect(result.UNSAFE_componentWillMount()).toBe(42);
  });

  it('should copy mixin with only componentWillReceiveProps', () => {
    const fn = jest.fn();
    const mixin = {
      componentWillReceiveProps: fn
    };
    const result = toUnsafe(mixin);
    expect(result.componentWillReceiveProps).toBeUndefined();
    expect(result.UNSAFE_componentWillReceiveProps).toBe(fn);
  });

  it('should copy mixin with only componentWillUpdate', () => {
    const fn = jest.fn();
    const mixin = {
      componentWillUpdate: fn
    };
    const result = toUnsafe(mixin);
    expect(result.componentWillUpdate).toBeUndefined();
    expect(result.UNSAFE_componentWillUpdate).toBe(fn);
  });

  it('should not set unsafe keys if original keys missing', () => {
    const mixin = { a: 1, b: 2 };
    const result = toUnsafe(mixin);
    expect(result.UNSAFE_componentWillMount).toBeUndefined();
    expect(result.UNSAFE_componentWillReceiveProps).toBeUndefined();
    expect(result.UNSAFE_componentWillUpdate).toBeUndefined();
  });

  it('should retain all other properties', () => {
    const mixin = {
      componentWillMount: () => 2,
      somethingElse: 55
    };
    const result = toUnsafe(mixin);
    expect(result.somethingElse).toBe(55);
  });
});