// Extra test cases for rafSchd edge/error branches
import rafSchd from '../src/';

// Pull in raf-stub to simulate step()
import { replaceRaf } from 'raf-stub';

replaceRaf();

beforeEach(() => {
  // @ts-ignore
  requestAnimationFrame.reset();
});

describe('rafSchd edge and error conditions', () => {
  it('should do nothing if cancel called with no frame scheduled', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled.cancel();
    expect(fn).not.toBeCalled();
  });

  it('should still work if passed undefined/no arguments', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled();
    // Simulate animation frame
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).toBeCalled();
    // Should be called with no args
    expect(fn.mock.calls[0].length).toBe(0);
  });

  it('should queue new value after cancel and re-invoke', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('value1');
    scheduled.cancel();
    // Schedule again after cancel
    scheduled('value2');
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).toHaveBeenCalledTimes(1);
    expect(fn).toHaveBeenCalledWith('value2');
  });

  it('should not call callback if raf is cancelled immediately in same tick', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('early cancel');
    scheduled.cancel(); // Cancel before frame
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).not.toBeCalled();
  });

  it('should pass multiple argument types (strings, numbers, objects)', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('a', 123, { k: 'v' });
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).toBeCalledWith('a', 123, { k: 'v' });
  });

  it('should allow cancel to be called multiple times safely', () => {
    const fn = jest.fn();
    const scheduled = rafSchd(fn);
    scheduled('one');
    scheduled.cancel();
    scheduled.cancel();
    // @ts-ignore
    requestAnimationFrame.step();
    expect(fn).not.toBeCalled();
  });
});