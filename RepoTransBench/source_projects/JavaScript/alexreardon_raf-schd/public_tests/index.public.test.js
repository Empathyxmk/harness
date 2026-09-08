// @flow
import { replaceRaf } from 'raf-stub';
import rafSchedule from '../src/';

replaceRaf();

beforeEach(() => {
  // $FlowFixMe
  requestAnimationFrame.reset();
});

describe('behaviour - public', () => {
  it('should not execute a callback before a animation frame (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    fn();

    expect(myMock).toHaveBeenCalledTimes(0);
  });

  it('should execute a callback after an animation frame (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    fn('run!');
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(myMock).toHaveBeenCalledTimes(1);
  });

  it('should not execute multiple times if waiting for a frame - public', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    fn('a');
    fn('b');
    fn('c');
    fn('d');

    // $FlowFixMe
    requestAnimationFrame.step();
    expect(myMock).toHaveBeenCalledTimes(1);

    // should have no impact
    // $FlowFixMe
    requestAnimationFrame.step();
    // $FlowFixMe
    requestAnimationFrame.flush();
    expect(myMock).toHaveBeenCalledTimes(1);
  });

  it('should execute the callback with the latest value (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    fn('x');
    fn('y');
    fn('z');
    fn('final');
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(myMock).toHaveBeenCalledTimes(1);
    expect(myMock.mock.calls[0][0]).toBe('final');
  });

  it('should execute the callbacks with the latest value when there are multiple args (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    fn('one', 'two', 'three');
    fn(10, 20, 30);
    fn('foo', 99, { value: 'bar' });
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(myMock).toHaveBeenCalledTimes(1);
    expect(myMock.mock.calls[0]).toEqual(['foo', 99, { value: 'bar' }]);
  });

  it('should return the exact value that was passed to the callback (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);
    const obj = { greet: 'hi' };

    fn(obj);
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(myMock).toHaveBeenCalledTimes(1);
    expect(myMock.mock.calls[0][0]).toBe(obj);
  });

  it('should allow cancelling of a frame using .cancel (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    fn('cancel-me');
    fn.cancel();
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(myMock).toHaveBeenCalledTimes(0);
  });

  it('should permit future frames after cancelling a frame (public)', () => {
    const myMock = jest.fn();
    const fn = rafSchedule(myMock);

    // first frame is cancelled
    fn('do-cancel');
    fn.cancel();
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(myMock).toHaveBeenCalledTimes(0);

    // second frame is not cancelled
    fn('after-cancel');
    // $FlowFixMe
    requestAnimationFrame.step();
    expect(myMock).toHaveBeenCalledWith('after-cancel');
  });
});

describe('respecting original "this" context - public', () => {
  it('should respect new bindings (public)', () => {
    const mock = jest.fn();
    const Foo = function(a: number) {
      this.a = a;
    };
    Foo.prototype.callMock = function() {
      return mock(this.a);
    };
    const foo = new Foo(25);
    const schedule = rafSchedule(function() {
      foo.callMock();
    });

    schedule();
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(mock).toBeCalledWith(25);
  });

  it('should respect explicit bindings (public)', () => {
    const mock = jest.fn();
    const callMock = function() {
      mock(this.a);
    };
    const foo = {
      a: 99,
    };
    const bound = callMock.bind(foo);
    const schedule = rafSchedule(bound);

    schedule();
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(mock).toBeCalledWith(foo.a);
  });

  it('should respect implicit bindings (public)', () => {
    const mock = jest.fn();
    const foo = {
      a: -15,
      callMock: function() {
        mock(this.a);
      },
    };

    const schedule = rafSchedule(function() {
      foo.callMock();
    });

    schedule();
    // $FlowFixMe
    requestAnimationFrame.step();

    expect(mock).toBeCalledWith(foo.a);
  });

  it('should respect ignored bindings (public)', () => {
    const mock = jest.fn();
    const callMock = function() {
      // $FlowExpectedError - this should throw!
      mock(this.a);
    };
    const schedule = rafSchedule(function() {
      callMock.call(null);
    });

    schedule();

    // $FlowFixMe
    expect(() => requestAnimationFrame.step()).toThrow();
  });
});

describe('flow type - public', () => {
  it('should type the result function correctly (public)', () => {
    const fakeFn = (y: number): void => {};

    const schedule = rafSchedule(fakeFn);

    schedule(123);

    schedule.cancel();
  });
});