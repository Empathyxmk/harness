const frozen = require('../src/frozen');

describe('frozen.js extra branches', function() {
    it('should not re-freeze already frozen objects', function() {
        const obj = { a: 1 };
        const froz1 = frozen.freeze(obj);
        const froz2 = frozen.freeze(froz1);
        expect(froz1).toBe(froz2);
    });

    it('should allow toJS on primitives', function() {
        expect(frozen.toJS(5)).toBe(5);
        expect(frozen.toJS(null)).toBe(null);
        expect(frozen.toJS(undefined)).toBe(undefined);
    });

    it('should handle equals for custom equals', function() {
        function MyType() {}
        MyType.prototype.equals = function (other) { return false; };
        const a = new MyType(), b = new MyType();
        expect(frozen.equals(a, b)).toBe(false);
    });

    it('should handle equals for circular structures', function() {
        const a = {};
        a.self = a;
        const b = {};
        b.self = b;
        expect(frozen.equals(a, b)).toBe(true);
    });

    it('should handle cyclic check with primitives', function() {
        expect(frozen.equals(1, 1)).toBe(true);
    });
});