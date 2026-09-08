const { colorToHex, NAME_TO_HEX } = require('../colors');

describe('colorToHex', () => {
    it('should convert 6-digit hex to itself', () => {
        expect(colorToHex('#12abcd')).toBe('#12abcd');
    });
    it('should convert 3-digit hex to 6-digit', () => {
        expect(colorToHex('#abc')).toBe('#aabbcc');
    });
    it('should handle color names if map exists', () => {
        expect(colorToHex('blue')).toBe('#0000ff');
    });
    it('should return original string for unknown names', () => {
        expect(colorToHex('unknowncolor')).toBe('unknowncolor');
    });
    it('should not convert invalid hex', () => {
        expect(colorToHex('#abcd')).toBe('#abcd');
    });
    it('should return input if not a string', () => {
        expect(colorToHex(123)).toBe(123);
    });
});