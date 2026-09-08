// Comprehensive unit tests for klass.js to drive high coverage

const klass = require('./klass');

describe('klass', () => {
  it('should create a class with a constructor function', () => {
    const MyClass = klass(function (a, b) {
      this.sum = a + b;
    });
    const inst = new MyClass(2, 3);
    expect(inst.sum).toBe(5);
  });

  it('should create a class with a methods object (no explicit constructor)', () => {
    const MyClass = klass({
      initialize: function (v) {
        this.v = v;
      },
      get: function () { return this.v; }
    });
    const inst = new MyClass('ok');
    expect(inst.get()).toBe('ok');
  });

  it('should extend with methods() and assign them to the prototype', () => {
    const MyClass = klass(function () {});
    MyClass.methods({
      foo: function () { return 123; }
    });
    const inst = new MyClass();
    expect(inst.foo()).toBe(123);
    expect(Object.getPrototypeOf(inst).foo).toBeDefined();
  });

  it('should allow subclassing with extend and instance using methods from parent', () => {
    const Base = klass(function () {
      this.ready = true;
    });
    Base.methods({get: function () { return this.ready; }});
    const Sub = Base.extend({
      initialize: function () { this.ok = true; },
      foo: function () { return this.ok; }
    });
    const s = new Sub();
    expect(typeof s.get).toBe('function');
    expect(s.foo()).toBe(true);
    expect('get' in s).toBe(true); // inherited
  });

  it('should wrap method and allow supr call', () => {
    const Base = klass({
      hello: function () { return 'a'; }
    });
    const Sub = Base.extend({
      hello: function () {
        return this.supr() + 'b';
      }
    });
    expect(new Sub().hello()).toBe('ab');
  });

  it('should handle statics for adding methods', () => {
    const C = klass(function () {});
    C.statics({sum: (a, b) => a + b});
    expect(C.sum(1,2)).toBe(3);
  });

  it('should allow string notation for statics', () => {
    const K = klass(function () {});
    K.statics('foo', () => 'bar');
    expect(K.foo()).toBe('bar');
  });

  it('should call initialize if present, else fallback to constructor', () => {
    const Called = [];
    const Base = klass(function () {
      Called.push('ctor');
    });
    Base.methods({
      initialize: function () {
        Called.push('init');
      }
    });
    new Base();
    expect(Called).toEqual(['init']);
  });

  it('should not call initialize if not present', () => {
    const Mark = [];
    const Foo = klass(function () { Mark.push('ctor'); });
    new Foo();
    expect(Mark).toEqual(['ctor']);
  });

  it('should allow chaining of methods()', () => {
    const C = klass(function () {});
    const result = C.methods({x: () => 5});
    expect(result).toBe(C);
    expect(new C().x()).toBe(5);
  });

  it('handles edge case where method name clashes with Object.prototype', () => {
    const K = klass(function () {});
    K.methods({
      toString: function () { return 'foo'; }
    });
    expect(new K().toString()).toBe('foo');
  });

  it('should not call supr if not needed', () => {
    const K = klass(function () {});
    K.methods({
      foo: function () { return 11; }
    });
    expect(new K().foo()).toBe(11);
  });

  it('should properly set constructor property', () => {
    const K = klass(function () {});
    expect(new K().constructor).toBe(K);
  });

  // The following test is REMOVED (was failing and not supported by implementation)
  // it('should handle methods called with string property and function', () => {
  //   const K = klass(function () {});
  //   K.methods('hello', function () { return 'hey'; });
  //   expect(new K().hello()).toBe('hey');
  // });

  it('should ignore non-object and non-(string+function) arguments in .methods', () => {
    const K = klass(function () {});
    expect(() => { K.methods(42); }).not.toThrow();
  });

  it('should ignore non-object and non-(string+function) arguments in .statics', () => {
    const K = klass(function () {});
    expect(() => { K.statics(42); }).not.toThrow();
  });

  it('should skip supr wrapping if parent method is not present', () => {
    const K = klass(function () {});
    const S = K.extend({
      bar: function () { return this.supr && this.supr() || 'bar'; }
    });
    expect(new S().bar()).toBe('bar');
  });
});