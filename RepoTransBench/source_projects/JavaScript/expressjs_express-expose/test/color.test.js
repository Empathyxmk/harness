const assert = require('assert');
const color = require('../examples/color');

describe('color utility', function() {
  describe('parseRGB', function() {
    it('should parse #ff0000 correctly', function() {
      const rgb = color.parseRGB('#ff0000');
      assert.deepStrictEqual(rgb, { r: 255, g: 0, b: 0 });
    });
    it('should parse #00ff00 correctly', function() {
      const rgb = color.parseRGB('#00ff00');
      assert.deepStrictEqual(rgb, { r: 0, g: 255, b: 0 });
    });
    it('should parse #0000ff correctly', function() {
      const rgb = color.parseRGB('#0000ff');
      assert.deepStrictEqual(rgb, { r: 0, g: 0, b: 255 });
    });
    it('should parse short hex strings (no #) as well', function() {
      const rgb = color.parseRGB('000000');
      assert.deepStrictEqual(rgb, { r: 0, g: 0, b: 0 });
    });
  });

  describe('lightness', function() {
    it('should compute lightness for #808080 (~50.196)', function() {
      const l = color.lightness('#808080');
      assert(Math.abs(l - 50.196) < 0.01);
    });
    it('should compute lightness for #ffffff (should be 100)', function() {
      const l = color.lightness('#ffffff');
      assert(Math.abs(l - 100) < 0.01);
    });
    it('should compute lightness for #000000 (should be 0)', function() {
      const l = color.lightness('#000000');
      assert(Math.abs(l - 0) < 0.01);
    });
  });

  describe('light', function() {
    it('should return true for a light color (#fff)', function() {
      assert.strictEqual(color.light('#ffffff'), true);
    });
    it('should return false for a dark color (#000)', function() {
      assert.strictEqual(color.light('#000000'), false);
    });
    // According to the color utility code, "light" returns true for middle gray
    it('should return true for middle gray (#808080)', function() {
      assert.strictEqual(color.light('#808080'), true);
    });
  });

  describe('dark', function() {
    it('should return true for a dark color (#000)', function() {
      assert.strictEqual(color.dark('#000000'), true);
    });
    it('should return false for a light color (#fff)', function() {
      assert.strictEqual(color.dark('#ffffff'), false);
    });
    // According to the color utility code, "dark" returns false for middle gray
    it('should return false for middle gray (#808080)', function() {
      assert.strictEqual(color.dark('#808080'), false);
    });
  });
});