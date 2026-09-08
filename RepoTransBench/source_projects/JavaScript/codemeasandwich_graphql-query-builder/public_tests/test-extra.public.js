const { expect } = require('chai');
const Query = require('../index.js');

describe('graphql-query-builder extra cases and errors (public)', () => {
    it('should throw if find is called with falsy value (public)', () => {
        const q = new Query('somethingElse');
        expect(() => q.find(null)).to.throw(Error);
        expect(() => q.find(false)).to.throw(Error);
    });

    it('should NOT throw if Query is constructed with undefined and second arg is object', () => {
        expect(() => new Query(undefined, {foo: 42})).to.not.throw();
    });

    it('should throw if Query is constructed with invalid second argument type (public)', () => {
        expect(() => new Query('sample', true)).to.throw(Error);
    });

    it('should throw if toString is called before find (public)', () => {
        const q = new Query('mytest');
        expect(() => q.toString()).to.throw(Error);
    });

    it('should throw if parceFind gets unhandled value type (public)', () => {
        const q = new Query('bar');
        expect(() => q.find(BigInt(10))).to.throw(Error);
    });

    it('should support setAlias after construction (public)', () => {
        const q = new Query('jane');
        q.find({score: 99});
        q.setAlias('otheralias');
        expect(q.toString()).to.contain('otheralias');
    });
}
);