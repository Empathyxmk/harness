const status = require('../index.js');

describe('statuses main export', () => {
  test('exports a function', () => {
    expect(typeof status).toBe('function');
  });

  test('status(code: number) returns status message', () => {
    expect(status(200)).toBe('OK');
    expect(status(404)).toBe('Not Found');
    expect(status(500)).toBe('Internal Server Error');
  });

  test('status(code: string number) returns status message', () => {
    expect(status('200')).toBe('OK');
    expect(status('404')).toBe('Not Found');
  });

  test('status(code: string message) returns status code', () => {
    expect(status('not found')).toBe(404);
    expect(status('OK')).toBe(200);
    expect(status('Internal Server Error')).toBe(500);
  });

  test('status throws on unknown string message', () => {
    expect(() => status('wut')).toThrow(/invalid status message/i);
    expect(() => status('Nonexistent Status')).toThrow();
  });

  test('status throws on unknown code (number)', () => {
    expect(() => status(999)).toThrow(/invalid status code/i);
    expect(() => status('999')).toThrow();
  });

  test('status throws on invalid type', () => {
    expect(() => status([])).toThrow(/number or string/);
    expect(() => status({})).toThrow(/number or string/);
    expect(() => status(null)).toThrow(/number or string/);
    expect(() => status(undefined)).toThrow(/number or string/);
    expect(() => status(true)).toThrow(/number or string/);
  });

  test('status.codes is an array of numbers', () => {
    expect(Array.isArray(status.codes)).toBe(true);
    expect(status.codes).toContain(200);
    expect(status.codes).toContain(404);
    expect(status.codes).toContain(500);
    // Spot-check nonstandard code presence
    expect(status.codes.some(c => typeof c === 'number')).toBe(true);
  });

  test('status.message is an object with code keys', () => {
    expect(typeof status.message).toBe('object');
    expect(status.message['200']).toBe('OK');
    expect(status.message['404']).toBe('Not Found');
  });

  test('status.code is lower-cased message map to code', () => {
    expect(typeof status.code).toBe('object');
    expect(status.code['ok']).toBe(200);
    expect(status.code['not found']).toBe(404);
    expect(status.code['internal server error']).toBe(500);
  });

  test('status.redirect contains specific codes', () => {
    expect(status.redirect[301]).toBe(true);
    expect(status.redirect[302]).toBe(true);
    expect(status.redirect[308]).toBe(true);
    expect(status.redirect[200]).toBeFalsy();
  });

  test('status.empty contains specific codes', () => {
    expect(status.empty[204]).toBe(true);
    expect(status.empty[205]).toBe(true);
    expect(status.empty[304]).toBe(true);
    expect(status.empty[404]).toBeFalsy();
  });

  test('status.retry contains specific codes', () => {
    expect(status.retry[502]).toBe(true);
    expect(status.retry[503]).toBe(true);
    expect(status.retry[504]).toBe(true);
    expect(status.retry[501]).toBeFalsy();
  });

  // Regression: code is case-insensitive (should be lowercased)
  test('status is case-insensitive for string messages', () => {
    expect(status('iNtErNaL sErVeR eRrOr')).toBe(500);
    expect(status('nOt fOuNd')).toBe(404);
  });
});