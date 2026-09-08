const frozen = require('../src/frozen');

describe('frozen.js branches - public data', function() {
    it('should freeze object and keep properties (public)', function() {
        let obj = {p: 6, q: "hi"};
        let fz = frozen.freeze(obj);
        expect(fz.p).toBe(6);
        expect(fz.q).toBe("hi");
        expect(Object.isFrozen(fz)).toBe(true);
    });

    it('should freeze array and keep values (public)', function() {
        let arr = [7, 11];
        let fz = frozen.freeze(arr);
        expect(Array.isArray(fz)).toBe(true);
        expect(fz[1]).toBe(11);
        expect(Object.isFrozen(fz)).toBe(true);
    });

    it('toJS should return unfrozen JS structures (public)', function() {
        let fz = frozen.freeze({u: 1, v: [9, 10]});
        let val = frozen.toJS(fz);
        expect(val).toEqual({u: 1, v: [9, 10]});
    });

    it('equals returns true for deep equal plain objects (public)', function() {
        expect(frozen.equals({x: 1, y: 2}, {x: 1, y: 2})).toBe(true);
    });

    it('equals returns false for different plain objects (public)', function() {
        expect(frozen.equals({x: 99}, {z: 99})).toBe(false);
    });
});