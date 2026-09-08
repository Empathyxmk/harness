const utils = require('../src/utils');

describe('utils.js - public branches', function() {
    it('isArray detects array (public)', function() {
        expect(utils.isArray([10, 20])).toBe(true);
        expect(utils.isArray({k: 1})).toBe(false);
    });

    it('isObject detects objects and not array (public)', function() {
        expect(utils.isObject({b: 2})).toBe(true);
        expect(utils.isObject([])).toBe(false);
    });

    it('isFunction detects function and not string (public)', function() {
        expect(utils.isFunction(function(){})).toBe(true);
        expect(utils.isFunction("not a func")).toBe(false);
    });

    it('own properly detects own and prototype properties (public)', function() {
        function C() { this.a = 9; }
        C.prototype.b = 12;
        let obj = new C();
        expect(utils.own(obj, "a")).toBe(true);
        expect(utils.own(obj, "b")).toBe(false);
    });

    it('equal returns true for same value primitives (public)', function() {
        expect(utils.equal("foo", "foo")).toBe(true);
    });

    it('equal returns false for different-length arrays (public)', function() {
        expect(utils.equal([1,2,3], [1,2])).toBe(false);
    });
});