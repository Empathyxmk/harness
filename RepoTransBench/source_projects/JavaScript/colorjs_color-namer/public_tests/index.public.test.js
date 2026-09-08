const namer = require('../index');
const chroma = require('chroma-js');

describe('color-namer main function (public tests)', () => {
  it('should be a function', () => {
    expect(typeof namer).toBe('function');
  });

  it('should return an object containing named sorted arrays for a color (different color)', () => {
    const result = namer('#FFF');
    expect(typeof result).toBe('object');
    expect(Object.keys(result).length).toBeGreaterThan(0);
    Object.values(result).forEach(list =>
      expect(Array.isArray(list)).toBe(true)
    );
    // basic test for structure of first list
    expect(result.basic[0]).toHaveProperty('name');
    expect(result.basic[0]).toHaveProperty('hex');
    expect(result.basic[0]).toHaveProperty('distance');
  });

  it('should handle non-hex input (different color name)', () => {
    const result = namer('green');
    expect(typeof result).toBe('object');
    expect(Object.keys(result).length).toBeGreaterThan(0);
  });

  it('should handle pick option (with different picks)', () => {
    const result = namer('#FFF', {pick: ['x11', 'html']});
    expect(Object.keys(result)).toEqual(expect.arrayContaining(['x11', 'html']));
  });

  it('should handle omit option (exclude different list)', () => {
    const result = namer('#FFF', {omit: ['x11']});
    expect(result.x11).toBeUndefined();
    expect(result.basic).toBeDefined();
  });

  it('should allow both pick and omit with new lists, pick precedence', () => {
    const result = namer('#FFF', {pick: ['roygbiv', 'ntc'], omit: ['ntc']});
    expect(Object.keys(result)).toEqual(['roygbiv']);
  });

  it('should cache results for a new color/options pair', () => {
    const options = {pick: ['html']};
    const first = namer('#FFF', options);
    const second = namer('#FFF', options);
    expect(first).toStrictEqual(second);
  });

  it('should use distance: "deltaE" for distance calculation (with different color)', () => {
    const options = {distance: 'deltaE'};
    const result = namer('#FFF', options);
    expect(result).toBeDefined();
    expect(Array.isArray(result.basic)).toBe(true);
    expect(result.basic[0]).toHaveProperty('distance');
  });

  it('should export chroma correctly', () => {
    expect(namer.chroma).toBeDefined();
    expect(typeof namer.chroma).toBe('function');
    expect(namer.chroma('blue').hex()).toBe('#0000ff');
  });

  it('should export lists with a different list property', () => {
    expect(namer.lists).toBeDefined();
    expect(namer.lists).toHaveProperty('x11');
    expect(Array.isArray(namer.lists.x11)).toBe(true);
  });

  it('should throw for another unrecognized color', () => {
    expect(() => namer('blorple')).toThrow();
  });

  it('should not throw if color arg is an HSL chroma.js object', () => {
    const color = chroma.hsl(240, 1, 0.5); // different chroma object
    expect(() => namer(color)).not.toThrow();
  });
});