const escapeForXML = require('../lib/escapeForXML');

describe('escapeForXML', () => {
    it('escapes all relevant XML characters', () => {
        expect(escapeForXML('&"\'<>')).toBe('&amp;&quot;&apos;&lt;&gt;');
    });

    it('returns input when no escaping needed', () => {
        expect(escapeForXML('abc')).toBe('abc');
    });

    it('returns non-string input unchanged', () => {
        expect(escapeForXML(5)).toBe(5);
        expect(escapeForXML(null)).toBe(null);
        expect(escapeForXML(undefined)).toBe(undefined);
    });

    it('works with empty string', () => {
        expect(escapeForXML('')).toBe('');
    });
});