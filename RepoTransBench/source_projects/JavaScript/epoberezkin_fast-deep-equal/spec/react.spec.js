const equal = require('../react');

describe('fast-deep-equal - react.js', () => {
  it('should ignore _owner on React elements', () => {
    // Use the same Symbol for $$typeof on both objects to check equality
    const REACT_ELEMENT = Symbol.for('react.element');
    const reactElementA = {
      $$typeof: REACT_ELEMENT,
      type: 'div',
      key: null,
      ref: null,
      props: { children: 'hi' },
      _owner: { some: 'circular' }
    };
    const reactElementB = {
      $$typeof: REACT_ELEMENT,
      type: 'div',
      key: null,
      ref: null,
      props: { children: 'hi' },
      _owner: { some: 'other' }
    };
    expect(equal(reactElementA, reactElementB)).toBe(true);
  });
  it('should fall back to normal behavior for non-React', () => {
    expect(equal({a:1}, {a:1})).toBe(true);
    expect(equal({a:1}, {a:2})).toBe(false);
  });
  it('should properly handle deeply unequal React', () => {
    // Use the same Symbol for $$typeof
    const REACT_ELEMENT = Symbol.for('react.element');
    const eltA = { $$typeof: REACT_ELEMENT, foo: { bar: [1,2,3] }, _owner:{}, baz: 5 };
    const eltB = { $$typeof: REACT_ELEMENT, foo: { bar: [1,2,4] }, _owner:{}, baz: 5 };
    expect(equal(eltA, eltB)).toBe(false);
  });
});