// Public extra test cases for rafSchd edge/error branches - new input/output
import rafSchd from '../src/';

// Pull in raf-stub to simulate step/rAF
import { replaceRaf } from 'raf-stub';

replaceRaf();

beforeEach(() => {
  // @ts-ignore
  requestAnimationFrame.reset();
});

describe('rafSchd public edge and error conditions', () => {
  it('should do nothing if cancel called with no frame scheduled (public)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled.cancel();
    expect(fn).not.toBeCalled();
  });

  it('should still work if passed undefined/no arguments (public)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    // Call with no arguments again
    scheduled();
    // Simulate animation frame
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).toBeCalled();
    // Should be called with no args
    expect(fn.mock.calls[0].length).toBe(0);
  });

  it('should queue new value after cancel and re-invoke (public)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('foo1');
    scheduled.cancel();
    // Schedule again after cancel
    scheduled('foo2');
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).toHaveBeenCalledTimes(1);
    expect(fn).toHaveBeenCalledWith('foo2');
  });

  it('should not call callback if raf is cancelled immediately in same tick (public)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('baz');
    scheduled.cancel(); // Cancel before frame
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).not.toBeCalled();
  });

  it('should pass multiple argument types (booleans, arrays, objects) (public)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled(false, [1, 2, 3], { test: true });
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).toBeCalledWith(false, [1, 2, 3], { test: true });
  });

  it('should allow cancel to be called multiple times safely (public)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('repeat');
    scheduled.cancel();
    scheduled.cancel();
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).not.toBeCalled();
  });
});