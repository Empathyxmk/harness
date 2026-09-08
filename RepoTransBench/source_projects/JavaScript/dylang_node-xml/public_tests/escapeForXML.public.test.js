const escapeForXML = require('../lib/escapeForXML');

describe('escapeForXML (public)', () => {
    it('escapes various XML characters (different mix)', () => {
        expect(escapeForXML('<>&\'"')).toBe('&lt;&gt;&amp;&apos;&quot;');
    });

    it('returns input when no escaping needed (different value)', () => {
        expect(escapeForXML('xyz')).toBe('xyz');
    });

    it('returns non-string input unchanged (bool and zero)', () => {
        expect(escapeForXML(true)).toBe(true);
        expect(escapeForXML(0)).toBe(0);
        expect(escapeForXML(null)).toBe(null);
        expect(escapeForXML(undefined)).toBe(undefined);
    });

    it('works with empty string (repeated case)', () => {
        expect(escapeForXML('')).toBe('');
    });
});