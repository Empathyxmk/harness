const Store = require('../../src/Store');
const { expect } = require('chai');

describe('Store - Extra Tests for coverage', () => {
  it('should not resolve non-existent key and trigger debug', () => {
    const store = new Store('adapter', ['foo']);
    expect(store.resolve('notfound')).to.be.undefined;
  });

  it('should throw error if template validation fails during register', () => {
    const store = new Store('adapter', ['foo']);
    expect(() => store.register('invalid', { bar: 123 })).to.throw(/must contain/);
  });

  it('should support valid registration and resolution', () => {
    const store = new Store('adapter', ['foo']);
    store.register('valid', { foo: 'bar' });
    expect(store.resolve('valid')).to.deep.equal({ foo: 'bar' });
  });

  it('should return false if candidate does not match template', () => {
    const store = new Store('adapter', ['foo', 'bar']);
    expect(store.validate({ foo: 1 })).to.be.false;
  });

  it('should return true if candidate matches the template', () => {
    const store = new Store('adapter', ['foo', 'bar']);
    expect(store.validate({ foo: 1, bar: 2 })).to.be.true;
  });
});