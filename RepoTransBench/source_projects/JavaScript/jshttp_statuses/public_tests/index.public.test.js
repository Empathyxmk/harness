const status = require('../index.js');

describe('statuses main export (PUBLIC)', () => {
  test('exports a function', () => {
    expect(typeof status).toBe('function');
  });

  test('status(code: number) returns status message (different data)', () => {
    expect(status(201)).toBe('Created');
    expect(status(403)).toBe('Forbidden');
    expect(status(418)).toBe("I'm a Teapot");
  });

  test('status(code: string number) returns status message (different data)', () => {
    expect(status('201')).toBe('Created');
    expect(status('418')).toBe("I'm a Teapot");
  });

  test('status(code: string message) returns status code (different data)', () => {
    expect(status('created')).toBe(201);
    expect(status('FORBIDDEN')).toBe(403);
    expect(status("I'm a Teapot")).toBe(418);
  });

  test('status throws on unknown string message (different data)', () => {
    expect(() => status('foo')).toThrow(/invalid status message/i);
    expect(() => status('Definitely Not A Status')).toThrow();
  });

  test('status throws on unknown code (number) (different data)', () => {
    expect(() => status(777)).toThrow(/invalid status code/i);
    expect(() => status('777')).toThrow();
  });

  test('status throws on invalid type (same types, different structure)', () => {
    expect(() => status([123])).toThrow(/number or string/);
    expect(() => status({foo: 'bar'})).toThrow(/number or string/);
    expect(() => status(undefined)).toThrow(/number or string/);
    expect(() => status(false)).toThrow(/number or string/);
    expect(() => status(null)).toThrow(/number or string/);
  });

  test('status.codes is an array of numbers (different data)', () => {
    expect(Array.isArray(status.codes)).toBe(true);
    expect(status.codes).toContain(201);
    expect(status.codes).toContain(403);
    expect(status.codes).toContain(418);
    // Spot-check nonstandard code presence
    expect(status.codes.some(c => c > 208)).toBe(true); // e.g., 418, 422, etc.
  });

  test('status.message is an object with code keys (different data)', () => {
    expect(typeof status.message).toBe('object');
    expect(status.message['201']).toBe('Created');
    expect(status.message['403']).toBe('Forbidden');
  });

  test('status.code is lower-cased message map to code (different data)', () => {
    expect(typeof status.code).toBe('object');
    expect(status.code['created']).toBe(201);
    expect(status.code['forbidden']).toBe(403);
    expect(status.code["i'm a teapot"]).toBe(418);
  });

  test('status.redirect contains specific codes (different data)', () => {
    expect(status.redirect[303]).toBe(true);
    expect(status.redirect[305]).toBe(true);
    expect(status.redirect[307]).toBe(true);
    expect(status.redirect[403]).toBeFalsy();
  });

  test('status.empty contains specific codes (different data)', () => {
    expect(status.empty[204]).toBe(true); // keep 204 for truthy check
    expect(status.empty[205]).toBe(true); // keep 205 for truthy check
    expect(status.empty[304]).toBe(true);
    expect(status.empty[403]).toBeFalsy();
  });

  test('status.retry contains specific codes (different data)', () => {
    expect(status.retry[503]).toBe(true);
    expect(status.retry[504]).toBe(true);
    expect(status.retry[502]).toBe(true);
    expect(status.retry[400]).toBeFalsy();
  });

  // Regression: code is case-insensitive (should be lowercased, different messages)
  test('status is case-insensitive for string messages (different data)', () => {
    expect(status('cReAtEd')).toBe(201);
    expect(status('FoRbIdDeN')).toBe(403);
  });
});