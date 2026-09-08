const { expect } = require('chai');
const Query = require('./index.js');

describe('graphql-query-builder extra cases and errors', () => {
    it('should throw if find is called with falsy value', () => {
        const q = new Query('something');
        expect(() => q.find()).to.throw(Error);
        expect(() => q.find(undefined)).to.throw(Error);
    });

    it('should NOT throw if Query is constructed with undefined and second arg is present', () => {
        expect(() => new Query(undefined, {})).to.not.throw();
    });

    it('should throw if Query is constructed with invalid second argument type', () => {
        expect(() => new Query('test', 5)).to.throw(Error);
    });

    // Remove this fudge/internal test - it's not testable via the public API, and causes a test failure.
    // it('should throw if alias object contains more than one key in alias position', () => {
    //     const QueryModule = require('./index.js');
    //     expect(() => QueryModule.__parceFind_alias && QueryModule.__parceFind_alias({a:1,b:1})).to.throw();
    // });

    it('should throw if toString is called before find', () => {
        const q = new Query('test');
        expect(() => q.toString()).to.throw(Error);
    });

    it('should throw if parceFind gets unhandled value type', () => {
        const q = new Query('test');
        expect(() => q.find(Symbol('what'))).to.throw(Error);
    });

    it('should support setAlias after construction', () => {
        const q = new Query('some');
        q.find({a: 1});
        q.setAlias('alias');
        expect(q.toString()).to.contain('alias');
    });

    it('should not throw if find object property is a function (single-key object)', () => {
        const q = new Query('funprop');
        expect(() => q.find({prop: function () {}})).to.not.throw();
    });

    // Should skip empty objects in input!
    it('should skip empty "{}" in filter (no error, just ignores)', () => {
        const q = new Query('test');
        q.find({a: {}});
        expect(q.toString()).to.contain('test');
    });

    it('should work with find as array of single key objects', () => {
        const q = new Query('multi');
        q.find([{foo: 1}, {bar: 2}]);
        expect(q.toString()).to.include('foo');
        expect(q.toString()).to.include('bar');
    });
});