const { strict: assert } = require('assert');
const Color = require('../color');

// Public tests: cover same logic as test/color-extra.test.js but with different test data

describe('Color extra edge cases (public)', function() {
    it('should create from RGBA values (public)', function() {
        var c = Color({red:0.25, green:0.45, blue:0.15, alpha:0.85});
        assert(Math.abs(c.getRed() - 0.25) < 0.00001);
        assert(Math.abs(c.getGreen() - 0.45) < 0.00001);
        assert(Math.abs(c.getBlue() - 0.15) < 0.00001);
        assert(Math.abs(c.getAlpha() - 0.85) < 0.00001);
    });
    it('should default to black for invalid input type (public)', function() {
        // Use a different invalid object
        const c = Color({baz:12345});
        assert.deepEqual([c.getRed(), c.getGreen(), c.getBlue()], [0, 0, 0]);
    });
    it('should create from HSV object (public)', function() {
        let c = Color({hue:45, saturation:0.8, value:0.9, alpha:0.2});
        assert(Math.abs(c.getHue() - 45) < 0.00001);
        assert(Math.abs(c.getSaturation() - 0.8) < 0.00001);
        assert(Math.abs(c.getValue() - 0.9) < 0.00001);
        assert(Math.abs(c.getAlpha() - 0.2) < 0.00001);
    });
    it('should create from HSL object (public)', function() {
        let c = Color({hue:60, saturation:0.7, lightness:0.25, alpha:0.35});
        assert(Math.abs(c.getHue() - 60) < 0.00001);
        assert(Math.abs(c.getSaturation() - 0.7) < 0.00001);
        assert(Math.abs(c.getLightness() - 0.25) < 0.00001);
        assert(Math.abs(c.getAlpha() - 0.35) < 0.00001);
    });
    it('should parse array constructor (public)', function() {
        let c = Color([10, 200, 30, 0.3]);
        assert(Math.abs(c.getRed() - (10/255)) < 0.0001);
        assert(Math.abs(c.getGreen() - (200/255)) < 0.0001);
        assert(Math.abs(c.getBlue() - (30/255)) < 0.0001);
        assert(Math.abs(c.getAlpha() - 0.3) < 0.0001);
    });
    it('should output correct CSS string (public)', function() {
        let c = Color({red:0, green:1, blue:0.3});
        let css = c.toCSS();
        assert(/^rgb\(/.test(css) || /^#/.test(css));
    });
    it('should blend colors correctly (public)', function() {
        let c1 = Color({red:0, green:1, blue:0, alpha:1});
        let c2 = Color({red:0, green:0, blue:0, alpha:1});
        let mix = c1.blend(c2, 0.3);
        assert(Math.abs(mix.getGreen() - 0.7) < 0.01);
    });
    it('should generate schemes (public)', function() {
        let c = Color('gold');
        let comp = c.complementaryScheme();
        assert(Array.isArray(comp));
        let triadic = c.triadicScheme();
        assert(Array.isArray(triadic));
    });
    it('should test color manipulation methods (public)', function() {
        let c = Color('green');
        let dark = c.darkenByAmount(0.2);
        let lighter = c.lightenByRatio(0.3);
        assert(typeof dark === 'object');
        assert(typeof lighter === 'object');
        let sat = c.saturateByRatio(0.3);
        let desat = c.desaturateByAmount(0.1);
        assert(typeof sat === 'object');
        assert(typeof desat === 'object');
    });
    it('should convert color to different string formats (public)', function() {
        let c = Color({red:0.5, green:0, blue:1});
        assert(typeof c.toString() === 'string');
        let hsv = c.toHSV();
        let hsl = c.toHSL();
        let rgb = c.toRGB();
        assert(typeof hsv === 'object');
        assert(typeof hsl === 'object');
        assert(typeof rgb === 'object');
    });
    it('should handle invalid CSS color input (public)', function() {
        let valid = Color.isValid('definitelynotacolor');
        assert.equal(valid, false);
        let valid2 = Color.isValid('blueviolet');
        assert.equal(valid2, true);
    });
    it('should roundtrip rgb and hsl (public)', function() {
        let c = Color({red:0.2, green:0.5, blue:0.75});
        let hsl = c.toHSL();
        let c2 = Color(hsl);
        assert(Color.isValid(c2.toCSS()));
    });
    it('should handle alpha < 1 (public)', function() {
        let c = Color({red:0.4, green:0.7, blue:0.2, alpha:0.12});
        let css = c.toCSS();
        assert(css.includes('rgba') || css.includes('rgb') || /^#/.test(css));
    });
});