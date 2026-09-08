const reactMixin = require('../index');
const smartMixin = require('smart-mixin');
const objectAssign = require('object-assign');

describe('index.js (react-mixin main)', () => {
  it('should throw if statics with same key are present in both class and mixin', () => {
    function MyClass() {}
    MyClass.foo = 1;
    const mixin = {
      statics: { foo: 2 }
    };
    expect(() => reactMixin.onClass(MyClass, mixin)).toThrow(TypeError);
  });

  it('should assign static props from mixin if not present on class', () => {
    function MyClass() {}
    const mixin = { statics: { stuff: 42 } };
    reactMixin.onClass(MyClass, mixin);
    expect(MyClass.stuff).toBe(42);
  });

  it('merges propTypes and defaultProps using MANY_MERGED_LOOSE', () => {
    function MyClass() {}
    const spy = jest.fn(() => ({}));
    const mixinObj = {
      propTypes: {},
      defaultProps: {},
      getDefaultProps: spy
    };
    reactMixin.onClass(MyClass, mixinObj);
    expect(typeof MyClass.defaultProps).toBe('object');
    expect(spy).toHaveBeenCalled();
  });

  it('should handle mixin.mixins', () => {
    function MyClass() {}
    const subMixin = { contextTypes: { a: () => true } };
    const topMixin = { 
      mixins: [subMixin], 
      contextTypes: { b: () => true } 
    };
    reactMixin.onClass(MyClass, topMixin);
    expect(MyClass.contextTypes).toHaveProperty('a');
    expect(MyClass.contextTypes).toHaveProperty('b');
  });

  it('setInitialState should add method to UNSAFE_componentWillMount if not already present', () => {
    const reactMixinMod = require('../index');
    const testMixin = { 
      getInitialState: function() { return { a: 1 }; }
    };
    let didCall = false;
    function TestClass() { this.state = {}; }
    TestClass.prototype = {};
    reactMixinMod.onClass(TestClass, testMixin);
    const testInstance = new TestClass();
    expect(typeof TestClass.prototype.UNSAFE_componentWillMount).toBe('function');
    TestClass.prototype.UNSAFE_componentWillMount.call(testInstance);
    expect(testInstance.state.a).toBe(1);
  });

  it('setInitialState should wrap original UNSAFE_componentWillMount if present', () => {
    let didCall = false;
    const testMixin = { 
      getInitialState: function() { return { b: 2 }; },
      UNSAFE_componentWillMount: function() { didCall = true; }
    };
    function TestClass() { this.state = {}; }
    TestClass.prototype = {};
    reactMixin.onClass(TestClass, testMixin);
    const testInstance = new TestClass();
    TestClass.prototype.UNSAFE_componentWillMount.call(testInstance);
    expect(testInstance.state.b).toBe(2);
    expect(didCall).toBeTruthy();
  });
});