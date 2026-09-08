const utils = require('../src/utils');

describe('utils extra edge/branch coverage - public data', function() {
    it('isArray should return false for string', function() {
        expect(utils.isArray("hello")).toBe(false);
    });
    it('isObject should return false for boolean', function() {
        expect(utils.isObject(true)).toBe(false);
    });
    it('isFunction should return false for a number', function() {
        expect(utils.isFunction(123)).toBe(false);
    });
    it('own should work for object with undefined prototype and different property', function() {
        let obj = Object.create(null);
        obj.y = 2;
        expect(utils.own(obj, 'y')).toBe(true);
    });
    it('equal should detect non-identical objects with same key but different value', function() {
        expect(utils.equal({a: 2}, {a: 3})).toBe(false);
    });
    it('equal should detect arrays with same length but different contents', function() {
        expect(utils.equal(['x', 'y'], ['x', 'z'])).toBe(false);
    });
});