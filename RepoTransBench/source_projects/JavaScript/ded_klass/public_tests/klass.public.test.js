const klass = require('../klass.js');

describe('klass (public tests)', () => {
  it('should create a class with a constructor function (different data)', () => {
    const Dog = klass(function(name) {
      this.name = name;
    });
    const d = new Dog('Rex');
    expect(d.name).toBe('Rex');
    expect(d).toBeInstanceOf(Dog);
  });

  it('should create a class with a methods object (no explicit constructor, different keys)', () => {
    const Animal = klass({
      species: 'unknown',
      getSpecies: function() { return this.species; }
    });
    const a = new Animal();
    expect(a.getSpecies()).toBe('unknown');
  });

  it('should extend with methods() and assign them to the prototype (changed method names)', () => {
    const Vehicle = klass()
      .methods({
        setModel: function(model) {
          this.vmod = model;
        },
        getModel: function() {
          return this.vmod;
        }
      });
    const v = new Vehicle();
    v.setModel('ZX-1');
    expect(v.getModel()).toBe('ZX-1');
  });

  it('should allow subclassing with extend and instance using methods from parent (different sub/methods)', () => {
    const Parent = klass({ foo: () => 'foo' });
    const Child = Parent.extend({ bar: () => 'bar' });
    const c = new Child();
    expect(c.foo()).toBe('foo');
    expect(c.bar()).toBe('bar');
  });

  it('should wrap method and allow supr call (different function body)', () => {
    const Base = klass({
      greet: function() { return 'Hello'; }
    });
    const Sub = Base.extend({
      greet: function() { return this.supr() + ', world!'; }
    });
    const s = new Sub();
    expect(s.greet()).toBe('Hello, world!');
  });

  it('should handle statics for adding methods (different statics names)', () => {
    const Statics = klass().statics({
      getType: function() { return 'STATIC'; }
    });
    expect(Statics.getType()).toBe('STATIC');
  });

  it('should allow string notation for statics (different strings)', () => {
    const StaticStr = klass().statics('sayHi', function() { return 'hi'; });
    expect(StaticStr.sayHi()).toBe('hi');
  });

  it('should call initialize if present, else fallback to constructor (different logic)', () => {
    const X = klass({
      initialize: function(n) { this.value = n * 9; }
    });
    const obj = new X(2);
    expect(obj.value).toBe(18);

    const Y = klass(function(m) { this.m = m + 5; });
    const y = new Y(3);
    expect(y.m).toBe(8);
  });

  it('should not call initialize if not present (check value)', () => {
    const Z = klass({});
    const z = new Z();
    expect(z.hasOwnProperty('value')).toBe(false);
  });

  it('should allow chaining of methods() (use different method names)', () => {
    const Chain = klass().methods({
      setX: function(x) { this.xv = x; }
    }).methods({
      getX: function() { return this.xv; }
    });
    const c = new Chain();
    c.setX(99);
    expect(c.getX()).toBe(99);
  });

  it('handles edge case where method name clashes with Object.prototype (public version)', () => {
    const Q = klass({ hasOwnProperty: () => 'yes' });
    const q = new Q();
    expect(q.hasOwnProperty()).toBe('yes');
  });

  it('should not call supr if not needed (checks returned value)', () => {
    const NoSupr = klass({ hello: () => 'ok' });
    const YetAnother = NoSupr.extend({ hello: () => 'fine' });
    expect(new YetAnother().hello()).toBe('fine');
  });

  it('should properly set constructor property (different naming)', () => {
    const Demo = klass();
    expect(Demo.prototype.constructor).toBe(Demo);
  });

  it('should ignore non-object and non-(string+function) arguments in .methods (arrays, numbers, etc)', () => {
    const Ign = klass().methods([1,2,3], 42, null, undefined, 'abc', true);
    expect(typeof Ign.prototype).toBe('object');
  });

  it('should ignore non-object and non-(string+function) arguments in .statics', () => {
    // Instead of checking typeof S.statics, which may always be 'function' if klass sets it,
    // let's check that adding garbage as statics does NOT add them as static props:
    const S = klass().statics([42,43], 'zzz', 2, null, undefined);
    // Should not copy static properties for non-object/non-(string/function) arguments.
    // We'll test with a valid static added, then add garbage:
    const T = klass().statics('a', () => 42);
    T.statics([1,2], false, null, undefined);
    expect(typeof T.a).toBe('function');
    expect(T.hasOwnProperty('b')).toBe(false);
    expect(T.hasOwnProperty('c')).toBe(false);
  });

  it('should skip supr wrapping if parent method is not present', () => {
    const Empty = klass();
    const Ext = Empty.extend({ only: () => 234 });
    expect(new Ext().only()).toBe(234);
  });
});