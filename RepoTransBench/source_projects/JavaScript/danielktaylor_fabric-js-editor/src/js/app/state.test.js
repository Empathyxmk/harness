const StateModule = require('./state');

describe('StateModule', () => {
  let state, currentVal, history;

  beforeEach(() => {
    history = [];
    currentVal = { v: 0 };
    state = StateModule(
      () => JSON.stringify(currentVal),
      (nv) => { currentVal = JSON.parse(nv); history.push({ ...currentVal }); }
    );
  });

  test('should save (pushState) new states', () => {
    currentVal.v = 1;
    state.save();
    currentVal.v = 2;
    state.save();
    expect(history).toEqual([]);
    state.undo();
    expect(currentVal).toEqual({ v: 1 });
    state.redo();
    expect(currentVal).toEqual({ v: 2 });
  });

  test('should not save same state twice (does not push duplicate)', () => {
    currentVal.v = 1;
    state.save();
    const stackLen = state.getStack().length;
    state.save(); // no change, should not push
    expect(state.getStack().length).toBe(stackLen); // verify no push
    state.undo(); // undo to zero state
    expect(currentVal).toEqual({ v: 0 });
  });

  test('undo at first state does nothing', () => {
    // should do nothing if already at 0
    state.undo();
    expect(history.length).toBe(0);
    expect(currentVal).toEqual({ v: 0 });
  });

  test('redo at last state does nothing', () => {
    currentVal.v = 1;
    state.save();
    state.redo();
    expect(history.length).toBe(0);
    expect(currentVal).toEqual({ v: 1 });
  });

  test('undo/redo normal sequence', () => {
    currentVal.v = 1;
    state.save();
    currentVal.v = 2;
    state.save();
    state.undo();
    expect(currentVal).toEqual({ v: 1 });
    state.undo();
    expect(currentVal).toEqual({ v: 0 });
    state.undo(); // still at 0, does nothing
    expect(currentVal).toEqual({ v: 0 });
    state.redo();
    expect(currentVal).toEqual({ v: 1 });
    state.redo();
    expect(currentVal).toEqual({ v: 2 });
    state.redo(); // no effect
    expect(currentVal).toEqual({ v: 2 });
  });

  test('should cap states to 100', () => {
    for (let i = 1; i <= 101; i++) {
      currentVal.v = i;
      state.save();
    }
    expect(state.getStack().length).toBe(100);
    // Go to the oldest state
    for (let i = 1; i < 100; i++) {
      state.undo();
    }
    expect(currentVal.v).toBe(2);
  });

  test('should fork stack if set after undo', () => {
    currentVal.v = 1;
    state.save();
    currentVal.v = 2;
    state.save();
    state.undo(); // now at v=1
    currentVal.v = 7;
    state.save();
    const stack = state.getStack();
    const idx = state.getIndex();
    expect(stack[idx]).toBe(JSON.stringify({ v: 7 }));
    expect(stack.length).toBe(3); // forked
    state.redo(); // no effect, at end
    expect(currentVal.v).toBe(7);
  });

  // Extra: test constructor error throwing
  test('throws if getState is missing', () => {
    expect(() => StateModule(undefined, () => {})).toThrow();
  });
  test('throws if setState is missing', () => {
    expect(() => StateModule(() => '{}', undefined)).toThrow();
  });

  // Internal API coverage for testing
  test('getStack & getIndex reflect correct internals', () => {
    expect(state.getStack()[0]).toBe(JSON.stringify({ v: 0 }));
    expect(state.getIndex()).toBe(0);
    currentVal.v = 47;
    state.save();
    expect(state.getStack()[1]).toBe(JSON.stringify({ v: 47 }));
    expect(state.getIndex()).toBe(1);
    state.undo();
    expect(state.getIndex()).toBe(0);
  });
});