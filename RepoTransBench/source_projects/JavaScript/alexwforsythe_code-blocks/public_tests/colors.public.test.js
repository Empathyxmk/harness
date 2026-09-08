const { colorToHex, NAME_TO_HEX } = require('../server/colors');

describe('colorToHex', () => {
    it('should convert 6-digit hex to itself', () => {
        expect(colorToHex('#abcdef')).toBe('#abcdef');
    });
    it('should convert 3-digit hex to 6-digit', () => {
        expect(colorToHex('#123')).toBe('#112233');
    });
    it('should handle color names if map exists', () => {
        expect(colorToHex('red')).toBe('#ff0000');
    });
    it('should return original string for unknown names', () => {
        expect(colorToHex('notacolor')).toBe('notacolor');
    });
    it('should not convert invalid hex', () => {
        expect(colorToHex('#12ab')).toBe('#12ab');
    });
    it('should return input if not a string', () => {
        expect(colorToHex(false)).toBe(false);
    });
});