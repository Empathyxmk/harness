const reactMixin = require('../index');
const smartMixin = require('smart-mixin');
const objectAssign = require('object-assign');

describe('index.js (react-mixin main) [public]', () => {
  it('should throw if statics with same key are present in both class and mixin (different key)', () => {
    function MyOtherClass() {}
    MyOtherClass.bar = 7;
    const mixin = {
      statics: { bar: 8 }
    };
    expect(() => reactMixin.onClass(MyOtherClass, mixin)).toThrow(TypeError);
  });

  it('should assign static props from mixin if not present on class (different key/value)', () => {
    function MyOtherClass() {}
    const mixin = { statics: { extra: 99 } };
    reactMixin.onClass(MyOtherClass, mixin);
    expect(MyOtherClass.extra).toBe(99);
  });

  it('merges propTypes and defaultProps using MANY_MERGED_LOOSE (different spy)', () => {
    function MyOtherClass() {}
    const spy = jest.fn(() => ({ newProp: 'abc' }));
    const mixinObj = {
      propTypes: { newProp: () => true },
      defaultProps: { newProp: 'abc' },
      getDefaultProps: spy
    };
    reactMixin.onClass(MyOtherClass, mixinObj);
    expect(typeof MyOtherClass.defaultProps).toBe('object');
    expect(spy).toHaveBeenCalled();
    expect(MyOtherClass.defaultProps).toHaveProperty('newProp', 'abc');
  });

  it('should handle mixin.mixins (different keys)', () => {
    function OtherClass() {}
    const subMixin = { contextTypes: { c: () => true } };
    const topMixin = { 
      mixins: [subMixin], 
      contextTypes: { d: () => true } 
    };
    reactMixin.onClass(OtherClass, topMixin);
    expect(OtherClass.contextTypes).toHaveProperty('c');
    expect(OtherClass.contextTypes).toHaveProperty('d');
  });

  it('setInitialState should add method to UNSAFE_componentWillMount if not already present (different state key)', () => {
    const reactMixinMod = require('../index');
    const testMixin = { 
      getInitialState: function() { return { x: 50 }; }
    };
    function PublicTestClass() { this.state = {}; }
    PublicTestClass.prototype = {};
    reactMixinMod.onClass(PublicTestClass, testMixin);
    const testInstance = new PublicTestClass();
    expect(typeof PublicTestClass.prototype.UNSAFE_componentWillMount).toBe('function');
    PublicTestClass.prototype.UNSAFE_componentWillMount.call(testInstance);
    expect(testInstance.state.x).toBe(50);
  });

  it('setInitialState should wrap original UNSAFE_componentWillMount if present (different key and check)', () => {
    let called = false;
    const testMixin = { 
      getInitialState: function() { return { z: 77 }; },
      UNSAFE_componentWillMount: function() { called = true; }
    };
    function PublicClass() { this.state = {}; }
    PublicClass.prototype = {};
    reactMixin.onClass(PublicClass, testMixin);
    const instance = new PublicClass();
    PublicClass.prototype.UNSAFE_componentWillMount.call(instance);
    expect(instance.state.z).toBe(77);
    expect(called).toBeTruthy();
  });
});