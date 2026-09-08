const { diffStates } = require('../src/diff');

describe('diff (public)', () => {
  test('diffStates computes changes (public)', () => {
    const prev = { foo: 1, arr: [1, 2], obj: { x: 1 } };
    const next = { foo: 2, arr: [2, 3], obj: { x: 2, y: 3 }, extra: 7 };
    const diff = diffStates(prev, next);
    expect(diff).toEqual({
      foo: { from: 1, to: 2 },
      arr: { from: [1, 2], to: [2, 3] },
      obj: { from: { x: 1 }, to: { x: 2, y: 3 } },
      extra: { from: undefined, to: 7 }
    });
  });

  test('diffStates on identical values yields empty object (public)', () => {
    const obj = { test: [1, 2, 3], thing: { z: 77 }, padd: 'foo' };
    expect(diffStates(obj, obj)).toEqual({});
  });

  test('diffStates with nested and missing values (public)', () => {
    const prev = { foo: { bar: 1 }, arr: [1, 2, 3] };
    const next = { foo: { bar: 1, baz: 2 }, arr: [1, 2, 3, 4], newkey: 'x' };
    const diff = diffStates(prev, next);
    expect(diff.foo).toEqual({ from: { bar: 1 }, to: { bar: 1, baz: 2 } });
    expect(diff.arr).toEqual({ from: [1, 2, 3], to: [1, 2, 3, 4] });
    expect(diff.newkey).toEqual({ from: undefined, to: 'x' });
  });
});