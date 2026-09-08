const { repeat, pad, formatTime, timer } = require('../src/helpers');

describe('helpers', () => {
  test('repeat() repeats strings as expected', () => {
    expect(repeat('a', 3)).toEqual('aaa');
    expect(repeat('-', 0)).toEqual('');
    expect(repeat('x', 1)).toEqual('x');
  });

  test('pad() pads numbers as expected', () => {
    expect(pad(5, 2)).toEqual('05');
    expect(pad(15, 2)).toEqual('15');
    expect(pad(7, 3)).toEqual('007');
  });

  test('formatTime() returns formatted time string', () => {
    const date = new Date(2000, 0, 1, 9, 5, 2, 8); // 09:05:02.008
    expect(formatTime(date)).toBe('09:05:02.008');
  });

  test('timer uses performance or Date', () => {
    expect(typeof timer).toBe('object');
    expect(typeof timer.now).toBe('function');
  });
});