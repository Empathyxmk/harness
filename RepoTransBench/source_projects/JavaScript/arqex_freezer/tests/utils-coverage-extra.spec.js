const utils = require('../src/utils');

describe('utils extra edge/branch coverage', function() {
    it('isArray should return false for null', function() {
        expect(utils.isArray(null)).toBe(false);
    });
    it('isObject should return false for number', function() {
        expect(utils.isObject(0)).toBe(false);
    });
    it('isFunction should return false for null', function() {
        expect(utils.isFunction(null)).toBe(false);
    });
    it('own should work for undefined prototype', function() {
        let obj = Object.create(null);
        obj.x = 1;
        expect(utils.own(obj, 'x')).toBe(true);
    });
    it('equal should detect non-identical objects with different keys', function() {
        expect(utils.equal({a: 1}, {b: 1})).toBe(false);
    });
    it('equal should detect arrays of different lengths', function() {
        expect(utils.equal([1,2], [1])).toBe(false);
    });
});