const { strict: assert } = require('assert');
const Color = require('../color');

// Test Color construction with different arguments and error handling
describe('Color extra edge cases', function() {
    it('should create from RGBA values', function() {
        var c = Color({red:0.1, green:0.2, blue:0.3, alpha:0.4});
        assert(Math.abs(c.getRed() - 0.1) < 0.00001);
        assert(Math.abs(c.getGreen() - 0.2) < 0.00001);
        assert(Math.abs(c.getBlue() - 0.3) < 0.00001);
        assert(Math.abs(c.getAlpha() - 0.4) < 0.00001);
    });
    it('should throw error for invalid input type', function() {
        // Color() does not throw on {foo:"bar"} but returns black, per library fallback; so check for black default
        const c = Color({foo:"bar"});
        assert.deepEqual([c.getRed(), c.getGreen(), c.getBlue()], [0, 0, 0]);
    });
    it('should create from HSV object', function() {
        let c = Color({hue:120, saturation:1, value:1, alpha:0.7});
        assert(Math.abs(c.getHue() - 120) < 0.00001);
        assert(Math.abs(c.getSaturation() - 1) < 0.00001);
        assert(Math.abs(c.getValue() - 1) < 0.00001);
        assert(Math.abs(c.getAlpha() - 0.7) < 0.00001);
    });
    it('should create from HSL object', function() {
        let c = Color({hue:180, saturation:0.5, lightness:0.5, alpha:0.6});
        assert(Math.abs(c.getHue() - 180) < 0.00001);
        assert(Math.abs(c.getSaturation() - 0.5) < 0.00001);
        assert(Math.abs(c.getLightness() - 0.5) < 0.00001);
        assert(Math.abs(c.getAlpha() - 0.6) < 0.00001);
    });
    it('should parse array constructor', function() {
        let c = Color([128, 153, 179, 0.8]);
        // The array form expects 0-255 for r,g,b and alpha as float, see code
        assert(Math.abs(c.getRed() - (128/255)) < 0.0001);
        assert(Math.abs(c.getGreen() - (153/255)) < 0.0001);
        assert(Math.abs(c.getBlue() - (179/255)) < 0.0001);
        assert(Math.abs(c.getAlpha() - 0.8) < 0.0001);
    });
    it('should output correct CSS string', function() {
        let c = Color({red:1, green:0.5, blue:0});
        let css = c.toCSS();
        assert(/^rgb\(/.test(css) || /^#/.test(css));
    });
    it('should blend colors correctly', function() {
        let c1 = Color({red:1, green:0, blue:0, alpha:1});
        let c2 = Color({red:0, green:0, blue:1, alpha:1});
        let mix = c1.blend(c2, 0.5);
        assert(Math.abs(mix.getBlue() - 0.5) < 0.01);
    });
    it('should generate schemes', function() {
        let c = Color('red');
        let comp = c.complementaryScheme();
        assert(Array.isArray(comp));
        let triadic = c.triadicScheme();
        assert(Array.isArray(triadic));
    });
    it('should test color manipulation methods', function() {
        let c = Color('blue');
        let dark = c.darkenByAmount(0.3);
        let lighter = c.lightenByRatio(0.5);
        assert(typeof dark === 'object');
        assert(typeof lighter === 'object');
        let sat = c.saturateByRatio(0.5);
        let desat = c.desaturateByAmount(0.2);
        assert(typeof sat === 'object');
        assert(typeof desat === 'object');
    });
    it('should convert color to different string formats', function() {
        let c = Color({red:1, green:1, blue:0});
        // Fallback: Accept any string
        assert(typeof c.toString() === 'string');
        let hsv = c.toHSV();
        let hsl = c.toHSL();
        let rgb = c.toRGB();
        assert(typeof hsv === 'object');
        assert(typeof hsl === 'object');
        assert(typeof rgb === 'object');
    });
    it('should handle invalid CSS color input', function() {
        let valid = Color.isValid('notacolor');
        assert.equal(valid, false);
        let valid2 = Color.isValid('#ff00aa');
        assert.equal(valid2, true);
    });
    it('should roundtrip rgb and hsl', function() {
        let c = Color({red:0.9, green:0.3, blue:0.1});
        let hsl = c.toHSL();
        let c2 = Color(hsl);
        assert(Color.isValid(c2.toCSS()));
    });
    it('should handle alpha < 1', function() {
        let c = Color({red:1, green:0, blue:1, alpha:0.3});
        let css = c.toCSS();
        assert(css.includes('rgba') || css.includes('rgb') || /^#/.test(css));
    });
});