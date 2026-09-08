const equal = require('../react');

describe('fast-deep-equal - react.js (public)', () => {
  it('should ignore _owner on React elements (public)', () => {
    const REACT_ELEMENT = Symbol.for('react.element');
    const reactElementA = {
      $$typeof: REACT_ELEMENT,
      type: 'span',
      key: null,
      ref: null,
      props: { children: 'hello world' },
      _owner: { alt: 'something' }
    };
    const reactElementB = {
      $$typeof: REACT_ELEMENT,
      type: 'span',
      key: null,
      ref: null,
      props: { children: 'hello world' },
      _owner: { alt: 'another' }
    };
    expect(equal(reactElementA, reactElementB)).toBe(true);
  });
  it('should fall back to normal behavior for non-React (public)', () => {
    expect(equal({x:2}, {x:2})).toBe(true);
    expect(equal({x:2}, {x:3})).toBe(false);
  });
  it('should properly handle deeply unequal React (public)', () => {
    const REACT_ELEMENT = Symbol.for('react.element');
    const eltA = { $$typeof: REACT_ELEMENT, first: { second: [4,5,6] }, _owner:{}, third: 'abc' };
    const eltB = { $$typeof: REACT_ELEMENT, first: { second: [4,5,7] }, _owner:{}, third: 'abc' };
    expect(equal(eltA, eltB)).toBe(false);
  });
});