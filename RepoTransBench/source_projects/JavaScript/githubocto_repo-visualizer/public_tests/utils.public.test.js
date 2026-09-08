const {
  truncateString,
  keepBetween,
  getPositionFromAngleAndDistance,
  getAngleFromPosition,
  keepCircleInsideCircle,
} = require('../src/utils');

describe('truncateString (public)', () => {
  it('should truncate a different long string', () => {
    expect(truncateString('0123456789abcdef', 6)).toBe('012345...');
  });
  it('should not truncate another short string', () => {
    expect(truncateString('bcd', 4)).toBe('bcd');
  });
  it('should use default length and public string', () => {
    expect(truncateString('abcdefghijabcdefghijabcdefghijabc')).toMatch(/^\w{20}\.\.\.$/);
  });
  it('should handle empty string public', () => {
    expect(truncateString('', 4)).toBe('');
  });
});

describe('keepBetween (public)', () => {
  it('returns value within new range', () => {
    expect(keepBetween(2, 8, 5)).toBe(5);
  });
  it('clamps below new min', () => {
    expect(keepBetween(2, 8, -1)).toBe(2);
  });
  it('clamps above new max', () => {
    expect(keepBetween(2, 8, 42)).toBe(8);
  });
});

describe('getPositionFromAngleAndDistance (public)', () => {
  it('should return correct position for 180 deg', () => {
    expect(getPositionFromAngleAndDistance(180, 4)[0]).toBeCloseTo(-4);
    expect(getPositionFromAngleAndDistance(180, 4)[1]).toBeCloseTo(0);
  });
  it('should return correct position for 270 deg', () => {
    expect(getPositionFromAngleAndDistance(270, 7)[0]).toBeCloseTo(0, 5);
    expect(getPositionFromAngleAndDistance(270, 7)[1]).toBeCloseTo(-7, 5);
  });
});

describe('getAngleFromPosition (public)', () => {
  it('should return correct angle for (0,-1)', () => {
    expect(getAngleFromPosition(0, -1)).toBeCloseTo(270);
  });
  it('should return correct angle for (1,1)', () => {
    expect(getAngleFromPosition(1, 1)).toBeCloseTo(45);
  });
  it('should return correct angle for (-1,-1)', () => {
    expect(getAngleFromPosition(-1, -1)).toBeCloseTo(-135);
  });
});

describe('keepCircleInsideCircle (public)', () => {
  it('returns position unchanged if already inside (public)', () => {
    expect(keepCircleInsideCircle(7, [1,2], 1, [2, 3])).toEqual([2,3]);
  });
  it('repositions if clearly outside, public', () => {
    const v = keepCircleInsideCircle(6, [0,0], 1, [8, 0]);
    expect(v[0]).toBeLessThan(6);
  });
  it('pads more for negative angles/isParent public', () => {
    const res = keepCircleInsideCircle(6, [0,0], 1, [-2, -5], true);
    expect(Array.isArray(res)).toBeTruthy();
  });
});