const frozen = require('../src/frozen');

describe('frozen.js extra branches - public data', function() {
    it('should not re-freeze already frozen arrays', function() {
        const arr = [2, 3];
        const froz1 = frozen.freeze(arr);
        const froz2 = frozen.freeze(froz1);
        expect(froz1).toBe(froz2);
    });

    it('should allow toJS on string and boolean primitives', function() {
        expect(frozen.toJS("test")).toBe("test");
        expect(frozen.toJS(false)).toBe(false);
        expect(frozen.toJS(undefined)).toBe(undefined);
    });

    it('should handle equals for custom equals that returns true', function() {
        function CustomType() {}
        CustomType.prototype.equals = function (other) { return true; };
        const a = new CustomType(), b = new CustomType();
        expect(frozen.equals(a, b)).toBe(true);
    });

    it('should handle equals for self-referencing arrays (circular structures)', function() {
        const a = [];
        a.push(a);
        const b = [];
        b.push(b);
        expect(frozen.equals(a, b)).toBe(true);
    });

    it('should handle cyclic check with different primitives', function() {
        expect(frozen.equals("abc", "abc")).toBe(true);
    });
});