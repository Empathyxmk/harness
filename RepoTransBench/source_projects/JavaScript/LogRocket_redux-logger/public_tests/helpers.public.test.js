const { repeat, pad, formatTime, timer } = require('../src/helpers');

describe('helpers (public)', () => {
  test('repeat() repeats strings as expected (public)', () => {
    expect(repeat('b', 4)).toEqual('bbbb');
    expect(repeat('=', 2)).toEqual('==');
    expect(repeat('y', 0)).toEqual('');
  });

  test('pad() pads numbers as expected (public)', () => {
    expect(pad(3, 4)).toEqual('0003');
    expect(pad(77, 3)).toEqual('077');
    expect(pad(120, 3)).toEqual('120');
  });

  test('formatTime() returns formatted time string (public)', () => {
    const date = new Date(2022, 11, 25, 23, 59, 59, 99); // 23:59:59.099
    expect(formatTime(date)).toBe('23:59:59.099');
  });

  test('timer uses performance or Date (public)', () => {
    expect(typeof timer).toBe('object');
    expect(typeof timer.now).toBe('function');
  });
});