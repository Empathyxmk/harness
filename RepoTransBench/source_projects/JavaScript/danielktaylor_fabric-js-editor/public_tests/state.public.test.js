const StateModule = require('../src/js/app/state');

// PUBLIC TESTS: different data/values but same coverage and intent.

describe('StateModule (public tests)', () => {
  let state, currentVal, history;

  beforeEach(() => {
    history = [];
    currentVal = { a: 10 };
    state = StateModule(
      () => JSON.stringify(currentVal),
      (nv) => { currentVal = JSON.parse(nv); history.push({ ...currentVal }); }
    );
  });

  test('should save (pushState) new states (public)', () => {
    currentVal.a = 20;
    state.save();
    currentVal.a = 30;
    state.save();
    expect(history).toEqual([]);
    state.undo();
    expect(currentVal).toEqual({ a: 20 });
    state.redo();
    expect(currentVal).toEqual({ a: 30 });
  });

  test('should not save same state twice (public)', () => {
    currentVal.a = 15;
    state.save();
    const stackLen = state.getStack().length;
    state.save(); // no change, should not push
    expect(state.getStack().length).toBe(stackLen);
    state.undo(); // back to initial
    expect(currentVal).toEqual({ a: 10 });
  });

  test('undo at first state does nothing (public)', () => {
    state.undo();
    expect(history.length).toBe(0);
    expect(currentVal).toEqual({ a: 10 });
  });

  test('redo at last state does nothing (public)', () => {
    currentVal.a = 42;
    state.save();
    state.redo();
    expect(history.length).toBe(0);
    expect(currentVal).toEqual({ a: 42 });
  });

  test('undo/redo normal sequence (public)', () => {
    currentVal.a = 11;
    state.save();
    currentVal.a = 22;
    state.save();
    state.undo();
    expect(currentVal).toEqual({ a: 11 });
    state.undo();
    expect(currentVal).toEqual({ a: 10 });
    state.undo();
    expect(currentVal).toEqual({ a: 10 });
    state.redo();
    expect(currentVal).toEqual({ a: 11 });
    state.redo();
    expect(currentVal).toEqual({ a: 22 });
    state.redo();
    expect(currentVal).toEqual({ a: 22 });
  });

  test('should cap states to 100 (public)', () => {
    for (let i = 1; i <= 105; i++) {
      currentVal.a = i * 2;
      state.save();
    }
    expect(state.getStack().length).toBe(100);
    for (let i = 1; i < 100; i++) {
      state.undo();
    }
    expect(currentVal.a).toBe(12); // 6th inserted value, since initial is a=10, then a=2, 4, 6, 8, 10, 12...
  });

  test('should fork stack if set after undo (public)', () => {
    currentVal.a = 7;
    state.save();
    currentVal.a = 21;
    state.save();
    state.undo(); // now at a=7
    currentVal.a = 99;
    state.save();
    const stack = state.getStack();
    const idx = state.getIndex();
    expect(stack[idx]).toBe(JSON.stringify({ a: 99 }));
    expect(stack.length).toBe(3);
    state.redo();
    expect(currentVal.a).toBe(99);
  });

  test('throws if getState is missing (public)', () => {
    expect(() => StateModule(undefined, () => {})).toThrow();
  });

  test('throws if setState is missing (public)', () => {
    expect(() => StateModule(() => '{}', undefined)).toThrow();
  });

  test('getStack & getIndex reflect correct internals (public)', () => {
    expect(state.getStack()[0]).toBe(JSON.stringify({ a: 10 }));
    expect(state.getIndex()).toBe(0);
    currentVal.a = 1234;
    state.save();
    expect(state.getStack()[1]).toBe(JSON.stringify({ a: 1234 }));
    expect(state.getIndex()).toBe(1);
    state.undo();
    expect(state.getIndex()).toBe(0);
  });
});