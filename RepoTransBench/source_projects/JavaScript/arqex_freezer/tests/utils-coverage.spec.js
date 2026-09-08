const { expect } = require('chai');
const utils = require('../src/utils');

describe('utils.js basics', () => {
    describe('isArray', () => {
        it('should return true for arrays', () => {
            expect(utils.isArray([])).to.be.true;
        });
        it('should return false for non-arrays', () => {
            expect(utils.isArray({})).to.be.false;
            expect(utils.isArray('a')).to.be.false;
            expect(utils.isArray(null)).to.be.false;
        });
    });
    describe('isObject', () => {
        it('should return true for objects', () => {
            expect(utils.isObject({})).to.be.true;
        });
        it('should return false for null, array, functions', () => {
            expect(utils.isObject(null)).to.be.false;
            expect(utils.isObject([])).to.be.false;
            expect(utils.isObject(()=>{})).to.be.false;
        });
    });
    describe('isFunction', () => {
        it('should return true for function', () => {
            expect(utils.isFunction(()=>{})).to.be.true;
        });
        it('should return false for non-function', () => {
            expect(utils.isFunction(1)).to.be.false;
            expect(utils.isFunction({})).to.be.false;
        });
    });
    describe('own', () => {
        it('should act like hasOwnProperty', () => {
            const obj = { a: 1 };
            expect(utils.own(obj, 'a')).to.be.true;
            expect(utils.own(obj, 'b')).to.be.false;
        });
    });
    describe('equal', () => {
        it('should check primitives', () => {
            expect(utils.equal(1, 1)).to.be.true;
            expect(utils.equal(1, 2)).to.be.false;
        });
        it('should compare arrays', () => {
            expect(utils.equal([1,2],[1,2])).to.be.true;
            expect(utils.equal([1],[1,2])).to.be.false;
        });
        it('should compare objects', () => {
            expect(utils.equal({a:1}, {a:1})).to.be.true;
            expect(utils.equal({a:1}, {a:2})).to.be.false;
            expect(utils.equal({a:1}, {a:1, b:2})).to.be.false;
        });
        it('should compare null and undefined', () => {
            expect(utils.equal(null, null)).to.be.true;
            expect(utils.equal(undefined, undefined)).to.be.true;
            expect(utils.equal(null, undefined)).to.be.false;
        });
    });
});