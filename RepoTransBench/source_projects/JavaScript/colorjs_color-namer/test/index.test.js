const namer = require('../index');
const chroma = require('chroma-js');

describe('color-namer main function', () => {
  it('should be a function', () => {
    expect(typeof namer).toBe('function');
  });

  it('should return an object containing named sorted arrays for a color', () => {
    const result = namer('#000');
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

  it('should handle non-hex input', () => {
    const result = namer('blue');
    expect(typeof result).toBe('object');
    expect(Object.keys(result).length).toBeGreaterThan(0);
  });

  it('should handle pick option (allow only certain lists)', () => {
    const result = namer('#000', {pick: ['pantone', 'basic']});
    expect(Object.keys(result)).toEqual(expect.arrayContaining(['pantone', 'basic']));
  });

  it('should handle omit option (exclude certain lists)', () => {
    const result = namer('#000', {omit: ['html']});
    expect(result.html).toBeUndefined();
    expect(result.basic).toBeDefined();
  });

  it('should allow both pick and omit, with pick taking precedence', () => {
    const result = namer('#000', {pick: ['html', 'pantone'], omit: ['pantone']});
    expect(Object.keys(result)).toEqual(['html']);
  });

  it('should cache results if the same color/options are passed', () => {
    const options = {pick: ['basic']};
    const first = namer('#000', options);
    const second = namer('#000', options);
    expect(first).toStrictEqual(second); // Cache returns deep-equal object (not same reference)
  });

  it('should use distance: "deltaE" for distance calculation', () => {
    const options = {distance: 'deltaE'};
    const result = namer('#000', options);
    expect(result).toBeDefined();
    expect(Array.isArray(result.basic)).toBe(true);
    expect(result.basic[0]).toHaveProperty('distance');
  });

  it('should export chroma', () => {
    expect(namer.chroma).toBeDefined();
    expect(typeof namer.chroma).toBe('function');
    expect(namer.chroma('red').hex()).toBe('#ff0000');
  });

  it('should export lists', () => {
    expect(namer.lists).toBeDefined();
    expect(namer.lists).toHaveProperty('ntc');
    expect(Array.isArray(namer.lists.ntc)).toBe(true);
  });

  it('should throw for unrecognized colors', () => {
    expect(() => namer('notacolor')).toThrow();
  });

  it('should not throw if color argument is an object from chroma.js', () => {
    const color = chroma('red');
    expect(() => namer(color)).not.toThrow();
  });
});