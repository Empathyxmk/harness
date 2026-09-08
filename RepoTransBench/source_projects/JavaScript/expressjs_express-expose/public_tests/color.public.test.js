const assert = require('assert');
const color = require('../examples/color');

describe('color utility (public tests)', function() {
  describe('parseRGB', function() {
    it('should parse #00ffff correctly', function() {
      const rgb = color.parseRGB('#00ffff');
      assert.deepStrictEqual(rgb, { r: 0, g: 255, b: 255 });
    });
    it('should parse #ffff00 correctly', function() {
      const rgb = color.parseRGB('#ffff00');
      assert.deepStrictEqual(rgb, { r: 255, g: 255, b: 0 });
    });
    it('should parse #ff00ff correctly', function() {
      const rgb = color.parseRGB('#ff00ff');
      assert.deepStrictEqual(rgb, { r: 255, g: 0, b: 255 });
    });
    it('should parse short hex strings (no #) as well', function() {
      const rgb = color.parseRGB('ffffff');
      assert.deepStrictEqual(rgb, { r: 255, g: 255, b: 255 });
    });
  });

  describe('lightness', function() {
    it('should compute lightness for #c0c0c0 (~75.294)', function() {
      const l = color.lightness('#c0c0c0');
      assert(Math.abs(l - 75.294) < 0.01);
    });
    it('should compute lightness for #ff0000 (should be ~50)', function() {
      const l = color.lightness('#ff0000');
      assert(Math.abs(l - 50) < 0.01);
    });
    it('should compute lightness for #010101 (should be ~0.20)', function() {
      const l = color.lightness('#010101');
      assert(Math.abs(l - 0.20) < 0.01);
    });
  });

  describe('light', function() {
    it('should return true for a light color (#eeeeee)', function() {
      assert.strictEqual(color.light('#eeeeee'), true);
    });
    it('should return false for a dark color (#121212)', function() {
      assert.strictEqual(color.light('#121212'), false);
    });
    it('should return true for gray between light and dark (#b0b0b0)', function() {
      assert.strictEqual(color.light('#b0b0b0'), true);
    });
  });

  describe('dark', function() {
    it('should return true for a dark color (#111111)', function() {
      assert.strictEqual(color.dark('#111111'), true);
    });
    it('should return false for a light color (#fafafa)', function() {
      assert.strictEqual(color.dark('#fafafa'), false);
    });
    it('should return false for mid gray (#b0b0b0)', function() {
      assert.strictEqual(color.dark('#b0b0b0'), false);
    });
  });
});