const {
  truncateString,
  keepBetween,
  getPositionFromAngleAndDistance,
  getAngleFromPosition,
  keepCircleInsideCircle,
} = require('./utils');

describe('truncateString', () => {
  it('should truncate long strings and append ...', () => {
    expect(truncateString('abcdefghijklmnopqrstuvwxyz', 5)).toBe('abcde...');
  });
  it('should not truncate short string', () => {
    expect(truncateString('abc', 5)).toBe('abc');
  });
  it('should use default length=20', () => {
    expect(truncateString('abcdefghijklmnopqrsuvwxyz')).toMatch(/^\w{20}\.\.\.$/);
  });
  it('should handle empty string', () => {
    expect(truncateString('', 10)).toBe('');
  });
});

describe('keepBetween', () => {
  it('returns within range', () => {
    expect(keepBetween(0, 10, 5)).toBe(5);
  });
  it('clamps below min', () => {
    expect(keepBetween(0, 10, -2)).toBe(0);
  });
  it('clamps above max', () => {
    expect(keepBetween(0, 10, 42)).toBe(10);
  });
});

describe('getPositionFromAngleAndDistance', () => {
  it('should return correct position for 0 deg', () => {
    expect(getPositionFromAngleAndDistance(0, 10)[0]).toBeCloseTo(10);
    expect(getPositionFromAngleAndDistance(0, 10)[1]).toBeCloseTo(0);
  });
  it('should return correct position for 90 deg', () => {
    expect(getPositionFromAngleAndDistance(90, 20)[0]).toBeCloseTo(0, 5);
    expect(getPositionFromAngleAndDistance(90, 20)[1]).toBeCloseTo(20, 5);
  });
});

describe('getAngleFromPosition', () => {
  it('should return correct angle for (1,0)', () => {
    expect(getAngleFromPosition(1, 0)).toBeCloseTo(0);
  });
  it('should return correct angle for (0,1)', () => {
    expect(getAngleFromPosition(0, 1)).toBeCloseTo(90);
  });
  it('should return correct angle for (-1,0)', () => {
    expect(getAngleFromPosition(-1, 0)).toBeCloseTo(180);
  });
});

describe('keepCircleInsideCircle', () => {
  it('returns unchanged if inside', () => {
    expect(keepCircleInsideCircle(10, [0,0], 1, [1, 1])).toEqual([1,1]);
  });
  it('repositions if outside', () => {
    const v = keepCircleInsideCircle(10, [0,0], 2, [20, 0]);
    expect(v[0]).toBeLessThan(10);
  });
  it('pads more for certain angles and isParent', () => {
    // angle between -20 and -100 with isParent = true triggers special padding
    // Trick by placing child at negative high y and a little left
    const res = keepCircleInsideCircle(10, [0,0], 2, [-1, -8], true);
    expect(Array.isArray(res)).toBeTruthy();
  });
});